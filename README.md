[# Crystal Oscillator Validator

**Versione:** 3.4  
**Autore:** Samuele Lorenzoni

---

## Descrizione

Questo strumento software è progettato per ingegneri e progettisti elettronici al fine di verificare e dimensionare circuiti oscillatori a topologia Pierce, comunemente impiegati con microcontrollori e altri dispositivi digitali.

A partire dalle specifiche del cristallo di quarzo e dai parametri del circuito, l'applicazione calcola i parametri operativi chiave (capacità di carico effettiva, transconduttanza critica, margine di guadagno, drive level) e fornisce una valutazione immediata sulla robustezza e l'affidabilità del design.

---

## Caratteristiche Principali

* **Analisi Completa**: Calcolo dei principali indicatori di performance di un oscillatore Pierce.
* **Preset di Componenti**: Database integrato di quarzi (es. ECS, Abracon, MicroCrystal) e sonde di misura (es. LeCroy, Tektronix) per accelerare l'inserimento dei dati.
* **Salvataggio e Caricamento Sessioni**: Possibilità di salvare tutti i parametri di input in un file locale (`.xtal`) e ricaricarli in un secondo momento per continuare il lavoro.
* **Interfaccia Intuitiva**: GUI progettata per un inserimento dati efficiente, con gestione automatica delle unità di misura.
* **Validazione Immediata**: Report finale con indicazioni cromatiche (OK, Attenzione, Critico) per una rapida interpretazione dei risultati.
* **Architettura Modulare (MVC)**: Motore di calcolo disaccoppiato dall'interfaccia utente per garantire manutenibilità e scalabilità.

---

## Preset e Analisi Worst-Case

Lo strumento include un database di preset per quarzi di uso comune. Questa funzionalità permette di caricare automaticamente i parametri di datasheet del componente selezionato.

Per i preset che si riferiscono a una *serie* di componenti (es. Abracon IXA20), i valori caricati sono rappresentativi di un caso d'uso comune (es. 24 MHz) e utilizzano le specifiche **worst-case** (es. ESR massimo) indicate dal produttore. Questo approccio garantisce che la validazione del circuito sia conservativa e robusta, coprendo le condizioni operative più critiche.

---

## Modello Teorico di Riferimento

L'analisi si basa sul modello elettrico equivalente del risonatore a quarzo e sulle condizioni di Barkhausen per l'innesco dell'oscillazione, in accordo con le principali application note di settore (es. AN2867 di STMicroelectronics).

### 1. Capacità di Carico Effettiva ($C_{L_{eff}}$)

È la capacità totale vista ai capi del cristallo. Assumendo un layout simmetrico, è calcolata come la serie dei due rami capacitivi del circuito:

C_stray_single_leg = CS_PCB + CS_PIN
CL_eff = (CL_sel + C_stray_single_leg) / 2.0


* `CL_sel`: Capacità del singolo condensatore di carico esterno.
* `CS_PCB`: Capacità parassita del PCB per un singolo ramo.
* `CS_PIN`: Capacità parassita del pin del MCU per un singolo ramo.

### 2. Transconduttanza Critica e Margine di Guadagno

Per garantire l'innesco dell'oscillazione, la transconduttanza ($g_m$) dell'amplificatore del MCU deve superare un valore critico ($g_{m_{crit}}$):

gm_crit = 4 * (ESR_max + R_ext) * (2 * pi * f)^2 * (C0 + CL_eff)^2


Il **Margine di Guadagno** (Gain Margin) quantifica la robustezza dell'innesco:

GainMargin = gm / gm_crit


Un valore `GainMargin > 5` è raccomandato per un design robusto.

### 3. Drive Level (DL)

Rappresenta la potenza dissipata dal cristallo. Un valore eccessivo può danneggiarlo. Viene stimato misurando la tensione picco-picco ($V_{pp}$) su un ramo del circuito:

C_leg_for_dl = CL_sel + CS_PCB + CS_PIN + C_probe
DL = ((ESR_max + R_ext) / 2.0) * (pi * f * C_leg_for_dl * Vpp)^2

* `C_probe`: Capacità di ingresso della sonda utilizzata per la misura.

---

## Architettura Software

L'applicazione adotta il design pattern **Model-View-Controller (MVC)**:

* **Model (`CrystalCircuitModel`)**: Implementa il motore di calcolo e le formule teoriche.
* **View (`MainView`)**: Gestisce l'intera interfaccia utente (widget, layout, stili).
* **Controller (`AppController`)**: Funge da orchestratore, coordinando il flusso di dati tra Model e View.

---

## Requisiti e Installazione

* **Python**: Versione 3.7 o superiore.
* **Dipendenze**: `numpy`

Installare la dipendenza necessaria tramite pip:
```bash
pip install numpy
](https://github.com/samuelorenz/Crystal-Calculator)
