# Automazione Risposte Mail — Commissione Orario

## Cosa fa
Ogni mattina legge le mail con una certa etichetta Gmail, le confronta con il regolamento,
e tramite Claude o Gemini decide se **inviare automaticamente** (confidenza alta) o
**salvare come bozza** (confidenza media/bassa).

## Setup in 5 passi

### 1. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 2. Configura Gmail API
1. Vai su https://console.cloud.google.com
2. Crea un progetto (o usane uno esistente)
3. Abilita la **Gmail API**
4. Crea credenziali OAuth 2.0 (tipo "App desktop")
5. Scarica il file e rinominalo `credentials.json`, mettilo nella stessa cartella dello script

### 3. Scegli il provider AI e imposta le chiavi
Imposta le variabili d'ambiente:
```bash
export AI_PROVIDER=claude          # oppure "gemini"
export ANTHROPIC_API_KEY=sk-ant-...   # se usi Claude
export GEMINI_API_KEY=...             # se usi Gemini
export GMAIL_LABEL=DaRispondere       # nome dell'etichetta da monitorare
```

### 4. Crea l'etichetta in Gmail
In Gmail crea un'etichetta (es. "DaRispondere") e imposta un filtro che la applichi
automaticamente alle mail che vuoi far gestire allo script.

### 5. Primo avvio (test)
```bash
export DRY_RUN=true   # modalità test: non invia/salva nulla, mostra solo cosa farebbe
python3 auto_mail_responder.py
```
Al primo avvio si aprirà il browser per autorizzare l'accesso a Gmail.
Quando sei soddisfatto, togli DRY_RUN e fai partire per davvero.

## Hosting automatico
Per farlo girare ogni mattina senza accendere il PC:
- **PythonAnywhere** — task schedulato giornaliero (piano gratuito)
- **Google Cloud Run + Cloud Scheduler** — serverless, crediti gratuiti iniziali
- **GitHub Actions** — workflow cron schedulato

## Modificare il regolamento
Tutte le regole sono nella variabile `REGOLAMENTO` dentro `auto_mail_responder.py`.
Aggiungi nuove regole con lo stesso formato della Regola 1.

## Sicurezza
- `credentials.json` e `token.json` contengono accessi sensibili: NON caricarli su repo pubblici.
- Le API key vanno sempre in variabili d'ambiente, mai scritte nel codice.

