#!/bin/bash

# Verifica se Anaconda è già installato
if ! command -v conda &> /dev/null
then
    echo "Anaconda non trovato, procedo con l'installazione..."

    # Scarica il file di installazione di Anaconda
    echo "Scaricando Anaconda..."
    wget --progress=bar:force https://repo.anaconda.com/archive/Anaconda3-2024.06-1-MacOSX-arm64.sh -O anaconda_installer.sh

    # Rendi eseguibile il file di installazione
    chmod +x anaconda_installer.sh

    # Esegui l'installazione
    ./anaconda_installer.sh -b -p $HOME/anaconda3

    # Aggiungi Anaconda al PATH
    echo "Aggiungendo Anaconda al PATH..."
    echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bash_profile
    source ~/.bash_profile

    echo "Anaconda installato con successo!"
else
    echo "Anaconda è già installato!"
fi

# Verifica se Conda è correttamente installato
if command -v conda &> /dev/null
then
    echo "Conda è pronto per l'uso!"
else
    echo "Errore: Conda non è stato installato correttamente."
    exit 1
fi

# Verifica se il file environment.yml esiste nella directory corrente
if [ ! -f "AmbienteMacOS.yml" ]; then
    echo "Il file AmbienteMacOS.yml non è presente nella directory corrente!"
    exit 1
fi

# Crea l'ambiente Conda dal file .yml
echo "Creando l'ambiente Conda dall'file AmbienteMacOS.yml..."
conda env create -f AmbienteMacOS.yml
conda init bash
echo "Ambiente Conda creato con successo!"

printf "
L'ambiente è stato creato con successo! Per attivarlo, esegui il comando: conda activate py310MacOS\n
E' necessario il setup nell'ambiente di sviluppo puntando all'interprete python dell'ambiente creato.\n\n"