from tensorflow.keras.callbacks import EarlyStopping

# Funzione per addestrare il modello
# model: modello da addestrare
# train_generator: generator per il training set
# validation_generator: generator per il validation set
# Return: history
# La funzione addestra il modello per 25 epoche
# Il training si ferma se la loss sul validation set non migliora per 5 epoche
def train_model(model, train_generator, validation_generator):
    history = model.fit(
        train_generator,
        epochs=25,
        validation_data=validation_generator,
        callbacks=[EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)]
    )
    return history
