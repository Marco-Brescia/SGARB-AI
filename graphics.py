import os
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

def plot_metrics(history, accuracy, recall, precision, specificity, y_test, y_probs, output_dir):
    # Grafico per accuracy e specificity3
    plt.figure(figsize=(10, 6))
    if 'accuracy' in history.history and 'val_accuracy' in history.history:
        plt.plot(history.history['accuracy'], label='Training Accuracy', linestyle='--', color='blue')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy', linestyle='-', color='blue')
    if 'specificity' in history.history and 'val_specificity' in history.history:
        plt.plot(history.history['specificity'], label='Training Specificity', linestyle='--', color='purple')
        plt.plot(history.history['val_specificity'], label='Validation Specificity', linestyle='-', color='purple')
    plt.title('Accuracy and Specificity (Training vs Validation)', fontsize=16)
    plt.xlabel('Epochs', fontsize=12)
    plt.ylabel('Metrics', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_specificity_plot.png'))
    plt.close()

    # Grafico per accuracy, recall, precision e specificity3
    metrics = ['Accuracy', 'Recall', 'Precision', 'Specificity']
    values = [accuracy, recall, precision, specificity]

    plt.figure(figsize=(10, 6))
    plt.bar(metrics, [value * 100 for value in values], color=['blue', 'green', 'orange', 'purple'])
    plt.title('Comparison of Accuracy, Recall, Precision and Specificity', fontsize=16)
    plt.ylabel('Percentage', fontsize=12)
    plt.ylim(0, 100)

    for i, v in enumerate(values):
        plt.text(i, v * 100 + 2, f"{v*100:.2f}%", ha='center', color='black', fontsize=12)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_recall_precision_specificity_plot.png'))
    plt.close()

    # Grafico per training e validation loss
    plt.figure(figsize=(10, 6))
    if 'loss' in history.history and 'val_loss' in history.history:
        plt.plot(history.history['loss'], label='Training Loss', linestyle='--', color='red')
        plt.plot(history.history['val_loss'], label='Validation Loss', linestyle='-', color='red')
    plt.title('Training and Validation Loss', fontsize=16)
    plt.xlabel('Epochs', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'training_validation_loss_plot.png'))
    plt.close()

    # Calcolare la curva ROC e l'area sotto la curva (AUC)
    fpr, tpr, thresholds = roc_curve(y_test, y_probs)
    roc_auc = auc(fpr, tpr)

    # Grafico ROC
    plt.figure(figsize=(10, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # linea diagonale
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC)', fontsize=16)
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'roc_curve.png'))
    plt.close()