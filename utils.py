import os

def create_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def save_model(model, output_dir):
    model.save(os.path.join(output_dir, 'model.h5'))
    print(f"Modello e immagini salvate nella cartella {output_dir}")
