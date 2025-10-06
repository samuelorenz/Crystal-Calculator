# Crystal Oscillator Validator: A Technical Reference

**Versione Software:** 5.0
**Autore:** Samuele Lorenzoni

---

## 1. Abstract

La progettazione di oscillatori a cristallo di quarzo, in particolare nella topologia Pierce, è un'attività critica nell'elettronica digitale. Un design non robusto può causare instabilità di frequenza, mancati avvii o danni permanenti al risuonatore, con conseguenze gravi sull'affidabilità del prodotto finale. Questo documento descrive il **Crystal Oscillator Validator**, un'applicazione software sviluppata per assistere i progettisti nella validazione sistematica e quantitativa di tali circuiti. Lo strumento implementa un modello matematico basato su note applicative standard del settore per calcolare parametri chiave come il **Margine di Guadagno** e il **Drive Level**. Attraverso un'interfaccia grafica interattiva, il software fornisce una valutazione oggettiva del design, evidenziando criticità e aree di miglioramento. Vengono inoltre discusse le funzionalità di gestione di una libreria di componenti e di salvataggio delle sessioni di analisi, che rendono lo strumento un ausilio completo per la progettazione e l'archiviazione della documentazione tecnica.

---

## 2. Novità della Versione 5.0: Interfaccia "Scientific Paper" e Validazione Chiara

Questa versione introduce un'importante revisione estetica e funzionale per migliorare l'esperienza utente e la chiarezza dei risultati.

### 2.1. Estetica "Scientific Paper"

L'interfaccia è stata ridisegnata per assomigliare a un'applicazione scientifica o a uno strumento di laboratorio, con un'estetica più pulita, professionale e accademica.
- **Caratteri**: L'intera applicazione ora utilizza il font **Times New Roman**, un classico della documentazione tecnica. Le formule matematiche sono rese in **Courier New** per una migliore leggibilità.
- **Palette Colori**: È stata adottata una palette di colori neutra, dominata da bianco, nero e grigi, che migliora la concentrazione sui dati. Un **rosso scuro accademico** è usato come colore d'accento per evidenziare le azioni principali e gli avvisi critici, sostituendo i precedenti blu e verdi.
- **Stile dei Widget**: Il tema grafico è stato aggiornato per un aspetto più tradizionale e meno invasivo, favorendo la funzionalità rispetto all'estetica decorativa.

### 2.2. Risultato Finale "PASS / FAIL"

Per rendere la valutazione del design inequivocabile, è stato introdotto un indicatore di stato finale ben visibile.
- **VALIDATION: PASS**: Visualizzato in verde scuro, indica che tutti i parametri calcolati (avvio, margine, drive level) rientrano nei limiti di sicurezza o accettabilità.
- **VALIDATION: FAIL**: Visualizzato in rosso scuro, indica che almeno uno dei parametri si trova in uno stato "CRITICO", segnalando che il design non è robusto e richiede modifiche immediate.

Questo verdetto finale sintetizza l'analisi complessa in una risposta chiara e diretta.

---

## 3. Installazione

Per eseguire il Crystal Oscillator Validator, è necessario avere installato Python 3.

1.  **Clonare o scaricare il repository.**

2.  **Creare e attivare un ambiente virtuale (consigliato):**
    ```bash
    # Creare l'ambiente
    python -m venv .venv

    # Attivare su Windows
    .venv\Scripts\activate

    # Attivare su macOS/Linux
    source .venv/bin/activate
    ```

3.  **Installare la dipendenza necessaria:**
    Una volta attivato l'ambiente virtuale, installare la libreria `numpy`.
    ```bash
    pip install numpy
    ```

4.  **Eseguire il programma:**
    ```bash
    python main.py
    ```

---

## 4. Contesto Teorico: L'Oscillatore Pierce

