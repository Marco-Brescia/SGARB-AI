from flask import Flask, request, jsonify, render_template
import os
import random  # Per simulare la predizione
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import tensorflow as tf

# Definizione della funzione di perdita personalizzata
def weighted_loss(y_true, y_pred):
    weight = tf.where(tf.equal(y_true, 0), 10.0, 1.0)
    return tf.reduce_mean(weight * tf.keras.losses.binary_crossentropy(y_true, y_pred))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Percorso del modello (relativo alla cartella interface)
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modello', 'new', 'model.h5')

# Carica il modello pre-addestrato
model = load_model(MODEL_PATH, custom_objects={'weighted_loss': weighted_loss})

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

    # Preprocessa l'immagine e fai una previsione (Commentato)
    img_array = preprocess_image(file_path)
    prediction = model.predict(img_array)
    os.remove(file_path)  # Rimuove l'immagine caricata dopo la classificazione

    # Interpreta il risultato (Supponendo che la soglia sia 0.5)
    result = 'IA' if prediction[0] > 0.5 else 'Real'

    confidence = float(prediction[0]) if result == 'IA' else 1 - float(prediction[0])

    return jsonify({'result': result, 'confidence': f"{confidence * 100:.2f}"})

if __name__ == '__main__':
    # Crea la cartella di upload se non esiste
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
