# Validatore di Circuiti Oscillatori a Quarzo

## Versione
3.1

## Autore
Samuele Lorenzoni

---

## Descrizione
Questo software supporta ingegneri e progettisti elettronici nella validazione e nel dimensionamento di circuiti oscillatori in configurazione Pierce, comunemente usati con microcontrollori. A partire dai dati del cristallo di quarzo e dai parametri del circuito, l’applicazione calcola i principali indicatori operativi e produce un report di valutazione utile a verificare la robustezza del progetto.

---

## Output e valutazione qualitativa
L’applicazione calcola i parametri principali e fornisce una valutazione qualitativa immediata in tre livelli:
- OK
- Attenzione
- Critico

---

## Parametri calcolati
- Capacità di carico effettiva (CL_eff)  
- Transconduttanza critica (gm_crit)  
- Margine di guadagno (Gain_Margin)  
- Drive Level (potenza dissipata dal cristallo)

---

## Caratteristiche principali
- Analisi completa dei parametri di un oscillatore Pierce  
- Preset disponibili per quarzi e sonde di misura di uso comune  
- Interfaccia grafica con gestione automatica delle unità di misura  
- Report sintetico con valutazione qualitativa immediata  
- Architettura modulare basata sul pattern MVC, pensata per manutenzione ed estendibilità  
- Preset e analisi worst-case

---

## Preset e analisi worst-case
Il software include preset per cristalli di quarzo diffusi (ad esempio la serie Abracon IXA20), basati su valori tipici di targa. Per analisi più restrittive è possibile configurare manualmente scenari worst-case utilizzando le tolleranze indicate nei datasheet dei componenti.

---

## Modello teorico e formule

### 1) Capacità di carico effettiva (CL_eff)
Si assume un layout simmetrico con due condensatori di carico identici (CL_sel) e capacità parassite (C_stray) su un singolo ramo del circuito.

Formule:
```text
C_stray_single_leg = CS_PCB + CS_PIN
CL_eff = (CL_sel + C_stray_single_leg) / 2.0
```

Dove:
- CL_sel = capacità del singolo condensatore di carico esterno  
- CS_PCB = capacità parassita introdotta dal PCB (per ramo)  
- CS_PIN = capacità parassita del pin del microcontrollore (per ramo)

---

### 2) Transconduttanza critica (gm_crit) e margine di guadagno
Perché l’oscillazione si inneschi, la transconduttanza del driver (gm) deve essere superiore al valore critico gm_crit.

Formula per la transconduttanza critica:
```text
gm_crit = 4 * ESR * (2 * PI * F)^2 * (C0 + CL_eff)^2
```

Margine di guadagno:
```text
Gain_Margin = gm / gm_crit
```

Linea guida di progetto:
- Per un design robusto è consigliato avere Gain_Margin ≥ 5.

Dove:
- ESR = Equivalent Series Resistance del cristallo  
- F = frequenza di risonanza (Hz)  
- C0 = capacità shunt del cristallo  
- CL_eff = capacità di carico effettiva calcolata sopra  
- gm = transconduttanza del driver (microcontrollore o stadio attivo)

---

### 3) Drive Level
Il Drive Level è la potenza dissipata dal cristallo e viene calcolata a partire dalla tensione e dalle correnti nel circuito. Il software fornisce il valore di Drive Level confrontandolo con i limiti massimi raccomandati dal produttore per valutare eventuali rischi di danneggiamento o instabilità.

---

## Note finali
- I risultati devono essere interpretati tenendo conto delle tolleranze dei componenti e delle condizioni operative reali (temperatura, alimentazione, layout PCB).  
- Per analisi conservative utilizzare i preset worst-case o inserire manualmente le tolleranze dei componenti dai datasheet.

---
```
