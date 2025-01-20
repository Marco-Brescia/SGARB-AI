import os
import shutil
import numpy as np
import gc
from sklearn.decomposition import PCA
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import matplotlib.pyplot as plt

# Configurazione directory
source_dir = Path(
    "input_base_dir")
output_dir = Path("filtered_images_Varianza")
output_dir.mkdir(exist_ok=True)
grafici_dir = Path("grafici")
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

# Funzione per filtro basato sul tipo di immagini (IA o reali)
def filter_images_by_type(images, paths, category, max_images=1000):
    # Estrazione delle caratteristiche
    features = extract_features(images)

    # Riduzione della dimensionalità con PCA
    pca = PCA(n_components=50)
    features_reduced = pca.fit_transform(features)

    if category == "AI":
        # Per immagini IA: seleziona con varianza più bassa
        variances = np.var(features_reduced, axis=1)
        sorted_indices = np.argsort(variances)  # Ordine crescente (varianza più bassa)
    else:
        # Per immagini reali: seleziona con varianza più alta
        variances = np.var(features_reduced, axis=1)
        sorted_indices = np.argsort(variances)[::-1]  # Ordine decrescente (varianza più alta)

    # Seleziona le immagini in base alla varianza
    selected_indices = sorted_indices[:max_images]
    selected_paths = [paths[i] for i in selected_indices]

    return selected_paths, features_reduced, selected_indices

# Funzione per salvare il grafico del grafico
def save_image(features_reduced, folder_name, selected_indices=None):
    plt.figure(figsize=(8, 6))

    # Usiamo PCA per ridurre a 2 dimensioni per la visualizzazione
    pca_2d = PCA(n_components=2)
    reduced_2d = pca_2d.fit_transform(features_reduced)

    # Crea un array fittizio di "cluster_labels" per la visualizzazione
    cluster_labels = np.zeros(reduced_2d.shape[0])

    # Visualizza tutte le immagini come pallini blu
    plt.scatter(reduced_2d[:, 0], reduced_2d[:, 1], c=cluster_labels, cmap='tab20', marker='o', alpha=0.6, label='Immagini')

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

    # Filtra le immagini in base alla categoria
    filtered_paths, features_reduced, selected_indices = filter_images_by_type(images, paths, category)

    # Salva il grafico del clustering con i nuovi "cluster_labels"
    save_image(features_reduced, folder.name, selected_indices)

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
folders = [f for f in source_dir.iterdir() if f.is_dir() and f.name not in ["REAL", "AI"]]

for folder in folders:
    progress_bar['value'] = 0  # Reset della barra di progresso per ogni cartella
    progress_bar['maximum'] = len(os.listdir(folder))  # Imposta la lunghezza massima della barra

    process_folder(folder, progress_bar)

print("Processo completato. Immagini filtrate salvate in:", output_dir)
print("Immagini dei cluster salvate in:", grafici_dir)

# Avvio dell'interfaccia grafica
root.mainloop()
