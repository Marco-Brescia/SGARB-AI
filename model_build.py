import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50

# Funzione per costruire il modello
# hp: oggetto HyperParameters
# img_width: larghezza delle immagini
# img_height: altezza delle immagini
# Return: modello costruito
# La funzione costruisce un modello con un'architettura ResNet50 e un classificatore custom
# L'ottimizzatore, la funzione di loss e le metriche sono definite all'interno della funzione

def build_model(hp, img_width, img_height):
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
        metrics=['accuracy', 'Recall']
    )

    return model
