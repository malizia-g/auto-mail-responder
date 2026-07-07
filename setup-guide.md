
Setup github · MD
Setup GitHub Actions — Automazione Mail
Il workflow daily.yml fa girare lo script più volte al giorno (ogni 3 ore, 8-17 ora italiana) su GitHub, senza accendere il PC.

⚠️ Punto importante: l'autenticazione
Lo script, al primo avvio in locale, apre il browser per autorizzare Gmail e crea un file token.json. Su GitHub Actions NON c'è un browser, quindi devi:

Generare token.json una volta sul tuo PC (avvio locale con DRY_RUN)
Caricare sia credentials.json che token.json come secret su GitHub
Il token.json contiene un refresh token di lunga durata, quindi una volta caricato lo script si ri-autentica da solo ogni mattina senza browser.

Passo 1 — Genera token.json in locale
Sul tuo computer, nella cartella dello script:

bash
pip install -r requirements.txt
export DRY_RUN=true
export GMAIL_LABEL=DaRispondere
python3 auto_mail_responder.py
Si apre il browser → autorizza → viene creato token.json.

Passo 2 — Crea il repository (PRIVATO)
Su GitHub: New repository → spunta Private → carica:

auto_mail_responder.py
requirements.txt
README.md
regolamento.md ← le regole/FAQ (il "cervello")
formato-risposta.md ← il formato JSON richiesto all'AI
.github/workflows/daily.yml ← crea la cartella e mettici dentro daily.yml
NON caricare credentials.json né token.json nel repo! Vanno solo nei secret.
IMPORTANTE: carica anche regolamento.md e formato-risposta.md, altrimenti lo script si ferma con un errore.

Passo 3 — Configura Secrets e Variables
Nel repo: Settings → Secrets and variables → Actions

Secrets (dati sensibili)
Nome	Valore
GMAIL_CREDENTIALS_JSON	incolla tutto il contenuto di credentials.json
GMAIL_TOKEN_JSON	incolla tutto il contenuto di token.json
ANTHROPIC_API_KEY	la tua API key Claude (se usi Claude)
GEMINI_API_KEY	la tua API key Gemini (se usi Gemini)
Variables (configurazione non sensibile)
Nome	Valore esempio
AI_PROVIDER	claude oppure gemini
GEMINI_MODEL	nome del modello Gemini, es. gemini-2.5-flash (se usi Gemini)
CLAUDE_MODEL	claude-sonnet-4-6 (solo se usi Claude)
GMAIL_LABEL	DaRispondere
PROCESSED_LABEL	Elaborata
DRY_RUN	true (per i primi giorni!) poi false
AI_MAX_RETRIES	3 (tentativi se il modello è occupato; facoltativa)
AI_RETRY_WAIT_SECONDS	300 (attesa fra i tentativi in secondi = 5 min; facoltativa)
Passo 4 — Test manuale
Vai sul tab Actions → seleziona il workflow → Run workflow. Controlla il log: con DRY_RUN=true vedrai cosa avrebbe fatto senza inviare nulla.

Passo 5 — Attiva l'automazione
Quando sei soddisfatto, cambia la variabile DRY_RUN a false. Da quel momento gira ogni 3 ore dalle 8 alle 17 ora italiana (8, 11, 14, 17).

Orario di esecuzione
Il cron nel workflow è 0 6,9,12,15 * * * (ore UTC), cioè 8/11/14/17 in ora legale estiva italiana (CEST = UTC+2). Il cron di GitHub NON gestisce l'ora legale: in inverno (CET = UTC+1) devi aggiungere 1 a ogni ora → 0 7,10,13,16 * * *, altrimenti lo script partirà un'ora prima del previsto.

Nota sui costi
GitHub Actions è gratuito fino a 2000 minuti/mese sui repo privati. Lo script gira pochi secondi al giorno → consumo trascurabile.


