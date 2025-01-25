import os
import shutil
import tkinter as tk
from tkinter import ttk
from pathlib import Path

# Definisci il percorso della cartella di origine e della cartella di destinazione
base_dir = Path("")
output_base_dir_ai = Path("Test/AI_test")  # Cartella di destinazione per AI_LD e simili
output_base_dir_real = Path("Test/REAL_test")  # Cartella di destinazione per le altre cartelle

# Crea le cartelle di destinazione se non esistono
output_base_dir_ai.mkdir(parents=True, exist_ok=True)
output_base_dir_real.mkdir(parents=True, exist_ok=True)


# Funzione per copiare le immagini dalle sottocartelle
def copy_images_from_subfolder(src_folder, dest_folder, progress_bar):
    # Conta il numero totale di immagini da copiare
    total_images = sum([len(files) for r, d, files in os.walk(src_folder) if
                        any(file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff')) for file in files)])

    # Imposta la barra di progresso
    progress_bar['maximum'] = total_images
    progress_bar['value'] = 0
    progress_bar.update()

    for folder in os.listdir(src_folder):
        folder_path = src_folder / folder
        if folder_path.is_dir():
            # Esplora tutte le immagini nella sottocartella
            for img_file in os.listdir(folder_path):
                img_path = folder_path / img_file
                if img_path.is_file() and img_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
                    try:
                        # Copia l'immagine direttamente nella cartella di destinazione
                        shutil.copy(img_path, dest_folder / img_file)
                        print(f"Copia immagine: {img_path} a {dest_folder}")
                    except Exception as e:
                        print(f"Errore nel copiare l'immagine {img_path}: {e}")

                    # Aggiorna la barra di progresso
                    progress_bar['value'] += 1
                    progress_bar.update()


# Funzione per copiare tutte le immagini da AI e REAL
def copy_all_images():
    # Creazione della finestra Tkinter per la barra di progresso
    root = tk.Tk()
    root.title("Copia delle Immagini")

    # Barra di progresso globale
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(padx=20, pady=20)

    # Cicla attraverso tutte le cartelle in 'test'
    for folder in os.listdir(base_dir):
        folder_path = base_dir / folder
        if folder_path.is_dir():
            # Se la cartella contiene "AI" nel nome, copia le immagini in 'AI_test'
            if "AI" in folder:
                print(f"Inizio copia delle immagini da {folder}...")
                copy_images_from_subfolder(folder_path, output_base_dir_ai, progress_bar)
                print(f"Copia delle immagini da {folder} completata.")
            else:
                # Altrimenti, copia le immagini in 'REAL_test'
                print(f"Inizio copia delle immagini da {folder}...")
                copy_images_from_subfolder(folder_path, output_base_dir_real, progress_bar)
                print(f"Copia delle immagini da {folder} completata.")

    # Avvio della finestra di Tkinter
    root.mainloop()


# Esegui la copia delle immagini
copy_all_images()

print("Processo completato: tutte le immagini sono state copiate.")
