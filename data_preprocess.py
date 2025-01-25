import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Funzione per creare le cartelle di output
# crea le cartelle di output
# base_path: percorso della cartella principale
# return: percorso delle cartelle AI e REAL
def create_output_folders(base_path):
    processed_path = os.path.join(base_path, "DatasetTraining(Processed)")
    ai_path = os.path.join(processed_path, "AI")
    real_path = os.path.join(processed_path, "REAL")

    os.makedirs(ai_path, exist_ok=True)
    os.makedirs(real_path, exist_ok=True)

    return ai_path, real_path

# Funzione per ridimensionare e salvare le immagini
# image_path: percorso dell'immagine da ridimensionare
# output_folder: percorso della cartella di output
def resize_and_save(image_path, output_folder):
    try:
        with Image.open(image_path) as img:
            img = img.resize((224, 224))
            base_name = os.path.basename(image_path)
            output_path = os.path.join(output_folder, base_name)
            img.save(output_path)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Funzione per elaborare una cartella
# input_folder: percorso della cartella di input
# output_folder: percorso della cartella di output
# folder_name: nome della cartella interna a output_folder
def process_folder(input_folder, output_folder, folder_name):
    image_paths = [os.path.join(input_folder, img) for img in os.listdir(input_folder) if
                   img.lower().endswith(('png', 'jpg', 'jpeg'))]

    with tqdm(total=len(image_paths), desc=f"Processing {folder_name}", unit="file") as pbar: # barra di progresso
        with ThreadPoolExecutor() as executor:                                                # esecuzione in parallelo
            futures = {executor.submit(resize_and_save, image_path, output_folder): image_path for image_path in
                       image_paths}
            for future in as_completed(futures):
                try:
                    future.result()  # Verifica eventuali errori
                except Exception as e:
                    print(f"Error: {e}")
                pbar.update(1)


if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_ai_path = os.path.join(base_path, "DatasetTraining(NotProcessed)", "AI")
    input_real_path = os.path.join(base_path, "DatasetTraining(NotProcessed)", "REAL")

    output_ai_path, output_real_path = create_output_folders(base_path)

    process_folder(input_ai_path, output_ai_path, "AI")
    process_folder(input_real_path, output_real_path, "REAL")
