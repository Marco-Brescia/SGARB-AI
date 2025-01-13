from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Funzione per creare i data generators
# dataset_dir: directory del dataset
# test_dir: directory del test set
# img_width: larghezza delle immagini
# img_height: altezza delle immagini
# batch_size: dimensione del batch
# Return: train_generator, validation_generator, test_generator
# La funzione carica le immagini dal dataset e le divide in training e validation set
# Il test set è caricato separatamente
def create_data_generators(dataset_dir, test_dir, img_width, img_height, batch_size):

    # Generatore per il training e la validazione
    train_datagen = ImageDataGenerator(rescale=1. / 255, validation_split=0.2)

    train_generator = train_datagen.flow_from_directory(    # cartella del dataset da cui caricare le immagini
        dataset_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory( # cartella del dataset da cui caricare le immagini per il validation test
        dataset_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary',
        subset='validation'
    )

    # Generatore per il test set
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_generator = test_datagen.flow_from_directory(  # cartella del test set da cui caricare le immagini
        test_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary',
        shuffle=False
    )

    print("Etichette nel train generator:", train_generator.class_indices)
    print("Etichette nel validation generator:", validation_generator.class_indices)
    print("Etichette nel test generator:", test_generator.class_indices)

    return train_generator, validation_generator, test_generator
