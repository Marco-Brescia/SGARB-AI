import keras_tuner as kt
from tensorflow.keras.callbacks import EarlyStopping

# Funzione per l'ottimizzazione degli iperparametri
# imgwidth: larghezza delle immagini
# imgheight: altezza delle immagini
# train_generator: generator per il training set
# validation_generator: generator per il validation set
# build_model: funzione per costruire il modello
# Return: modello con gli iperparametri ottimizzati
# La funzione utilizza keras_tuner per l'ottimizzazione degli iperparametri
# La funzione restituisce il modello con gli iperparametri ottimizzati
def hyperparameter_tuning(imgwidth, imgheight, train_generator, validation_generator, build_model):
    tuner = kt.Hyperband(
        build_model,
        objective='val_accuracy',
        max_epochs=25,
        directory='hp_tuning',
        project_name='auto_ml_project'
    )

    tuner.search(
        train_generator,
        epochs=25,
        validation_data=validation_generator,
        callbacks=[EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)]
    )

    best_hyperparameters = tuner.get_best_hyperparameters()[0]
    model = tuner.hypermodel.build(best_hyperparameters, img_width=imgwidth, img_height=imgheight)

    return model
