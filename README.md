Validatore di Circuiti Oscillatori a Cristallo di Quarzo
1. Abstract
Questo applicativo software costituisce uno strumento di validazione per circuiti oscillatori a topologia Pierce-gate, ampiamente impiegati in sistemi a microcontrollore. Il software modella il comportamento del circuito basandosi su parametri circuitali e del risonatore, forniti dall'utente, al fine di quantificare metriche di performance critiche. L'obiettivo primario è automatizzare il processo di verifica del design, assicurando il rispetto delle condizioni di innesco dell'oscillazione e prevenendo il sovrapilotaggio (overdriving) del cristallo, in accordo con le metodologie definite in application note di riferimento del settore, quale la AN2867 di STMicroelectronics.

2. Modello Teorico di Riferimento
L'analisi si fonda sul modello elettrico equivalente di un risonatore a cristallo di quarzo e sulle condizioni di Barkhausen per l'oscillazione.

2.1 Capacità di Carico Effettiva (C 
L 
eff
​
 
​
 )
La frequenza di oscillazione di un risonatore in un circuito parallelo è determinata dalla capacità di carico effettiva vista ai suoi terminali. Questa è data dalla combinazione serie dei condensatori di carico esterni (C 
L1
​
 ,C 
L2
​
 ) e dal contributo delle capacità parassite totali (C 
S 
tot
​
 
​
 ). Assumendo un layout simmetrico (C 
L1
​
 =C 
L2
​
 =C 
L 
sel
​
 
​
 ), la formula implementata è:

CL_eff = (CL_sel / 2) + 2 * (CS_PCB + CS_PIN)

dove C 
S 
PCB
​
 
​
  e C 
S 
PIN
​
 
​
  rappresentano le capacità parassite per singolo ramo del circuito.

2.2 Condizione di Innesco e Margine di Guadagno
L'innesco e il mantenimento dell'oscillazione richiedono che il guadagno di anello sia maggiore di uno e che la fase totale sia un multiplo di 360°. Questo si traduce nella necessità che la transconduttanza (g 
m
​
 ) dell'amplificatore invertente del MCU superi una soglia critica, definita transconduttanza critica (g 
m 
crit
​
 
​
 ):

gm_crit = 4 * (ESR_max + R_ext) * (2 * pi * f)^2 * (C0 + CL_eff)^2

Per garantire robustezza rispetto a variazioni di temperatura, tensione e tolleranze dei componenti, si definisce il Margine di Guadagno (Gain Margin) come il rapporto adimensionale:

GainMargin = gm / gm_crit

Un valore di Gain Margin > 5 è considerato indice di un design robusto.

2.3 Livello di Pilotaggio (Drive Level - DL)
Il Drive Level rappresenta la potenza dissipata dal cristallo durante l'oscillazione. Un DL eccessivo può causare un invecchiamento precoce, una deviazione in frequenza o il danneggiamento fisico del risonatore. Il calcolo viene effettuato a partire dalla tensione picco-picco (V 
pp
​
 ) misurata su un pin dell'oscillatore e dalla capacità totale su quel ramo (C 
leg
​
 ):

C_leg = CL_sel + CS_PCB + CS_PIN + C_probe

DL = ((ESR_max + R_ext) / 2) * (pi * f * C_leg * Vpp)^2

Il valore calcolato deve essere inferiore al DL massimo specificato dal costruttore del cristallo.

3. Architettura Software
L'applicazione è strutturata secondo il design pattern Model-View-Controller (MVC):

Model (CrystalCircuitModel): Contiene il motore di calcolo, implementando le formule del modello teorico. È agnostico rispetto all'interfaccia.

View (MainView): Gestisce la resa grafica di tutti i widget dell'interfaccia utente (GUI).

Controller (AppController): Orchestra il flusso di dati tra il Model e la View, gestendo gli eventi dell'utente e la logica applicativa.

4. Requisiti di Sistema e Installazione
Interprete Python: Versione 3.7 o superiore.

Librerie Esterne: NumPy per le operazioni numeriche.

Installazione della dipendenza tramite pip:

pip install numpy

5. Guida all'Esecuzione
Posizionarsi via terminale nella directory contenente lo script.

Assicurarsi che le dipendenze siano installate.

Lanciare l'eseguibile Python:

python xtal_validator_app.py

6. Riferimenti Bibliografici
AN2867: Oscillator design guide for STM8AF/AL/S, STM32 MCUs and MPUs. STMicroelectronics.

SLLA549: TCAN455x Clock Optimization and Design Guidelines. Texas Instruments.

Versione applicazione: 2.5
