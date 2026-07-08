# Report test del regolamento — 7 luglio 2026

Test dell'auto-responder con **12 mail simulate** passate nella pipeline reale di
`auto_mail_responder.py` (provider Gemini), senza toccare Gmail. Il regolamento testato è
la versione di [regolamento.md](regolamento.md) aggiornata il 7/7/2026 (regole 1–5 +
contesto dal regolamento orario ufficiale a.s. 2026/27).

**Esito finale: 12/12 azioni corrette** (2 casi corretti dopo un fix al regolamento
individuato proprio grazie al test, v. sezione "Problemi trovati").

## Tabella riassuntiva

| # | Caso | Mail simulata | Attesa | Ottenuto | Esito |
|---|------|---------------|--------|----------|-------|
| 1 | Accesso da @gmail.com | Notifica Drive "richiede l'accesso" | invio auto | alta → invio auto | ✅ |
| 2 | Accesso da altra scuola | Richiesta accesso da @iiscremona.it | invio auto | alta → invio auto | ✅ |
| 3 | 🪤 Accesso da account istituzionale | Richiesta accesso da @iisgalvanimi.edu.it | bozza | bassa → bozza | ✅ * |
| 4 | Link form desiderata | "Non trovo più il link del modulo" | invio auto | alta → invio auto | ✅ |
| 5 | Link form punteggio | "Dove calcolo il punteggio?" | invio auto | alta → invio auto | ✅ |
| 6 | Domanda crediti (figli+distanza) | "Quanti crediti mi spettano?" | bozza | media → bozza | ✅ |
| 7 | Domanda part-time | "Giorno libero E desiderata?" | bozza | media → bozza | ✅ |
| 8 | Segnalazione errore orario | Sovrapposizione 4BINF/2A | bozza | media → bozza | ✅ |
| 9 | Richiesta cambio orario | Spostare 1ª ora lunedì | bozza | bassa → bozza | ✅ |
| 10 | Salute grave + certificato | Terapie ogni mercoledì | bozza | media → bozza | ✅ |
| 11 | Lamentela equità (minaccia RSU) | "4 ore buche, terzo anno, vado in RSU" | bozza | bassa → bozza | ✅ |
| 12 | 🪤 Studente fuori tema da @gmail | "Quando recupero la verifica?" | bozza | bassa → bozza | ✅ * |

\* = corretto dopo il fix al regolamento descritto sotto. I casi 3, 6, 11, 12 sono stati
elaborati con `gemini-2.5-flash-lite` per esaurimento quota giornaliera di
`gemini-3.5-flash`; gli altri con `gemini-3.5-flash`.

## Risposte generate

### Caso 1 — Accesso da @gmail.com → INVIATA IN AUTOMATICO

> **Oggetto:** Re: Richiesta di condivisione per "Orario dal 14-09"
>
> Gentile Mario, i moduli e i file dell'istituto sono accessibili esclusivamente tramite
> account istituzionale. Ti chiediamo di effettuare l'accesso con il tuo account
> @iisgalvanimi.edu.it e riprovare. Per qualsiasi problema con l'account istituzionale,
> rivolgiti alla segreteria. Grazie per la collaborazione.
>
> La Commissione Orario

### Caso 2 — Accesso da altra scuola (@iiscremona.it) → INVIATA IN AUTOMATICO

