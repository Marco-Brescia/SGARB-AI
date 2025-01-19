#!/bin/bash

# Verifica se Anaconda è già installato
if ! command -v conda &> /dev/null; then
    echo "Anaconda non trovato, procedo con l'installazione..."

    # Controlla se `curl` è installato
    if ! command -v curl &> /dev/null; then
        echo "Errore: il comando 'curl' non è installato. Installalo e riprova."
        exit 1
    fi

    # Scarica il file di installazione di Anaconda
    echo "Scaricando Anaconda..."
    curl -# -o anaconda_installer.sh https://repo.anaconda.com/archive/Anaconda3-2024.06-1-MacOSX-arm64.sh

    # Rendi eseguibile il file di installazione
    chmod +x anaconda_installer.sh

    # Esegui l'installazione solo se la directory non esiste
    if [ -d "$HOME/anaconda3" ]; then
        echo "Anaconda è già presente in $HOME/anaconda3. Usa l'opzione -u per aggiornare manualmente."
    else
        ./anaconda_installer.sh -b -p $HOME/anaconda3
    fi

    # Verifica se la riga non è già presente in ~/.zshrc
    if ! grep -q 'export PATH="$HOME/anaconda3/bin:$PATH"' ~/.zshrc; then
        # Aggiungi la riga al file ~/.zshrc
        echo 'export PATH="$HOME/anaconda3/bin:$PATH"' | sudo tee -a ~/.zshrc > /dev/null
    fi

    # Ricarica il file ~/.zshrc per applicare le modifiche
    source ~/.zshrc

    rm anaconda_installer.sh

    # Chiudi la console e riaprila
    echo "Per applicare le modifiche al PATH, verrà aperto un altro terminale."
    # Dopo aver aggiornato ~/.zshrc o ~/.bash_profile
    osascript -e "tell application \"Terminal\" to do script \"cd '$(pwd)' && './MacOSenv.sh'\""
    exit 0
fi

# Verifica se Conda è correttamente installato
if command -v conda &> /dev/null; then
    echo "Conda è pronto per l'uso!"
else
    echo "Errore: Conda non è stato installato correttamente."
    exit 1
fi

# Verifica se il file AmbienteMacOS.yml esiste nella directory corrente
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