L'applicazione si focalizza sulla validazione di oscillatori a cristallo basati sulla topologia **Pierce**, la più diffusa in ambito di microcontrollori (MCU) per la sua stabilità, semplicità ed efficienza. Un oscillatore Pierce è costituito da un amplificatore invertente (tipicamente una porta logica CMOS interna all'MCU) e una rete di feedback a π (pi-greco) formata dal cristallo di quarzo e due condensatori di carico esterni (CL1, CL2).

- **Il Cristallo come Risuonatore**: Il cristallo di quarzo opera come un elemento risonante ad altissimo fattore di merito (Q). Il suo comportamento elettrico è descritto dal modello di BVD (Butterworth-Van Dyke), che include una capacità statica `C0` (shunt) e un ramo serie RLC (`R1`, `L1`, `C1`). Ai fini di questo strumento, i parametri fondamentali forniti dal datasheet sono la **Frequenza Nominale (F)**, la **Resistenza Serie Equivalente (ESR o R1)**, la **Capacità di Shunt (C0)** e il **Massimo Drive Level (DL_max)**.

- **Condizione di Oscillazione**: Per un'oscillazione stabile, il circuito deve soddisfare il **criterio di Barkhausen**: il guadagno totale di anello deve essere maggiore di 1 e lo sfasamento totale deve essere di 360°. L'amplificatore invertente fornisce 180°, mentre la rete a π deve fornire gli altri 180° e compensare le perdite energetiche introdotte dal cristallo (rappresentate dalla sua ESR).

---

## 5. Modello Matematico e Implementazione

Le analisi eseguite dal software si basano sulle formule e le metodologie descritte in documenti di riferimento come la nota applicativa **AN2867 di STMicroelectronics**. Di seguito vengono dettagliate le formule implementate.

### 5.1. Capacità di Carico Effettiva (CL_eff)

- **Formula:**
  ```
  C_stray = Cs_PCB + Cs_PIN
  CL_eff = (CL_sel + C_stray) / 2
  ```
- **Variabili:**
  - `CL_sel`: Capacità del singolo condensatore di carico esterno (assumendo CL1 = CL2).
  - `Cs_PCB`: Capacità parassita dovuta alle piste del circuito stampato (PCB).
  - `Cs_PIN`: Capacità parassita intrinseca del pin di I/O dell'MCU.
  - `C_stray`: Capacità parassita totale su un singolo ramo dell'oscillatore.
- **Interpretazione Fisica:** `CL_eff` rappresenta la capacità totale vista dal cristallo guardando verso la rete di carico. Il suo valore influenza direttamente la frequenza di oscillazione e la stabilità. La formula deriva dalla serie dei due rami capacitivi (ciascuno composto da `CL_sel` in parallelo con `C_stray`).

### 5.2. Transconduttanza Critica (Gm_crit)

- **Formula:**
  ```
  Total_ESR = ESR_max + Rext_sel
  Gm_crit = 4 * Total_ESR * (2 * pi * F)^2 * (C0 + CL_eff)^2
  ```
- **Variabili:**
  - `ESR_max`: Massima Resistenza Serie Equivalente del cristallo (dal datasheet).
  - `Rext_sel`: Valore della resistenza esterna opzionale, usata per limitare il Drive Level.
  - `F`: Frequenza di risonanza nominale del cristallo.
  - `C0`: Capacità di shunt del cristallo (dal datasheet).
- **Interpretazione Fisica:** `Gm_crit` è la **transconduttanza minima** che l'amplificatore interno all'MCU deve possedere per innescare e sostenere l'oscillazione. Essa deve essere sufficiente a compensare le perdite introdotte dalla `Total_ESR` alla frequenza di lavoro. Se la transconduttanza dell'MCU (`Gm_MCU`) è inferiore a questo valore, l'oscillatore non partirà.

### 5.3. Margine di Guadagno (Gain Margin, S_f)

- **Formula:**
  ```
  Gain_Margin = Gm_MCU / Gm_crit
  ```
