Validatore di Circuiti Oscillatori a Quarzo

Versione: 3.1
Autore: Samuele Lorenzoni

Descrizione

Il software è pensato per supportare ingegneri e progettisti elettronici nella validazione e nel dimensionamento di circuiti oscillatori in configurazione Pierce, comunemente utilizzati con microcontrollori.

A partire dai dati del cristallo di quarzo e dai parametri del circuito, l’applicazione calcola i principali indicatori operativi e produce un report di valutazione utile a verificare la robustezza e l’affidabilità del progetto.

Parametri calcolati

Capacità di carico effettiva (CL_eff)

Transconduttanza critica (gm_crit)

Margine di guadagno

Drive Level (potenza dissipata dal cristallo)

Il risultato è presentato con un sistema di valutazione qualitativa:

OK

Attenzione

Critico

Caratteristiche principali

Analisi completa dei parametri di un oscillatore Pierce

Preset disponibili per quarzi e sonde di misura di uso comune

Interfaccia grafica con gestione automatica delle unità di misura

Report sintetico con valutazione qualitativa immediata

Architettura modulare basata sul pattern MVC, pensata per manutenzione ed estendibilità

Preset e analisi worst-case

Il software include preset per cristalli di quarzo diffusi (ad esempio serie Abracon IXA20), basati su valori tipici di targa.
Per analisi più restrittive è possibile configurare manualmente scenari worst-case, utilizzando le tolleranze specificate nei datasheet dei componenti.

Modello teorico e formule
1. Capacità di carico effettiva (CL_eff)

Si assume un layout simmetrico con due condensatori di carico identici (CL_sel) e capacità parassite (C_stray) su un singolo ramo del circuito:

C_stray_single_leg = CS_PCB + CS_PIN
CL_eff = (CL_sel + C_stray_single_leg) / 2.0


Dove:

CL_sel = capacità del singolo condensatore di carico esterno

CS_PCB = capacità parassita introdotta dal PCB (per ramo)

CS_PIN = capacità parassita del pin del microcontrollore (per ramo)

2. Transconduttanza critica e margine di guadagno

Affinché l’oscillazione si inneschi, la transconduttanza del microcontrollore (gm) deve essere superiore al valore critico (gm_crit):

gm_crit = 4 * ESR * (2 * PI * F)^2 * (C0 + CL_eff)^2


Il margine di guadagno si calcola come:

Gain_Margin = gm / gm_crit


Per un design robusto è consigliato Gain_Margin ≥ 5.
