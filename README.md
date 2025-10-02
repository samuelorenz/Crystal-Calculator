========================================= Validatore di Oscillatori a Cristallo
--- Descrizione ---

Questo script e' uno strumento software per ingegneri elettronici e progettisti hardware.
Il suo scopo e' validare il design di un circuito oscillatore a cristallo (tipo Pierce)
basandosi sui parametri forniti dai datasheet dei componenti (cristallo, MCU) e sulle
misurazioni effettuate sul circuito reale.

L'applicazione esegue i calcoli fondamentali per determinare la stabilita' e
l'affidabilita' dell'oscillatore, fornendo un feedback immediato sulla bonta' del design.
La metodologia si basa su application note standard del settore, come la AN2867 di
STMicroelectronics.

--- Requisiti Tecnici ---

Piattaforma: Python

Versione Python: 3.7 o superiore (sviluppato e testato con Python 3.10)

Dipendenze Esterne: NumPy

Per installare la dipendenza, e' necessario eseguire il comando:
pip install numpy

--- Istruzioni per l'Esecuzione ---

Assicurarsi di avere Python 3 installato sul proprio sistema.

Aprire un terminale o prompt dei comandi.

Navigare fino alla cartella in cui si trova il file xtal_validator_app.py.

Installare la dipendenza NumPy con il comando:
pip install numpy

Avviare l'applicazione eseguendo lo script:
python xtal_validator_app.py

--- Funzionalita' Principali ---

Inserimento parametrizzato dei dati del cristallo, MCU e PCB.

Gestione intuitiva delle unita' di misura (MHz, pF, uW, etc.).

Calcolo dei parametri chiave:

Capacita' di Carico Effettiva (CL_eff)

Transconduttanza Critica (Gm_crit)

Margine di Guadagno (Gain Margin)

Drive Level (DL) effettivo

Report di validazione con stato immediato (OK, ATTENZIONE, CRITICO).

Preset per le sonde da oscilloscopio piu' comuni.

Interfaccia grafica completa con menu e barra di stato.

Versione applicazione: 2.5
