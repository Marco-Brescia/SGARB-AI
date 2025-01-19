@echo off

:: Verifica se Anaconda è già installato
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Anaconda non trovato, procedo con l'installazione...

    :: Scarica il file di installazione di Anaconda (versione 64-bit per Windows)
    echo Scaricando Anaconda...
    echo Questo potrebbe richiedere del tempo, attendere pazientemente.
    echo Il download e' in corso...
    echo Se sembra che il processo sia bloccato, non ti preoccupare, e' normale, il download sta procedendo.
    powershell -command "& { (New-Object System.Net.WebClient).DownloadFile('https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Windows-x86_64.exe', 'Anaconda3-installer.exe') }"

    echo Download completato!

    :: Esegui l'installazione di Anaconda in modalità silenziosa
    echo Installazione di Anaconda in corso...
    start /wait "" Anaconda3-installer.exe /InstallationType=JustMe /RegisterPython=1 /S /D=%USERPROFILE%\Anaconda3

    :: Verifica che l'installazione sia riuscita
    if not exist "%USERPROFILE%\Anaconda3\Scripts\conda.exe" (
        echo Errore: Installazione di Anaconda non riuscita.
        del Anaconda3-installer.exe
        exit /b 1
    )

    :: Aggiungi Anaconda al PATH
    echo Aggiungendo Anaconda al PATH...
    setx PATH "%USERPROFILE%\Anaconda3;%USERPROFILE%\Anaconda3\Scripts;%USERPROFILE%\Anaconda3\Library\bin;%PATH%" /m

    :: Pulisci il file dell'installer
    del Anaconda3-installer.exe

    echo Anaconda installato con successo!
) else (
    echo Anaconda e' gia' installato!
)

echo Anaconda e' stato installato correttamente e aggiunto al PATH, ma Windows potrebbe non riconoscerlo immediatamente.
echo Questo accade perche' le variabili d'ambiente potrebbero non aggiornarsi subito.
echo Per garantire il corretto funzionamento dei comandi di Anaconda, potrebbe essere necessario riavviare il computer.
echo Nonostante cio', il processo di configurazione continuera' normalmente tramite Anaconda Prompt.

:: Esegui setup.bat che si occupa della creazione e attivazione dell'ambiente Conda
echo Eseguendo setup.bat...
call setup.bat

pause
