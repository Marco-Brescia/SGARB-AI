import os
import shutil
import numpy as np
import gc
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_distances
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import matplotlib.pyplot as plt

# Configurazione directory
source_dir = Path("")
output_dir = Path("filtered_images_DistanzaCoseno_Distribuito")
output_dir.mkdir(exist_ok=True)
grafici_dir = Path("grafici_DistanzaCoseno_Distribuito")
grafici_dir.mkdir(exist_ok=True)

# Configurazione TensorFlow per usare la GPU se disponibile
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
else:
    print("Nessuna GPU trovata, si utilizza la CPU.")

# Caricamento del modello ResNet50 pre-addestrato
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# Funzione per caricare un singolo file immagine con gestione degli errori
def load_single_image(img_path):
    try:
        img = Image.open(img_path).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = preprocess_input(img_array)  # Pre-elaborazione per ResNet50
        return img_array
    except Exception as e:
        print(f"Errore caricamento immagine {img_path}: {e}")
        return None

# Funzione per caricare immagini in parallelo con barra di progresso
def load_images(folder, progress_bar):
    images = []
    paths = []

    for file in os.listdir(folder):
        if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')):
            img_path = folder / file
            img_array = load_single_image(img_path)
            if img_array is not None:
                images.append(img_array)
                paths.append(img_path)
            progress_bar['value'] += 1  # Incrementa la barra di progresso
            progress_bar.update()  # Aggiorna la barra di progresso

    return np.array(images), paths

# Funzione per estrarre feature tramite ResNet50
def extract_features(images):
    images = tf.convert_to_tensor(images)  # Convertiamo in tensori TensorFlow
    features = model.predict(images, batch_size=32)  # Estrazione feature tramite il modello
    return features

# Funzione per filtro basato sulla distanza coseno con selezione di 2000 immagini distribuite uniformemente
def filter_images_by_cosine_distance(images, paths, category, max_images=2000):
    # Estrazione delle caratteristiche
    features = extract_features(images)

    # Calcolo del centroide delle feature
    centroid = np.mean(features, axis=0)

    # Calcolo della distanza coseno di ogni immagine rispetto al centroide
    distances = cosine_distances(features, centroid.reshape(1, -1)).flatten()

    # Ordinare le immagini in base alla distanza coseno
    sorted_indices = np.argsort(distances)

    # Selezionare 2000 immagini distribuite uniformemente su tutto l'intervallo delle distanze coseno
    # Creiamo degli "step" per coprire uniformemente le distanze
    step = len(distances) // max_images
    selected_indices = [sorted_indices[i * step] for i in range(max_images)]

    selected_paths = [paths[i] for i in selected_indices]

    return selected_paths, features, selected_indices


# Funzione per salvare il grafico delle immagini con le immagini selezionate
def save_image(features, folder_name, selected_indices=None):
    plt.figure(figsize=(8, 6))

    # Usiamo PCA per ridurre a 2 dimensioni per la visualizzazione
    pca_2d = PCA(n_components=2)
    reduced_2d = pca_2d.fit_transform(features)

    # Visualizza tutte le immagini come pallini blu
    plt.scatter(reduced_2d[:, 0], reduced_2d[:, 1], c='blue', marker='o', alpha=0.6, label='Immagini')

    # Aggiungi le X rosse per le immagini selezionate
    if selected_indices is not None:
        selected_2d = reduced_2d[selected_indices]
        plt.scatter(selected_2d[:, 0], selected_2d[:, 1], c='red', marker='x', s=100,
                    label='Immagini rappresentative')

    plt.title(f"Grafici - {folder_name}")
    plt.xlabel("Componente principale 1")
    plt.ylabel("Componente principale 2")
    plt.legend()

    cluster_plot_path = grafici_dir / f"{folder_name}_graphic.png"
    plt.savefig(cluster_plot_path)
    plt.close()

# Funzione per copiare le immagini selezionate nelle rispettive cartelle
def copy_images_to_respective_folders(selected_paths, category, output_category_dir):
    for img_path in selected_paths:
        try:
            shutil.copy(img_path, output_category_dir / Path(img_path).name)
        except Exception as e:
            print(f"Errore nel copiare l'immagine {img_path}: {e}")

# Funzione aggiornata per elaborare una cartella
def process_folder(folder, progress_bar):
    category = "AI" if "AI" in folder.name else "REAL"
    output_category_dir = output_dir / category / f"new_{folder.name}"
    output_category_dir.mkdir(parents=True, exist_ok=True)

    images, paths = load_images(folder, progress_bar)
    if not images.size:
        return

    filtered_paths, features, selected_indices = filter_images_by_cosine_distance(images, paths, category)

    # Salva il grafico del clustering con i nuovi "cluster_labels"
    save_image(features, folder.name, selected_indices)

    # Copia le immagini selezionate nella cartella di output
    copy_images_to_respective_folders(filtered_paths, category, output_category_dir)

    # Liberiamo la memoria delle immagini elaborate
    del images, paths
    gc.collect()  # Pulizia memoria CPU
    tf.keras.backend.clear_session()  # Se usi la GPU, libera la memoria GPU

# Interfaccia grafica con Tkinter
root = tk.Tk()
root.title("Sfoltimento del Dataset")

# Barra di progresso globale per il caricamento delle cartelle
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(padx=20, pady=20)

# Elaborazione delle cartelle sequenziale
folders = [f for f in source_dir.iterdir() if f.is_dir() and f.name not in ["REAL", "AI", "AI_LD"]]

for folder in folders:
    progress_bar['value'] = 0  # Reset della barra di progresso per ogni cartella
    progress_bar['maximum'] = len(os.listdir(folder))  # Imposta la lunghezza massima della barra

    process_folder(folder, progress_bar)

print("Processo completato. Immagini filtrate salvate in:", output_dir)
print("Immagini dei cluster salvate in:", grafici_dir)

# Avvio dell'interfaccia grafica
root.mainloop()
