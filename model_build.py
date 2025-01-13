import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import backend as K

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

    model.compile(
        optimizer=hp.Choice('optimizer', values=['adam', 'sgd']),
        loss=weighted_loss,
        metrics=['accuracy', 'Recall']
    )

    return model

def weighted_loss(y_true, y_pred):
     # Peso per la classe AI (etichetta 0)
    weight_for_0 = 1.5  # Maggiore peso per la classe AI
    weight_for_1 = 1.0  # Ponderazione per la classe REAL (etichetta 1)

    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.clip_by_value(y_pred, K.epsilon(), 1.0 - K.epsilon())

    # Calcola il cross-entropy per ciascun campione
    cross_entropy = - (y_true * tf.math.log(y_pred) + (1 - y_true) * tf.math.log(1 - y_pred))

    # Aggiungi i pesi
    weight = y_true * weight_for_0 + (1 - y_true) * weight_for_1
    weighted_loss = cross_entropy * weight

    return tf.reduce_mean(weighted_loss)

#vecchia funzione di loss
# def weighted_loss(y_true, y_pred):
#    weight = tf.where(tf.equal(y_true, 0), 10.0, 1.0)
#    return tf.reduce_mean(weight * tf.keras.losses.binary_crossentropy(y_true, y_pred))