Stesso template del caso 1, con saluto "Gentile L. Bianchi" (nome ricavato
dall'indirizzo — unica piccola imperfezione).

### Caso 3 — 🪤 Accesso da account istituzionale → BOZZA (da riscrivere)

> Gentile Paola, i moduli e i file dell'istituto sono accessibili esclusivamente tramite
> account istituzionale. Ti chiediamo di effettuare l'accesso con il tuo account
> @iisgalvanimi.edu.it e riprovare. [...]

**Valutazione:** azione corretta (bozza, non inviata), ma il testo proposto è fuori
luogo: il collega sta *già* usando l'account istituzionale, quindi serve una decisione
della commissione sui permessi del file. Prima del fix al regolamento la bozza prometteva
"verificheremo i permessi" (impegno inventato); ora non promette nulla ma resta da
riscrivere. È il motivo per cui questo caso resta in bozza.

### Caso 4 e 5 — Link desiderata / punteggio → INVIATE IN AUTOMATICO

> Gentile Giulia, ecco i link ufficiali per l'a.s. 2026/27:
>
> - Calcolo del punteggio di riferimento: https://forms.gle/5PJDdb6mQ84cN5zZA
> - Espressione dei desiderata: https://forms.gle/pjVnQ3Ua2MgLu5618
> - Regolamento orario approvato dal collegio docenti:
>   https://docs.google.com/document/d/1SlhdlrXC3aqRu6ZqAIAD_2rV1lVVFVWK/edit
>
> I moduli saranno attivi fino al 15 luglio 2026. Per accedere è necessario utilizzare
> esclusivamente l'account istituzionale @iisgalvanimi.edu.it: in caso di "accesso
> negato", verifica di non essere collegato con un account Google personale. Grazie per
> la collaborazione.
>
> La Commissione Orario

**Nota:** viene usato il link punteggio *corretto* (`5PJDdb...`), non quello errato
della prima mail del 25/6 poi rettificata.

### Caso 6 — Domanda crediti (2 figli, 60 min di viaggio) → BOZZA (da ricontrollare)

> Gentile Anna Riva,
>
> in merito alla sua richiesta sul credito orario, le informazioni relative al calcolo e
> ai criteri di attribuzione sono dettagliate nel regolamento ufficiale consultabile al
> seguente link: https://docs.google.com/document/d/1SlhdlrXC3aqRu6ZqAIAD_2rV1lVVFVWK/edit
>
> Le ricordiamo che ogni docente full time parte da un credito base di 2 ore,
> incrementabile in base a diversi fattori tra cui la presenza di figli minori e la
> distanza casa-scuola.
>
> Per una verifica puntuale del suo punteggio e per l'espressione dei desiderata, le
> consigliamo di utilizzare il modulo dedicato: https://forms.gle/5PJDdb6mQ84cN5zZA
>
> La Commissione Orario.

**Valutazione:** prudente e corretta — non calcola il totale (che spetta al form) ma
indirizza agli strumenti giusti. Quasi pronta all'invio.

### Caso 7 — Part-time (12 ore) → BOZZA (da ricontrollare)

> Gentile Sara, in base al regolamento orario ufficiale per l'a.s. 2026/27, per il
> personale in part-time sono previste due opzioni alternative:
>
> - Puoi scegliere il giorno libero, ma senza esprimere altri desiderata;
> - OPPURE puoi formulare un orario su desiderata con un punteggio di -1, rinunciando
>   alla scelta del giorno libero.
>
> Per tutti i dettagli ti invitiamo a consultare il regolamento completo approvato dal
> collegio docenti al seguente link:
> https://docs.google.com/document/d/1SlhdlrXC3aqRu6ZqAIAD_2rV1lVVFVWK/edit
>
> Rimaniamo a disposizione per eventuali chiarimenti.
>
> Un cordiale saluto,
> La Commissione Orario

**Valutazione:** risposta fedele al regolamento, quasi pronta all'invio.

### Caso 8 — Segnalazione errore orario → BOZZA (da ricontrollare)

> Gentile Luca, grazie per la segnalazione. Verifichiamo e provvediamo a correggere
> l'orario al più presto.
>
> La Commissione Orario.

**Valutazione:** in linea con lo stile delle vostre risposte reali; resta in bozza
perché la correzione dell'orario va fatta a mano.

### Caso 9 — Richiesta cambio orario → BOZZA (da ricontrollare)

> Gentile Elena,
>
> grazie per la tua segnalazione. Valuteremo la fattibilità dello spostamento della tua
> prima ora del lunedì al pomeriggio del mercoledì. Faremo il possibile per venirti
> incontro, ma ti ricordiamo che le esigenze didattiche hanno sempre la priorità e non
> possiamo garantire che la modifica sia realizzabile.
>
> Cordiali saluti,
> La Commissione Orario

**Valutazione:** riprende il tono usato nelle risposte reali ("faremo il possibile…
non possiamo garantire"). Quasi pronta.

### Caso 10 — Salute grave con certificato → BOZZA (da ricontrollare)

> Gentile Marco, ci dispiace per la situazione e ti auguriamo una pronta guarigione. In
> merito alla tua richiesta, ti informiamo che, come previsto dal regolamento orario
> ufficiale, in caso di gravi problemi di salute o personali l'orario deve essere
> concordato direttamente con la Dirigenza. Ti invitiamo pertanto a rivolgerti alla
> Dirigenza per presentare la tua richiesta e il relativo certificato. [...] Un cordiale
> saluto, La Commissione Orario.

**Valutazione:** indirizza correttamente alla Dirigenza come da regolamento, tono
empatico. Da ricontrollare per la delicatezza del tema, ma ben impostata.

### Caso 11 — Lamentela su equità con minaccia RSU → BOZZA (da riscrivere)

> Gentile collega Greco,
>
> grazie per averci contattato in merito alla sua segnalazione sull'orario.
>
> Prendiamo nota della sua richiesta e delle sue osservazioni riguardo alle ore buche.
> Cerchiamo sempre di ottimizzare l'orario tenendo conto delle esigenze didattiche e,
> per quanto possibile, di quelle personali dei colleghi. [...] La informiamo tuttavia
> che i desiderata non sono certezze e possono essere disattesi in tutto o in parte.
>
> Cordiali saluti,
> La Commissione Orario

**Valutazione:** diplomatica ma generica; una situazione conflittuale con minaccia di
ricorso alla RSU va gestita personalmente dalla commissione. Correttamente in bozza.

### Caso 12 — 🪤 Studente fuori tema da @gmail.com → BOZZA (da scrivere ex novo)

Categoria assegnata: "richiesta studente esterna", confidenza bassa, **testo vuoto**:
il modello non inventa una risposta e lascia alla commissione la stesura. Comportamento
sicuro; nota: in Gmail comparirà una bozza con corpo vuoto.

## Problemi trovati e sistemati durante il test

1. **Bug sventato (falso positivo Regola 1).** Nella prima esecuzione la mail dello
   studente da @gmail.com riceveva **in automatico** il template "usa l'account
   istituzionale": il modello applicava la Regola 1 sul solo mittente non istituzionale.
   Fix in `regolamento.md`: controesempio esplicito nella Regola 1 ("il mittente non
   istituzionale da solo NON basta") e regola generale "invio automatico SOLO per Regole
   1 e 4, nel dubbio bozza". Dopo il fix il caso finisce correttamente in bozza.
2. **Bozze con promesse inventate.** Il caso 3 generava "provvederemo a verificare i
   permessi": aggiunta alla regola generale il divieto di promettere azioni specifiche
   non previste dalle regole.
3. **Venv non allineato.** Mancava il nuovo SDK `google-genai` richiesto da
   `requirements.txt` (la migrazione SDK era nel codice ma non nel venv): installato.

## ⚠️ Quota Gemini — rischio in produzione

Il free tier di `gemini-3.5-flash` (modello impostato in `.env.local.sh`) ha un limite di
**20 richieste al giorno per progetto**, esaurito a metà test
(`GenerateRequestsPerDayPerProjectPerModel-FreeTier, limit: 20`). Con il workflow ogni
3 ore e giornate di posta intensa (a settembre 2025: 15+ richieste di accesso in un
giorno) il limite può bloccare l'elaborazione in produzione.

**Raccomandazione:** impostare la repository variable `GEMINI_MODEL` su
`gemini-2.5-flash-lite` (quota giornaliera molto più ampia, qualità risultata equivalente
in questi test), oppure attivare il billing sul progetto Google AI.

## Promemoria per il futuro

- I link ai form cambiano ogni anno: a giugno 2027 aggiornare la **Regola 4** di
  `regolamento.md` (nuovi link e nuova scadenza). Dopo il 15 luglio 2026 la risposta
  automatica della Regola 4 citerà moduli chiusi.
- L'"Allegato 1" del regolamento ufficiale (tabella dei pesi) non è estraibile come
  testo dal Google Doc: per domande sui costi precisi dei desiderata l'AI rimanda al
  documento completo.
