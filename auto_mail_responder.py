#!/usr/bin/env python3
"""
Automazione Risposte Mail - Commissione Orario IIS Galvani/Mi
================================================================
Ogni mattina:
  1. Legge le mail con una certa etichetta Gmail
  2. Le confronta con un regolamento (FAQ)
  3. Genera una risposta tramite Claude o Gemini
  4. Invia automaticamente (confidenza alta) o salva come bozza (confidenza media/bassa)

Configurazione tramite variabili d'ambiente - vedi sezione CONFIG.
"""

import os
import json
import base64
import logging
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ============================================================
# CONFIG - modifica qui o usa variabili d'ambiente
# ============================================================
LABEL_NAME = os.environ.get("GMAIL_LABEL", "DaRispondere")  # etichetta da monitorare
PROVIDER = os.environ.get("AI_PROVIDER", "gemini")  # "claude" oppure "gemini"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")
PROCESSED_LABEL = os.environ.get("PROCESSED_LABEL", "Elaborata")  # etichetta dopo elaborazione
AI_REPLIED_LABEL = os.environ.get("AI_REPLIED_LABEL", "Risposta da AI")
LEVEL2_REVIEW_LABEL = os.environ.get("LEVEL2_REVIEW_LABEL", "Da controllare a livello 2")
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"  # se true, non invia nulla

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("mail-responder")

# ============================================================
# REGOLAMENTO / FAQ
# Questo è il "cervello" del sistema. Aggiungi qui le regole.
# ============================================================
REGOLAMENTO = """
Sei l'assistente della Commissione Orario dell'IIS Galvani/Mi.
Rispondi alle mail in italiano, in tono cortese e formale (dai del "tu" ai colleghi/studenti).
Firma sempre come "La Commissione Orario".

REGOLE:

[Regola 1] Richiesta accesso con account Gmail personale
- Trigger: qualcuno chiede accesso a un file/modulo dell'istituto usando un indirizzo @gmail.com (non istituzionale)
- Confidenza: ALTA -> invio automatico
- Risposta:
  "Gentile [Nome], i moduli e i file dell'istituto sono accessibili esclusivamente
  tramite account istituzionale. Ti chiediamo di effettuare l'accesso con il tuo account
  @iisgalvanimi.edu.it e riprovare. Per qualsiasi problema con l'account istituzionale,
  rivolgiti alla segreteria. Grazie per la collaborazione."

[Regola generale]
- Se la mail non rientra in nessuna regola conosciuta, oppure è ambigua, o richiede
  una decisione discrezionale -> confidenza BASSA -> salva come bozza.
- Non inventare informazioni non presenti nel regolamento.
"""

# ============================================================
# OUTPUT RICHIESTO ALL'AI
# ============================================================
SYSTEM_INSTRUCTIONS = REGOLAMENTO + """

Analizza la mail fornita e rispondi ESCLUSIVAMENTE con un oggetto JSON valido,
senza testo aggiuntivo, senza backtick, con questa struttura esatta:

{
  "categoria": "stringa breve che identifica il tipo di richiesta",
  "confidenza": "alta" | "media" | "bassa",
  "azione": "invia_automatico" | "salva_bozza",
  "oggetto_risposta": "oggetto della mail di risposta",
  "testo_risposta": "corpo completo della mail di risposta"
}

Regola per 'azione':
- confidenza "alta"  -> "invia_automatico"
- confidenza "media" o "bassa" -> "salva_bozza"
"""


# ============================================================
# AUTENTICAZIONE GMAIL
# ============================================================
def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


# ============================================================
# FUNZIONI GMAIL
# ============================================================
def get_label_id(service, label_name):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for lbl in labels:
        if lbl["name"].lower() == label_name.lower():
            return lbl["id"]
    return None


def ensure_label(service, label_name):
    label_id = get_label_id(service, label_name)
    if label_id:
        return label_id
    body = {"name": label_name, "labelListVisibility": "labelShow",
            "messageListVisibility": "show"}
    created = service.users().labels().create(userId="me", body=body).execute()
    return created["id"]


def list_messages_with_label(service, label_id):
    result = service.users().messages().list(
        userId="me", labelIds=[label_id]
    ).execute()
    return result.get("messages", [])


def get_message_detail(service, msg_id):
    msg = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()
    headers = {h["name"].lower(): h["value"] for h in msg["payload"]["headers"]}
    body = extract_body(msg["payload"])
    return {
        "id": msg_id,
        "thread_id": msg["threadId"],
        "from": headers.get("from", ""),
        "subject": headers.get("subject", ""),
        "to": headers.get("to", ""),
        "message_id_header": headers.get("message-id", ""),
        "body": body,
    }


def extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and part["body"].get("data"):
                return base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8", errors="ignore")
        # fallback ricorsivo
        for part in payload["parts"]:
            res = extract_body(part)
            if res:
                return res
    elif payload["body"].get("data"):
        return base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode("utf-8", errors="ignore")
    return ""


def parse_sender_email(from_header):
    """Estrae l'indirizzo email dal campo From."""
    if "<" in from_header and ">" in from_header:
        return from_header.split("<")[1].split(">")[0].strip()
    return from_header.strip()


def create_mime_message(to_addr, subject, body_text, thread_id=None,
                        in_reply_to=None):
    message = MIMEText(body_text, "plain", "utf-8")
    message["to"] = to_addr
    message["subject"] = subject
    if in_reply_to:
        message["In-Reply-To"] = in_reply_to
        message["References"] = in_reply_to
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    body = {"raw": raw}
    if thread_id:
        body["threadId"] = thread_id
    return body


def send_reply(service, msg_body):
    return service.users().messages().send(userId="me", body=msg_body).execute()


def save_draft(service, msg_body):
    return service.users().drafts().create(
        userId="me", body={"message": msg_body}
    ).execute()


def mark_processed(service, msg_id, source_label_id, add_label_ids):
    service.users().messages().modify(
        userId="me", id=msg_id,
        body={"removeLabelIds": [source_label_id],
              "addLabelIds": add_label_ids},
    ).execute()


# ============================================================
# AI PROVIDERS
# ============================================================
def ask_claude(mail_text):
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1500,
        system=SYSTEM_INSTRUCTIONS,
        messages=[{"role": "user", "content": mail_text}],
    )
    return resp.content[0].text


def ask_gemini(mail_text):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=mail_text,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
        ),
    )
    return resp.text or ""


def get_ai_response(mail_text):
    raw = ask_claude(mail_text) if PROVIDER == "claude" else ask_gemini(mail_text)
    # pulizia eventuali backtick
    cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)


# ============================================================
# MAIN
# ============================================================
def main():
    log.info("Avvio automazione risposte mail (provider=%s, dry_run=%s)",
             PROVIDER, DRY_RUN)
    service = get_gmail_service()

    source_label_id = get_label_id(service, LABEL_NAME)
    if not source_label_id:
        log.error("Etichetta '%s' non trovata. Creala in Gmail.", LABEL_NAME)
        return
    processed_label_id = ensure_label(service, PROCESSED_LABEL)
    ai_replied_label_id = ensure_label(service, AI_REPLIED_LABEL)
    level2_review_label_id = ensure_label(service, LEVEL2_REVIEW_LABEL)

    messages = list_messages_with_label(service, source_label_id)
    log.info("Trovate %d mail da elaborare", len(messages))

    for m in messages:
        try:
            detail = get_message_detail(service, m["id"])
            sender = parse_sender_email(detail["from"])
            log.info("Elaboro mail da %s | oggetto: %s", sender, detail["subject"])

            ai_input = (
                f"Mittente: {detail['from']}\n"
                f"Oggetto: {detail['subject']}\n\n"
                f"Corpo:\n{detail['body']}"
            )
            result = get_ai_response(ai_input)
            log.info("  -> categoria=%s confidenza=%s azione=%s",
                     result.get("categoria"), result.get("confidenza"),
                     result.get("azione"))

            reply_subject = result.get("oggetto_risposta") or f"Re: {detail['subject']}"
            reply_body = result["testo_risposta"]
            msg_body = create_mime_message(
                to_addr=sender,
                subject=reply_subject,
                body_text=reply_body,
                thread_id=detail["thread_id"],
                in_reply_to=detail["message_id_header"],
            )

            if DRY_RUN:
                log.info("  [DRY_RUN] nessuna azione eseguita")
                log.info("  Testo risposta:\n%s", reply_body)
                if result.get("azione") == "invia_automatico":
                    log.info("  [DRY_RUN] etichette che verrebbero aggiunte: %s, %s",
                             PROCESSED_LABEL, AI_REPLIED_LABEL)
                else:
                    log.info("  [DRY_RUN] etichette che verrebbero aggiunte: %s, %s",
                             PROCESSED_LABEL, LEVEL2_REVIEW_LABEL)
                continue

            if result.get("azione") == "invia_automatico":
                send_reply(service, msg_body)
                log.info("  ✓ Risposta INVIATA automaticamente")
                target_label_ids = [processed_label_id, ai_replied_label_id]
            else:
                save_draft(service, msg_body)
                log.info("  ✓ Bozza SALVATA per revisione")
                target_label_ids = [processed_label_id, level2_review_label_id]

            mark_processed(service, m["id"], source_label_id, target_label_ids)

        except Exception as e:
            log.exception("Errore elaborando mail %s: %s", m["id"], e)

    log.info("Elaborazione completata.")


if __name__ == "__main__":
    main()
