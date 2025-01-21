# SGARB-AI

![SGARB-AI](interface/static/images/logo_2su1_w.png)

## Gruppo

Il progetto è stato realizzato dal gruppo **Symposium**.

### Componenti del gruppo:
- 🧑‍💻 [**Giuseppe Gambardella**](https://github.com/giuseppegambardella)
- 🧑‍💻 [**Marco Brescia**](https://github.com/Marco-Brescia)
- 🧑‍💻 [**Francesco Faiella**](https://github.com/FaiellaFrancesco)


## Indice
1. 📝 [Introduzione](#-introduzione)
2. 📦 [Requisiti](#-requisiti)
3. 📦 [Gestione modelli con Git LFS](#-gestione-dei-modelli-con-git-lfs)
4. 🚀 [Come replicare il progetto](#-come-replicare-il-progetto)
    - 🗂️ [Reperire il dataset](#-reperire-il-dataset)
    - 🗑️ [Eliminazione cartelle non utilizzate](#-eliminazione-cartelle-non-utilizzate)
    - 🔢 [Selezione immagini con Coseno Distribuito per la riduzione del dataset per il training](#-selezione-immagini-con-coseno-distribuito-per-la-riduzione-del-dataset-per-il-training)
    - 📊 [Creazione del dataset per il training](#-creazione-del-dataset-per-il-training)
    - 🖼️ [Preprocessing delle immagini](#-preprocessing-delle-immagini)
    - 🧪 [Creazione del TestSet](#-creazione-del-testset)
    - 🏋️‍♂️ [Training del modello](#-training-del-modello)
    - 🔄 [Ordine di esecuzione degli script](#-ordine-di-esecuzione-degli-script)

## 📝 Introduzione

Il progetto **SGARB-AI** è stato sviluppato come parte del corso di **Intelligenza Artificiale** presso l'**Università degli Studi di Salerno**, nell'anno accademico **2024-2025**. L'obiettivo principale di questo progetto è l'implementazione di un sistema di riconoscimento delle immagini, utilizzando tecniche avanzate di deep learning, per distinguere tra opere d'arte reali e arte generata tramite algoritmi di intelligenza artificiale.

Attraverso l'analisi e il confronto di immagini provenienti da due categorie principali — **Arte Reale** e **Arte AI Generata** — il progetto mira a sviluppare un modello in grado di riconoscere le differenze tra arte prodotta da esseri umani e quella creata da algoritmi avanzati, con particolare attenzione alla riduzione del dataset e all'ottimizzazione del modello per una classificazione accurata.

In particolare, il progetto si è focalizzato maggiormente sul riconoscimento e la classificazione accurata della classe **AI Generata**, con l'intento di migliorare la capacità del modello di identificare le immagini generate tramite intelligenza artificiale, riducendo al minimo i falsi negativi in questa categoria.


# 📦 Requisiti

- Anaconda, una piattaforma per la gestione di ambienti e pacchetti Python, utile per data science, machine learning e progetti scientifici.

> **Nota:** Se Anaconda è già installato e il percorso è correttamente aggiunto alle variabili di ambiente, gli script procederanno esclusivamente con l'installazione dell'ambiente virtuale.

- In alternativa, puoi scaricare e installare manualmente Anaconda da questo link, scegliendo la versione adatta al tuo sistema operativo.
    - [Anaconda](https://repo.anaconda.com/archive)



## MacOS

1. Apri il terminale.
2. Naviga nella cartella `ambienti` del progetto:
    ```bash
    cd /percorso/del/progetto/ambienti
    ```
3. Esegui lo script di installazione per macOS:
    ```bash
    ./MacOSenv.sh
    ```
4. Segui le istruzioni nel terminale per completare l'installazione dell'ambiente.
5. Nel caso in cui il terminale non riconosca lo script come eseguibile, esegui il seguente comando:
    ```bash
    chmod +x MacOSenv.sh
    ```
    E ripeti il passaggio 3.
6. Non chiudere il terminale finché l'installazione non è completata.

## Windows

1. Apri il prompt dei comandi (CMD) come amministratore.
2. Naviga nella cartella `ambienti` del progetto:
    ```cmd
    cd \percorso\del\progetto\ambienti
    ```
3. Esegui lo script di installazione per Windows:
    ```bat
    WindowsEnv.bat
    ```
4. Segui le istruzioni nel prompt dei comandi per completare l'installazione dell'ambiente.

## Installazione esclusiva dell'ambiente virtuale senza Anaconda

1. Installa Anaconda dal link fornito sopra in modo che il percorso sia aggiunto alle variabili di ambiente.
2. Avvia lo script fornito sopra per importare l'ambiente virtuale:
    - MacOS: `MacOSenv.sh`
    - Windows: `WindowsEnv.bat`
3. Segui le istruzioni nel terminale o nel prompt dei comandi per completare l'installazione dell'ambiente.
4. Non chiudere il terminale o il prompt dei comandi finché l'installazione non è completata.
5. Se l'installazione è completata, puoi chiudere il terminale o il prompt dei comandi.

## 📦 Gestione dei modelli con Git LFS
1. File interessati: file con estensione `.h5`
2. Se aprendo un file .h5 trovi il seguente contenuto:
```
  version https://git-lfs.github.com/spec/v1
  oid sha256:9c5d3e1a842c7b51e03a1a6bd2d3b8499a7d543e71916a67f3f3280e3b7d9e7b
  size 10485760
```
Significa che il file è un segnaposto e il contenuto reale non è ancora stato scaricato.
3. Per scaricare i file completi, utilizza il seguente comando:

 ```bash
  git lfs pull
 ```

- Questo comando scaricherà i file reali dal server remoto, rendendoli pronti per l’uso.


In alcuni casi, i file vengono scaricati automaticamente durante il git clone o il git pull. Tuttavia, se trovi file .h5 che appaiono come segnaposto (con il contenuto testuale mostrato sopra), esegui manualmente git lfs pull per ottenere i dati completi.
>**Nota:** Git LFS è già installato nell’ambiente di lavoro preconfigurato, quindi non è necessario installarlo manualmente.


# 🚀 Come replicare il progetto

## 🗂️ Reperire il dataset

1. Scaricare il dataset dal seguente link:
    - [Dataset](https://www.kaggle.com/datasets/ravidussilva/real-ai-art)
    - Scaricato il dataset estraetelo in una cartella

## 🗑️ Eliminazione cartelle non utilizzate
1. Aprendo la cartella del dataset, la struttura sara' la seguente:
    ```
    real-ai-art
      ├── train
      │   ├── AI_LD_art_nouveau
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      │   ├── AI_LD_baroque
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      │   ├── AI_SD_art_nouveau
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   ├── AI_SD_baroque
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      │   ├── art_nouveau
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      │   ├── baroque
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      ├── test
      │   ├── AI_LD_art_nouveau
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      │   ├── AI_LD_baroque
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      │   ├── AI_SD_art_nouveau
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   ├── AI_SD_baroque
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      │   ├── art_nouveau
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
      │   ├── baroque
      │   │   ├── 00000001.jpg
      │   │   ├── 00000002.jpg
      │   │   │
      │   │   ├── ecc...
    ```
2. Eliminare le cartelle che hanno il prefisso `AI_SD` in entrambe le cartelle `train` e `test` poiché non sono utilizzate per il progetto.

## 🔢 Selezione immagini con Coseno Distribuito per la riduzione del dataset per il training
1. File interessato: `SelezioneImmaginiCosenoDistribuito.py`
2. Puntare il percorso del dataset nella variabile `source_dir`, dei risultati 
   - Esempio:
    ```python
    source_dir = Path("percorso/del/dataset/train ES: ../../real-ai-art/train") # Cartella contenente il dataset
    output_dir = Path("percorso/della/cartella/risultati") # Cartella di destinazione per le immagini selezionate
    output_dir.mkdir(exist_ok=True)
    grafici_dir = Path("percorsa/della/cartella/grafici") # Cartella di destinazione per i grafici
    grafici_dir.mkdir(exist_ok=True)
    ```
3. Eseguire lo script `SelezioneImmaginiCosenoDistribuito.py` per selezionare le immagini.
4. La cartella di output `output_dir` avrà questa struttura:
    ```
    nome_cartella
   ├── AI
   │   ├── new_AI_LD_art_nouveau
   │   │   ├── 00000001.jpg
   │   │   ├── 00000002.jpg
   │   │   ├── ...
   │   │   └── 0000xxxx.jpg
   │   ├── new_AI_LD_baroque
   │   │   ├── 00000001.jpg
   │   │   ├── 00000002.jpg
   │   │   ├── ...
   │   │   └── 0000xxxx.jpg
   │   ├── ecc...
   ├── REAL
   │   ├── new_art_nouveau
   │   │   ├── 00000001.jpg
   │   │   ├── 00000002.jpg
   │   │   ├── ...
   │   │   └── 0000xxxx.jpg
   │   ├── new_baroque
   │   │   ├── 00000001.jpg
   │   │   ├── 00000002.jpg
   │   │   ├── ...
   │   │   └── 0000xxxx.jpg
   │   ├── ecc...
    ```

## 📊 Creazione del dataset per il training
1. File interessato: `build_dataset.py`
2. Variabili interresate: `base_dir`, `output_base_dir`, `output_base_dir_real`
1. Aggiornare il valore di `base_dir` con il percorso della cartella creata dallo script precedente. Inoltre, modificare le variabili `output_base_dir` e `output_base_dir_real`.
   - Esempio:
    ```python
   # Cartella contenente le immagini selezionate 
   base_dir = Path("percorso/della/cartella/risultati")  # Cartella contenente le immagini selezionate
   # Cartelle di destinazione per i dataset
   output_base_dir = Path("DatasetTraining(NotProcessed)/AI")  # Cartella di destinazione per AI_LD
   output_base_dir_real = Path("DatasetTraining(NotProcessed)/REAL")  # Cartella di destinazione per REAL
    ```
2. Eseguire lo script `build_dataset.py` per creare il dataset per il training.
3. Le cartelle di output avranno questa struttura:
    ```
    DatasetTraining(NotProcessed)
   ├── AI
   │   ├── 00000001.jpg
   │   ├── 00000002.jpg
   │   ├── ...
   │   └── 0000xxxx.jpg
   ├── REAL
   │   ├── 00000001.jpg
   │   ├── 00000002.jpg
   │   ├── ...
   │   └── 0000xxxx.jpg
   ```
> **Nota:** Per evitare confusione, si consiglia di aggiungere l'etichetta (NotProcessed) alle cartelle di output. In questa fase, le immagini non sono ancora utilizzabili dal modello, poiché non rispettano la dimensione di 224 x 224 pixel richiesta. Al momento, le immagini sono ancora 256 x 256 pixel. Il nome `DatasetTraining(NotProcessed)` è da considerare come placeholder.

## 🖼️ Preprocessing delle immagini
1. Rinominare la variabile relativa alla cartella processata in `processed_path` all'interno di `data_preprocess.py`. Inoltre, aggiornare i percorsi delle cartelle di input con l'etichetta `NotProcessed` in `input_ai_path` e `input_real_path` nella sezione `__main__`, utilizzando i nomi delle cartelle ricavati dai passaggi precedenti.
   - Esempio:
    ```python
   def create_output_folders(base_path):
    processed_path = os.path.join(base_path, "cartella_di_destinazione(Processed)")
    ai_path = os.path.join(processed_path, "AI")
    real_path = os.path.join(processed_path, "REAL")
   
       os.makedirs(ai_path, exist_ok=True)
       os.makedirs(real_path, exist_ok=True)
   
       return ai_path, real_path
    ```
   ```python
   if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_ai_path = os.path.join(base_path, "nome_cartella(NotProcessed)", "AI")
    input_real_path = os.path.join(base_path, "nome_cartella(NotProcessed)", "REAL")
    ```
2. Eseguire lo script `data_preprocess.py` per preprocessare le immagini.
3. Le cartelle di output avranno questa struttura:
    ```
    cartella_di_destinazione(Processed)
   ├── AI
   │   ├── 00000001.jpg
   │   ├── 00000002.jpg
   │   ├── ...
   │   └── 0000xxxx.jpg
   ├── REAL
   │   ├── 00000001.jpg
   │   ├── 00000002.jpg
   │   ├── ...
   │   └── 0000xxxx.jpg
   ```
> **Nota:** Le immagini sono state ridimensionate a 224 x 224 pixel e sono ora pronte per il training. È possibile modificare i percorsi delle cartelle di destinazione tramite le variabili `ai_path` e `real_path`; tuttavia, questa operazione è fortemente sconsigliata, in quanto richiederebbe ulteriori modifiche agli script per garantirne il corretto funzionamento.

## 🧪 Creazione del TestSet
1. Modificare i valori delle variabili `base_dir`, `output_base_dir` e `output_base_dir_real` nel file `build_testset.py` per specificare i nomi delle cartelle di input (relative ai dati di test) e delle cartelle di output desiderate.
   - Esempio:
    ```python
   # Cartella contenente le immagini selezionate 
   base_dir = Path("percorso_della_cartella_test ES: ../../real-ai-art/test")  # Cartella contenente le immagini per il test
   # Cartelle di destinazione per le immagini di test
   output_base_dir = Path("cartella_test/AI_test ES: TestSet/AI_test")  # Cartella di destinazione per AI
   output_base_dir_real = Path("cartella_test/REAL_test ES: TestSet/REAL_test")  # Cartella di destinazione per REAL
    ```
2. Eseguire lo script `build_testset.py` per creare la cartella di test.
3. La cartella di output avrà questa struttura:
    ```
    TestSet
   ├── AI_test
   │   ├── 00000001.jpg
   │   ├── 00000002.jpg
   │   ├── ...
   │   └── 0000xxxx.jpg
   ├── REAL_test
   │   ├── 00000001.jpg
   │   ├── 00000002.jpg
   │   ├── ...
   │   └── 0000xxxx.jpg
    ```

## ️🏋️‍♂️ Training del modello

1. Modificare i valori delle variabili `dataset_dir`, `test_dir` e `output_dir` nel file `main.py` per specificare i percorsi delle cartelle di input e di output.
   - Esempio:
    ```python
   def main():
    # Definisci i percorsi delle cartelle
    dataset_dir = ""  # Sostituisci con il percorso del dataset ES: "DatasetTraining(Processed)"
    test_dir = ""   # Sostituisci con il percorso della cartella di test ES: "Test"
    output_dir = ""         # Sostituisci con il percorso della cartella di output dove salvare i risultati ES: 'modello/nuovo/'
    ```
2. Eseguire lo script `main.py` per avviare il training del modello.
3. I risultati del training saranno salvati nella cartella di output specificata.
4. Il modello addestrato sarà salvato come `model.h5` nella cartella di output.
5. I risultati del training saranno salvati come grafici nella cartella di output.
6. I risultati del training includono:
    - Grafico dell'accuratezza e recall
    - Grafico della loss
    - Grafico della matrice di confusione
    - Grafico della curva Precision-Recall
    - Grafico precision, recall, accuracy

# 🔄 Ordine di esecuzione degli script
1. `SelezioneImmaginiCosenoDistribuito.py`
2. `build_dataset.py`
3. `data_preprocess.py`
4. `build_testset.py`
5. `main.py`


## 🌐 Esecuzione dell'interfaccia

Per avviare l'interfaccia web di **SGARB-AI**, segui questi passaggi:

1. Apri un terminale o prompt dei comandi.
2. Naviga alla cartella `/interface` del progetto:
    ```bash
    cd /percorso/del/progetto/interface
    ```
3. Esegui il file `app.py` utilizzando Python:
    ```bash
    python app.py
    ```
4. Una volta avviato, il terminale mostrerà un messaggio simile a questo:
    ```
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```
5. Apri un browser e vai all'indirizzo [http://127.0.0.1:5000](http://127.0.0.1:5000). Visualizzerai l'interfaccia grafica del progetto.

> **Nota:** Assicurati che tutte le dipendenze richieste per il progetto siano installate e che l'ambiente virtuale sia attivo.

