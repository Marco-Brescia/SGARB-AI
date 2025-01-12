import os
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.metrics import Recall
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
import keras_tuner as kt

# Percorsi delle directory

# `dataset_dir` è la cartella dei dati processati
# Esempio: "DatasetTraining(Processed)"
dataset_dir = ""

# `test_dir` è la cartella di test
# Esempio: "Test"
test_dir = ""

# `output_dir` è la cartella di output del modello e dei grafici
# Esempio: 'modello/new/'
output_dir = ''

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Impostazioni
img_width, img_height = 224, 224
batch_size = 32

# Data generators
train_datagen = ImageDataGenerator(rescale=1. / 255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    dataset_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    dataset_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'
)

test_datagen = ImageDataGenerator(rescale=1. / 255)
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=False
)

# Funzione per costruire il modello
def build_model(hp):
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(hp.Int('units', min_value=512, max_value=2048, step=512), activation='relu'),
        layers.Dropout(hp.Float('dropout', min_value=0.2, max_value=0.5, step=0.1)),
        layers.Dense(1, activation='sigmoid')
    ])

    def weighted_loss(y_true, y_pred):
        weight = tf.where(tf.equal(y_true, 0), 10.0, 1.0)
        return tf.reduce_mean(weight * tf.keras.losses.binary_crossentropy(y_true, y_pred))

    model.compile(
        optimizer=hp.Choice('optimizer', values=['adam', 'sgd']),
        loss=weighted_loss,
        metrics=['accuracy', Recall()]
    )

    return model

# Tuner
tuner = kt.Hyperband(
    build_model,
    objective='val_accuracy',
    max_epochs=25,
    directory='hp_tuning',
    project_name='auto_ml_project'
)

# Ricerca dei migliori iperparametri
tuner.search(
    train_generator,
    epochs=25,
    validation_data=validation_generator,
    callbacks=[EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)]
)

best_hyperparameters = tuner.get_best_hyperparameters()[0]
model = tuner.hypermodel.build(best_hyperparameters)

history = model.fit(
    train_generator,
    epochs=25,
    validation_data=validation_generator,
    callbacks=[EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)]
)

# Valutazione finale
evaluation_results = model.evaluate(test_generator, verbose=1)
metrics_names = model.metrics_names
evaluation_summary = "\n".join(
    [f"{name}: {value:.4f}" for name, value in zip(metrics_names, evaluation_results)]
)
print("*** Risultati della Valutazione Finale ***")
print(evaluation_summary)

# Predizioni sul test set
y_pred = model.predict(test_generator)
y_true = test_generator.labels
y_pred_binary = (y_pred > 0.5).astype(int)

# Metriche
precision = precision_score(y_true, y_pred_binary)
recall = recall_score(y_true, y_pred_binary)

# Salva la matrice di confusione
cm = confusion_matrix(y_true, y_pred_binary)
cm_display = ConfusionMatrixDisplay(confusion_matrix=cm)
cm_display.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'))
plt.close()

# Grafici per accuracy e recall
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

# Salva il modello
model.save(os.path.join(output_dir, 'model.h5'))
print(f"Modello e immagini salvate nella cartella {output_dir}")
