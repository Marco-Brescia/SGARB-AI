@echo off

:: Verifica se il file AmbienteWin.yml esiste nella directory corrente
if not exist "AmbienteWin.yml" (
    echo Il file AmbienteWin.yml non è presente nella directory corrente!
    exit /b 1
)

:: Inizializza Conda
call "%USERPROFILE%\Anaconda3\Scripts\activate.bat"

:: Creazione dell'ambiente Conda
echo Creando l'ambiente Conda dal file AmbienteWin.yml...
conda env create -f AmbienteWin.yml

:: Attivazione dell'ambiente appena creato
echo Attivando l'ambiente...
conda init cmd.exe
conda activate py310Win

:: Conferma del successo
echo Ambiente Conda creato e attivato con successo!
echo Il processo di configurazione e' completato.
echo Per iniziare a lavorare, devi puntare all'interprete dell'ambiente Conda dal tuo IDE preferito.
pause