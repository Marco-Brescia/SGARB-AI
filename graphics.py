import os
import matplotlib.pyplot as plt

def plot_metrics(history, accuracy, recall, precision, output_dir):
    # Grafico per accuracy e recall
    plt.figure(figsize=(10, 6))
    if 'accuracy' in history.history and 'val_accuracy' in history.history:
        plt.plot(history.history['accuracy'], label='Training Accuracy', linestyle='--', color='blue')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy', linestyle='-', color='blue')
    if 'recall' in history.history and 'val_recall' in history.history:
        plt.plot(history.history['recall'], label='Training Recall', linestyle='--', color='green')
        plt.plot(history.history['val_recall'], label='Validation Recall', linestyle='-', color='green')
    plt.title('Accuracy and Recall (Training vs Validation)', fontsize=16)
    plt.xlabel('Epochs', fontsize=12)
    plt.ylabel('Metrics', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_recall_plot.png'))
    plt.close()

    # Grafico per accuracy, recall e precision
    metrics = ['Accuracy', 'Recall', 'Precision']
    values = [accuracy, recall, precision]

    plt.figure(figsize=(10, 6))
    plt.bar(metrics, [value * 100 for value in values], color=['blue', 'green', 'orange'])
    plt.title('Comparison of Accuracy, Recall, and Precision', fontsize=16)
    plt.ylabel('Percentage', fontsize=12)
    plt.ylim(0, 100)

    for i, v in enumerate(values):
        plt.text(i, v * 100 + 2, f"{v*100:.2f}%", ha='center', color='black', fontsize=12)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_recall_precision_plot.png'))
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