- **Variabili:**
  - `Gm_MCU`: Transconduttanza dell'amplificatore dell'MCU (dal datasheet del microcontrollore).
- **Interpretazione Fisica:** Il Margine di Guadagno, noto anche come *Safety Factor* (S_f), è un indicatore adimensionale della **robustezza dell'oscillatore**. Indica di quanto il guadagno dell'amplificatore supera il minimo necessario. Un margine elevato garantisce un avvio rapido e affidabile in un ampio range di temperature, tensioni di alimentazione e variazioni di processo (sia del cristallo che dell'MCU).

### 5.4. Drive Level (DL)

- **Formula:**
  ```
  C_leg_total = CL_sel + C_stray + C_probe
  DL = (Total_ESR / 2) * (pi * F * C_leg_total)^2 * Vpp_measured^2
  ```
- **Variabili:**
  - `C_probe`: Capacità della sonda dell'oscilloscopio usata per la misurazione.
  - `Vpp_measured`: Tensione picco-picco misurata sul pin di output dell'oscillatore (solitamente OSC_IN/CL1).
- **Interpretazione Fisica:** Il Drive Level è la **potenza dissipata dal cristallo** durante l'oscillazione. Un pilotaggio eccessivo (overdrive) può causare un invecchiamento precoce, una deriva in frequenza o un danno fisico permanente al quarzo. Questa formula calcola la potenza basandosi sulla corrente che scorre attraverso il ramo capacitivo misurato. È fondamentale includere `C_probe`, poiché la sonda altera il comportamento del circuito e la tensione misurata.

---

## 6. Motore di Validazione: Criteri e Soglie

Il software automatizza la valutazione del design confrontando i risultati calcolati con soglie raccomandate dall'industria.

- **Criterio 1: Avvio dell'Oscillazione**
  - **Controllo**: `Gm_MCU > Gm_crit`
  - **Logica**: Se la transconduttanza del dispositivo attivo non supera quella critica, l'oscillazione non può essere sostenuta.
  - **Stati**: `CRITICO` (se `Gm_MCU < Gm_crit`), `OK` (se `Gm_MCU > Gm_crit`).

- **Criterio 2: Robustezza del Design (Gain Margin)**
  - **Controllo**: Valore di `Gain_Margin`.
  - **Logica**: Un margine di guadagno elevato è necessario per compensare le variazioni dei componenti e le derive ambientali.
  - **Stati e Soglie**: 
    - `ECCELLENTE` (`Gain_Margin ≥ 5`): Raccomandato dalla maggior parte dei produttori per design commerciali.
    - `OTTIMIZZARE` (`3 ≤ Gain_Margin < 5`): Funzionante in condizioni nominali, ma a rischio ai limiti di temperatura/tensione.
    - `CRITICO` (`Gain_Margin < 3`): Design inaffidabile, con alto rischio di mancato avvio.

- **Criterio 3: Affidabilità e Vita Utile (Drive Level)**
  - **Controllo**: Rapporto `DL / DL_max`.
  - **Logica**: Il superamento del `DL_max` specificato dal produttore del cristallo ne compromette l'integrità.
  - **Stati e Soglie**:
    - `OK` (`DL / DL_max ≤ 0.8`): Il cristallo opera in un'area di totale sicurezza.
    - `ATTENZIONE` (`0.8 < DL / DL_max ≤ 1.0`): Il design è al limite. Si raccomanda di considerare una resistenza `Rext` per ridurre la potenza.
    - `CRITICO` (`DL / DL_max > 1.0`): Overdrive. Il cristallo è a rischio di danneggiamento. L'uso di `Rext` è obbligatorio.

Il software sintetizza questi tre controlli in un **Risultato Finale** univoco, visualizzato in modo prominente nell'interfaccia. Lo stato sarà `VALIDATION: PASS` se nessun criterio è `CRITICO`, o `VALIDATION: FAIL` in caso contrario, fornendo al progettista un verdetto immediato e inequivocabile sulla conformità del design.

---

## 7. Architettura Software e Funzionalità Avanzate

### 7.1. Libreria dei Quarzi Dinamica

Lo strumento gestisce una libreria di componenti persistente, salvata nel file `xtal_library.json` nella directory dell'applicazione. Questo file JSON contiene un dizionario di profili di quarzi, dove ogni profilo memorizza i parametri fondamentali (F, C0, ESR, DL_max).

- **Gestione**: L'utente può aggiungere nuovi componenti alla libreria (`Salva Quarzo`), caricarli per un'analisi (`<Combobox>`) o rimuoverli (`Elimina`).
- **Scopo**: Centralizzare e riutilizzare le specifiche dei componenti approvati o di uso comune, riducendo l'inserimento manuale e gli errori.

### 7.2. Gestione delle Sessioni di Lavoro

È fondamentale distinguere la libreria (dati di *componenti*) dalle sessioni (dati di *analisi*).

- **File di Lavoro (`.xtal`)**: Tramite `File > Salva Lavoro`, l'utente può salvare l'intero stato dell'applicazione in un file `.xtal`. Questo file è un'istantanea JSON che include **tutti i parametri di input**: specifiche del quarzo, parametri del circuito (Gm, CL, parassite) e misurazioni (Vpp, sonda).
- **Scopo**: Archiviare una validazione completa per la documentazione di progetto, confrontare diverse configurazioni circuitali per lo stesso quarzo o riprendere un'analisi interrotta.

### 7.3. Interfaccia Utente e Feedback in Tempo Reale

L'interfaccia è progettata per guidare l'utente e prevenire errori:

- **Stale Data Invalidation**: Se un qualsiasi parametro di input viene modificato, tutti i risultati calcolati vengono immediatamente invalidati (visualizzati come `...` in grigio), forzando l'utente a eseguire un nuovo calcolo per garantire la coerenza dei dati.
- **Input Validation**: I campi di input numerici sono validati in tempo reale. Un input non valido (es. testo) colora il campo di rosso e impedisce il calcolo, mostrando un errore esplicito.
- **Barra di Stato**: Fornisce un log testuale delle azioni eseguite e dello stato corrente, migliorando la consapevolezza dell'utente.

---

## 8. Protocollo Operativo Consigliato

Per una validazione completa e rigorosa, si raccomanda di seguire i seguenti passaggi:

1.  **Raccolta Dati**: Reperire i datasheet del cristallo e dell'MCU. Ottenere i valori di `F`, `C0`, `ESR_max`, `DL_max` per il cristallo e `Gm_MCU`, `Cs_PIN` per l'MCU.
2.  **Stima Parassiti**: Stimare `Cs_PCB` in base al layout o usare un valore conservativo (es. 1-3 pF).
3.  **Configurazione Iniziale**: Inserire tutti i parametri nello strumento. Selezionare il modello di sonda corretto o inserire la sua capacità manualmente.
4.  **Misurazione Sperimentale**: Assemblare il circuito e misurare la tensione `Vpp` sul pin di output dell'oscillatore (es. OSC_IN). Inserire questo valore nel campo `Vpp Misurata`.
5.  **Esecuzione Calcoli**: Premere il pulsante `Esegui Calcoli`.
6.  **Analisi dei Risultati**: Valutare criticamente i tre criteri nel pannello "Stato di Validazione" e il risultato finale "PASS/FAIL".
7.  **Iterazione (se necessario)**: Se il risultato è `FAIL`, modificare il design (es. cambiare i valori di `CL_sel`, aggiungere/modificare `Rext_sel`) e ripetere dal punto 4.
8.  **Archiviazione**: Una volta ottenuto un design robusto (`PASS`), salvare la sessione di lavoro (`File > Salva Lavoro`) per la documentazione di progetto.
