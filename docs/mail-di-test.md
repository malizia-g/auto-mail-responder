# Mail di test per il risponditore automatico

> Invia queste mail **all'indirizzo monitorato** dal risponditore
> (la casella su cui gira lo script, es. `commissione.orario@iisgalvanimi.edu.it`).
> Se il filtro Gmail è attivo, verranno etichettate da sole come **DaRispondere**;
> altrimenti applica l'etichetta a mano prima di far girare lo script.
>
> **Consiglio:** manda le mail "invio automatico" (① e ②) da un indirizzo **non tuo**
> (es. un `@gmail.com`), così vedi davvero arrivare la risposta.
> Per un primo giro sicuro, fai girare lo script con `DRY_RUN=true` (vedi il log senza
> inviare nulla), poi rilancia con `DRY_RUN=false` per confermare ① e ②.

## Riepilogo comportamento atteso

| Test | Cosa verifica | Confidenza | Azione | Etichette finali |
|------|---------------|-----------|--------|------------------|
| ① | Regola 1 – accesso non istituzionale | alta | **invia automatico** | Elaborata + Risposta da AI |
| ② | Regola 4 – link desiderata/punteggio | alta | **invia automatico** | Elaborata + Risposta da AI |
| ③ | Regola 2 – errore/refuso orario | media | bozza | Elaborata + Da controllare a livello 2 |
| ④ | Regola 3 – modifica/cambio orario | bassa | bozza | Elaborata + Da controllare a livello 2 |
| ⑤ | Regola 5 – regolamento (crediti) | media | bozza | Elaborata + Da controllare a livello 2 |
| ⑥ | Trappola: gmail ma NON parla di accesso | bassa | bozza | Elaborata + Da controllare a livello 2 |
| ⑦ | Fallback: mail fuori tema | bassa | bozza | Elaborata + Da controllare a livello 2 |

---

## ① Regola 1 — accesso con account non istituzionale → ✅ INVIO AUTOMATICO

Inviare da un indirizzo **`@gmail.com`** (o altro dominio esterno).

- **Oggetto:** `Richiesta di accesso al modulo desiderata`
- **Corpo:**

```
Buongiorno,
ho provato ad aprire il modulo dei desiderata ma mi dice accesso negato.
Potete condividermelo? Grazie,
Marco
```

---

## ② Regola 4 — richiesta link desiderata/punteggio → ✅ INVIO AUTOMATICO

Inviare da un indirizzo **`@iisgalvanimi.edu.it`**.

- **Oggetto:** `Link desiderata e calcolo punteggio`
- **Corpo:**

```
Ciao,
dove trovo il modulo per esprimere i desiderata e come calcolo il mio punteggio orario?
Grazie
```

---

## ③ Regola 2 — segnalazione errore/refuso orario → 📝 BOZZA (media)

- **Oggetto:** `Errore orario 3B mercoledì`
- **Corpo:**

```
Buongiorno,
nell'orario pubblicato manca la mia ora di mercoledì in 3B, c'è una
sovrapposizione con Matematica. Potete verificare?
```

---

## ④ Regola 3 — richiesta modifica/cambio orario → 📝 BOZZA (bassa)

- **Oggetto:** `Cambio giorno libero`
- **Corpo:**

```
Ciao,
sarebbe possibile spostare il mio giorno libero dal lunedì al venerdì
per motivi familiari? Grazie
```

---

## ⑤ Regola 5 — domanda sul regolamento (crediti) → 📝 BOZZA (media)

- **Oggetto:** `Domanda sul credito orario`
- **Corpo:**

```
Buongiorno,
ho la Legge 104 e due figli piccoli: quanti crediti orari mi spettano
in totale? Grazie
```

---

## ⑥ Trappola per la Regola 1 — mittente esterno ma NON parla di accesso → 📝 BOZZA (bassa)

Inviare da un indirizzo **`@gmail.com`**. Serve a verificare che il sistema **non** invii
in automatico solo perché il mittente è esterno.

- **Oggetto:** `Domanda sulla verifica di matematica`
- **Corpo:**

```
Salve prof,
quando riconsegnate la verifica di matematica? Volevo sapere il voto.
Grazie, uno studente
```

---

## ⑦ Fallback generale — mail fuori tema → 📝 BOZZA (bassa)

- **Oggetto:** `Offerta fotocopiatrici per la scuola`
- **Corpo:**

```
Buongiorno,
siamo un fornitore di stampanti multifunzione e vorremmo proporvi
un'offerta dedicata agli istituti scolastici...
```
