@echo off

:: Verifica se Anaconda è già installato
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Anaconda non trovato, procedo con l'installazione...

    :: Scarica il file di installazione di Anaconda (versione 64-bit per Windows) con barra di progresso
    echo Scaricando Anaconda...
    powershell -command "& { (New-Object System.Net.WebClient).DownloadFile('https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Windows-x86_64.exe', 'Anaconda3-installer.exe') }"



    Write-Host "Download completato!""
    :: Esegui l'installazione di Anaconda in modalità silenziosa
    echo Installazione di Anaconda...
    start /wait Anaconda3-installer.exe /InstallationType=JustMe /RegisterPython=1 /S /D=%USERPROFILE%\Anaconda3

    :: Aggiungi Anaconda al PATH
    echo Aggiungendo Anaconda al PATH...
    setx PATH "%USERPROFILE%\Anaconda3;%USERPROFILE%\Anaconda3\Scripts;%USERPROFILE%\Anaconda3\Library\bin;%PATH%"

    :: Pulisci il file dell'installer
    del Anaconda3-installer.exe

    echo Anaconda installato con successo!
) else (
    echo Anaconda è già installato!
)

:: Verifica se Conda è correttamente installato
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Errore: Conda non è stato installato correttamente.
    exit /b 1
)

:: Verifica se il file AmbienteWindows.yml esiste nella directory corrente
if not exist "AmbienteWin.yml" (
    echo Il file AmbienteWin.yml non è presente nella directory corrente!
    exit /b 1
)

:: Crea l'ambiente Conda dal file .yml
echo Creando l'ambiente Conda dall'file AmbienteWin.yml...
call conda env create -f AmbienteWin.yml

:: Attiva l'ambiente appena creato
echo Attivando l'ambiente...
call conda init
call conda activate py310Win

echo Ambiente Conda creato e attivato con successo!
