
Setup github · MD
Setup GitHub Actions — Automazione Mail
Il workflow daily.yml fa girare lo script ogni mattina su GitHub, senza accendere il PC.

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
.github/workflows/daily.yml ← crea la cartella e mettici dentro daily.yml
NON caricare credentials.json né token.json nel repo! Vanno solo nei secret.

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
GMAIL_LABEL	DaRispondere
PROCESSED_LABEL	Elaborata
DRY_RUN	true (per i primi giorni!) poi false
Passo 4 — Test manuale
Vai sul tab Actions → seleziona il workflow → Run workflow. Controlla il log: con DRY_RUN=true vedrai cosa avrebbe fatto senza inviare nulla.

Passo 5 — Attiva l'automazione
Quando sei soddisfatto, cambia la variabile DRY_RUN a false. Da quel momento gira ogni mattina alle 7:00 ora italiana (5:00 UTC nel workflow).

Orario di esecuzione
Il cron nel workflow è 0 5 * * * (5:00 UTC = 7:00 ora legale estiva italiana). In inverno diventerebbe le 6:00 italiane. Se vuoi un orario preciso tutto l'anno, puoi impostare due cron (uno estivo, uno invernale) oppure accettare lo scarto di un'ora.

Nota sui costi
GitHub Actions è gratuito fino a 2000 minuti/mese sui repo privati. Lo script gira pochi secondi al giorno → consumo trascurabile.


