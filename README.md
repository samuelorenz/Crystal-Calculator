```markdown
# Validatore di Circuiti Oscillatori a Quarzo
Versione: 3.1  
Autore: Samuele Lorenzoni

## Descrizione
Questo strumento aiuta ingegneri e progettisti elettronici a verificare e dimensionare circuiti oscillatori in configurazione Pierce (tipicamente usati con microcontrollori). A partire dalle specifiche del cristallo e dai parametri del circuito, l'applicazione calcola i principali parametri operativi come:

- capacità di carico effettiva,
- transconduttanza critica e margine di guadagno,
- Drive Level (potenza dissipata dal cristallo).

Il risultato è un report con indicazioni chiare (es. OK, Attenzione, Critico) per valutare la robustezza del progetto.

## Caratteristiche principali
- Analisi completa dei parametri di un oscillatore Pierce.
- Database di preset (quarzi e sonde) per inserimento rapido dei dati.
- Interfaccia grafica semplice e gestione automatica delle unità di misura.
- Report finale con valutazione qualitativa dei risultati.
- Architettura modulare (pattern MVC) per facilità di manutenzione ed estensione.

## Preset e analisi worst-case
Il software include preset per quarzi comuni. Per serie di componenti (es. Abracon IXA20) i preset rappresentano valori tipici: per analisi più restrittive è possibile eseguire scenari worst-case basati sulle tolleranze di datasheet.

## Modello teorico e formule principali
L'analisi si basa sul modello equivalente del risonatore a quarzo e sulle condizioni di Barkhausen. Di seguito le formule usate (variabili in maiuscolo indicate come nei datasheet).

1) Capacità di carico effettiva (CL_eff)

Assumendo un layout simmetrico con due condensatori di carico uguali (CL_sel per ciascun ramo) e capacità parassite su un singolo ramo:

- C_stray_single_leg = CS_PCB + CS_PIN
- CL_eff = (CL_sel + C_stray_single_leg) / 2.0

Dove:
- CL_sel: capacità del singolo condensatore di carico esterno.
- CS_PCB: capacità parassita del PCB (per ramo).
- CS_PIN: capacità parassita del pin MCU (per ramo).

2) Transconduttanza critica e margine di guadagno

La transconduttanza dell'amplificatore invertente del MCU (gm) deve superare una transconduttanza critica gm_crit per garantire l'innesco:

gm_crit = 4
