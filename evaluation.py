import os
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix, ConfusionMatrixDisplay, precision_score
import matplotlib.pyplot as plt

from model_build import specificity


# Valuta il modello con il generatore di test e restituisce i risultati della valutazione
# model: modello da valutare
# test_generator: generatore di test
# Restituisce i risultati della valutazione
def evaluate_model(model, test_generator):
    evaluation_results = model.evaluate(test_generator, verbose=1)
    return evaluation_results

# Funzione per calcolare e salvare le metriche
# Calcola la recall e l'accuracy e salva la matrice di confusione
# Restituisce la recall e l'accuracy
# y_true: etichette reali
# y_pred_binary: predizioni binarie
# output_dir: percorso della cartella di output
def compute_and_save_metrics(y_true, y_pred_binary, output_dir):
    # Calcola la matrice di confusione
    cm = confusion_matrix(y_true, y_pred_binary)

    # Estrai i valori dalla matrice di confusione
    tn, fp, fn, tp = cm.ravel()

    # Calcola precision, recall, accuracy e specificity3
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    specificity = tn / (tn + fp) if tn + fp > 0 else 0

    # Salva la matrice di confusione
    cm_display = ConfusionMatrixDisplay(confusion_matrix=cm)
    cm_display.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'))
    plt.close()

    return precision, recall, accuracy, specificity

