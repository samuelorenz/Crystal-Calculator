Validatore di Circuiti Oscillatori a Quarzo
Versione: 3.1

Autore: Samuele Lorenzoni

🎯 Descrizione
Questo strumento è progettato per assistere ingegneri e progettisti elettronici nella verifica e nel dimensionamento di circuiti oscillatori in configurazione Pierce, tipicamente impiegati con microcontrollori.

Inserendo le specifiche del cristallo di quarzo e i parametri del circuito, l'applicazione calcola i parametri operativi fondamentali per validare il design.

Parametri Calcolati
Capacità di carico effettiva (C 
L 
eff
​
 
​
 )

Transconduttanza critica (g 
m 
crit
​
 
​
 ) e margine di guadagno

Drive Level (potenza dissipata dal cristallo)

Il risultato finale è un report con indicazioni chiare e intuitive (OK, Attenzione, Critico) per valutare la robustezza e l'affidabilità del progetto.

✨ Caratteristiche Principali
Analisi completa dei parametri di un oscillatore Pierce.

Database di preset per quarzi e sonde di misura, per un inserimento rapido dei dati.

Interfaccia grafica semplice con gestione automatica delle unità di misura.

Report finale con una valutazione qualitativa immediata dei risultati.

Architettura modulare basata sul pattern MVC, che garantisce facilità di manutenzione ed estensione.

🛠️ Preset e Analisi Worst-Case
Il software include una serie di preset per cristalli di quarzo di uso comune. Per componenti di una stessa serie (es. Abracon IXA20), i preset utilizzano valori tipici. Per analisi più rigorose e restrittive, è possibile configurare manualmente scenari worst-case basandosi sulle tolleranze specificate nei datasheet dei componenti.

📚 Modello Teorico e Formule
L'analisi si fonda sul modello elettrico equivalente del risonatore a quarzo e sulle condizioni di Barkhausen per l'oscillazione.

1. Capacità di Carico Effettiva (C 
L 
eff
​
 
​
 )
Assumendo un layout simmetrico con due condensatori di carico identici (C 
L 
sel
​
 
​
 ) e considerando le capacità parassite (C 
stray
​
 ) su un singolo ramo del circuito:

C_stray_single_leg = CS_PCB + CS_PIN
La capacità di carico effettiva vista dal cristallo è calcolata come:

CL_eff = (CL_sel + C_stray_single_leg) / 2.0
Dove:

CL_sel: Capacità del singolo condensatore di carico esterno.

CS_PCB: Capacità parassita introdotta dal PCB (per singolo ramo).

CS_PIN: Capacità parassita del pin del microcontrollore (per singolo ramo).

2. Transconduttanza Critica e Margine di Guadagno
Per garantire un avvio affidabile dell'oscillazione, la transconduttanza dell'amplificatore invertente del microcontrollore (g 
m
​
 ) deve superare un valore critico (g 
m 
crit
​
 
​
 ):

gm_crit = 4 * ESR * (2 * PI * F)^2 * (C0 + CL_eff)^2
Il margine di guadagno (Gain Margin) è il rapporto tra la transconduttanza del MCU e quella critica, e tipicamente si raccomanda un valore ≥ 5 per un design robusto.

Gain_Margin = gm / gm_crit
