from flask import Flask, request, jsonify, render_template
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Percorso del modello (relativo alla cartella interface)
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modello', 'new', 'model.h5')

# Carica il modello pre-addestrato
model = load_model(MODEL_PATH)

# Preprocessing dell'immagine
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))  # Cambia la dimensione in base al tuo modello
    img_array = img_to_array(img) / 255.0  # Normalizza tra 0 e 1
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Salva l'immagine caricata
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Preprocessa l'immagine e fai una previsione
    img_array = preprocess_image(file_path)
    prediction = model.predict(img_array)
    os.remove(file_path)  # Rimuove l'immagine caricata dopo la classificazione

    # Interpreta il risultato (supponendo che la soglia sia 0.5)
    result = 'IA' if prediction[0] > 0.5 else 'Real'
    return jsonify({'result': result})

if __name__ == '__main__':
    # Crea la cartella di upload se non esiste
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)