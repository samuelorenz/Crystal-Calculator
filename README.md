# Validatore per Circuiti Oscillatori a Cristallo di Quarzo

## Descrizione
Questo strumento software aiuta a verificare e dimensionare circuiti oscillatori a topologia Pierce (tipicamente usati con microcontrollori). Calcola parametri chiave (capacità di carico effettiva, transconduttanza critica, margine di guadagno, drive level) a partire dalle specifiche del cristallo e dai componenti esterni, fornendo indicazioni di robustezza del progetto.

Versione applicazione: 2.5

---

## Caratteristiche principali
- Calcolo della capacità di carico effettiva vista dal cristallo.
- Valutazione della transconduttanza critica richiesta (gm_crit).
- Determinazione del Margine di Guadagno (Gain Margin).
- Stima del Drive Level (DL) e confronto con i limiti del costruttore.
- Architettura modulare (MVC): motore di calcolo indipendente dall'interfaccia.

---

## Modello teorico di riferimento

L'analisi si basa sul modello elettrico equivalente del risonatore a cristallo e sulle condizioni di Barkhausen per l'innesco dell'oscillazione.

### 1) Capacità di carico effettiva (CL_eff)
La capacità di carico effettiva vista dal cristallo, assumendo un layout simmetrico (CL1 = CL2 = CL_sel), è calcolata come:

CL_eff = (CL_sel / 2) + 2 * (CS_PCB + CS_PIN)

Dove:
- CL_sel: capacità selezionata per singolo condensatore di carico (per ramo).
- CS_PCB: capacità parassita del PCB per singolo ramo.
- CS_PIN: capacità parassita del pin per singolo ramo.

Questa CL_eff determina la frequenza effettiva di oscillazione del risonatore in circuito parallelo.

### 2) Transconduttanza critica e Margine di Guadagno
Per garantire l'innesco e il mantenimento dell'oscillazione, la transconduttanza efficace dell'amplificatore invertente (gm) deve essere superiore a una transconduttanza critica gm_crit, data da:

gm_crit = 4 * (ESR_max + R_ext) * (2 * π * f)^2 * (C0 + CL_eff)^2

Dove:
- ESR_max: resistenza equivalente serie massima del cristallo.
- R_ext: resistenza esterna nella rete.
- f: frequenza di oscillazione (Hz).
- C0: capacità parallela intrinseca del cristallo.
- CL_eff: capacità di carico effettiva.

Definiamo quindi il Margine di Guadagno (Gain Margin) come rapporto adimensionale:
GainMargin = gm / gm_crit

Indicazione pratica:
- GainMargin > 5 → progetto robusto rispetto a tolleranze e variazioni operative.

### 3) Drive Level (DL)
Il Drive Level rappresenta la potenza dissipata dal cristallo durante l'oscillazione. Un valore eccessivo accelera l'invecchiamento o danneggia il cristallo. Stimiamo la capacità totale sul ramo di misura:

C_leg = CL_sel + CS_PCB + CS_PIN + C_probe

E il Drive Level in funzione di Vpp misurata sul pin e della capacità del ramo:

DL = ((ESR_max + R_ext) / 2) * (π * f * C_leg * Vpp)^2

Il valore calcolato deve risultare inferiore al DL massimo indicato dal produttore del cristallo.

---

## Architettura software
L'applicazione segue il pattern Model-View-Controller (MVC):

- Model (CrystalCircuitModel): implementa il motore di calcolo e le formule teoriche; è indipendente dall'interfaccia.
- View (MainView): gestisce l'interfaccia utente (widget, visualizzazioni).
- Controller (AppController): coordina il flusso tra Model e View, gestisce eventi e validazioni.

Questa separazione facilita test, manutenzione ed estensione delle funzionalità (es. aggiunta di formati di input/output o di nuove analisi).

---

## Requisiti di sistema e installazione
- Python 3.7 o superiore
- Dipendenze Python:
  - numpy

Installazione di numpy:
```bash
pip install numpy
```

---

## Esecuzione
Dalla directory contenente lo script principale:

```bash
python xtal_validator_app.py
```

Assicurarsi che le dipendenze siano state installate e che si stiano usando i valori corretti per le unità (Hz, Farad, Ohm, Vpp).

---

## Raccomandazioni pratiche
- Verificare sempre le capacità parassite (CS_PCB, CS_PIN) misurate o stimate in fase di layout: possono impattare significativamente la frequenza e il drive level.
- Tenere conto delle tolleranze dei componenti e delle variazioni ambientali (temperatura, alimentazione).
- Considerare un margine di sicurezza sul Gain Margin (es. > 5) per aumentare la robustezza del progetto.
- Confrontare il DL calcolato con la specifica del produttore e non superare il DL massimo raccomandato.

---

## Riferimenti
- AN2867 — Oscillator design guide for STM8AF/AL/S, STM32 MCUs and MPUs (STMicroelectronics)
- SLLA549 — TCAN455x Clock Optimization and Design Guidelines (Texas Instruments)

---

Se vuoi, posso:
- tradurre il README in inglese,
- aggiungere esempi numerici o casi di prova,
- preparare un file di esempio con valori tipici per testare il calcolo.
