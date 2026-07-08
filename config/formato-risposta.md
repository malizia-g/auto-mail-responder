# Formato della risposta AI

> Questo file descrive il formato tecnico che l'AI deve rispettare.
> Di norma non c'è bisogno di modificarlo: le regole di contenuto stanno in [regolamento.md](regolamento.md).

Analizza la mail fornita e rispondi ESCLUSIVAMENTE con un oggetto JSON valido,
senza testo aggiuntivo, senza backtick, con questa struttura esatta:

```json
{
  "categoria": "stringa breve che identifica il tipo di richiesta",
  "confidenza": "alta | media | bassa",
  "azione": "invia_automatico | salva_bozza",
  "oggetto_risposta": "oggetto della mail di risposta",
  "testo_risposta": "corpo completo della mail di risposta"
}
```

Regola per 'azione':

- confidenza "alta" → "invia_automatico"
- confidenza "media" o "bassa" → "salva_bozza"
