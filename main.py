from data_loading import create_data_generators
from model_build import build_model
from hp_tuning import hyperparameter_tuning
from training import train_model
from evaluation import evaluate_model, compute_and_save_metrics
from graphics import plot_metrics
from utils import create_output_dir, save_model

def main():
    # Definisci i percorsi delle cartelle
    dataset_dir = "DatasetTrainingDistanzaCoseno_Distribuito(Processed)"  # Sostituisci con il percorso del dataset ES: "DatasetTraining(Processed)"
    test_dir = "Test"   # Sostituisci con il percorso della cartella di test ES: "Test"
    output_dir = "modello/specificity/"  # Sostituisci con il percorso della cartella di output dove salvare i risultati ES: 'modello/nuovo/'

    # Crea la cartella di output se non esiste
    create_output_dir(output_dir)

    # Impostazioni immagini
    img_width, img_height = 224, 224
    batch_size = 32

    # Creazione dei generatori di dati per il training, la validazione e il test
    train_generator, validation_generator, test_generator = create_data_generators(
        dataset_dir, test_dir, img_width, img_height, batch_size)

    # Ottimizzazione degli iperparametri tramite Hyperband
    model = hyperparameter_tuning(img_width, img_height,train_generator, validation_generator, build_model)

    # Addestramento del modello
    history = train_model(model, train_generator, validation_generator)

    # Valutazione finale del modello sul test set
    evaluate_model(model, test_generator)

    # Predizioni sul test set
    y_pred = model.predict(test_generator)
    y_true = test_generator.labels
    y_pred_binary = (y_pred > 0.5).astype(int)

    # Calcolare le metriche e salvarle
    precision, recall, accuracy, specificity = compute_and_save_metrics(y_true, y_pred_binary, output_dir)

    # Tracciare i grafici per precision, recall, accuracy, ecc.
    plot_metrics(history, accuracy, recall, precision, specificity, y_true, y_pred, output_dir)

    # Salvare il modello addestrato
    save_model(model, output_dir)

# Esegui il main se il file viene eseguito direttamente
if __name__ == "__main__":
    main()
