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

# Facoltative (hanno un default sensato)
export GEMINI_MODEL=gemini-2.5-flash  # modello Gemini (default: gemini-2.5-flash-lite)
export BACKUP_GEMINI_MODEL=gemini-2.5-flash-lite  # modello di riserva se il principale
                                      # è sovraccarico o ha esaurito la quota giornaliera
                                      # (free tier). Vuoto = nessun fallback.
export CLAUDE_MODEL=claude-sonnet-4-6 # modello Claude
export AI_MAX_RETRIES=3               # tentativi se il modello è occupato (503/429)
export AI_RETRY_WAIT_SECONDS=300      # attesa fra i tentativi, in secondi (5 min)
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
Le regole NON sono più nel codice: stanno nei file markdown, facili da modificare.
- `regolamento.md` — le regole e le FAQ (il "cervello"). Aggiungi nuove regole con lo stesso formato della Regola 1.
- `formato-risposta.md` — il formato JSON tecnico richiesto all'AI (di solito non serve toccarlo).

Percorsi sovrascrivibili con le variabili `REGOLAMENTO_FILE` e `FORMATO_FILE`.
Se un file manca, lo script si ferma con un messaggio d'errore chiaro.

## Modello occupato / sovraccarico
Se l'AI risponde con un errore di sovraccarico (es. `503 UNAVAILABLE`, `429`), lo script
aspetta 5 minuti e riprova, fino a 3 tentativi. Regolabile con `AI_MAX_RETRIES` e
`AI_RETRY_WAIT_SECONDS`.

## Sicurezza
- `credentials.json` e `token.json` contengono accessi sensibili: NON caricarli su repo pubblici.
- Le API key vanno sempre in variabili d'ambiente, mai scritte nel codice.

