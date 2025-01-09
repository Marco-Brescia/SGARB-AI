from flask import Flask, render_template, request

app = Flask(__name__)

# Rotta per la home page
@app.route('/')
def home():
    return render_template('index.html')

# Rotta per gestire i file caricati (ad esempio immagini)
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Nessun file caricato", 400

    file = request.files['file']

    # Salva il file o esegui il tuo modello qui
    # file.save('percorso_dove_salvare_il_file')

    # Simula una risposta
    response = {"message": "File caricato con successo"}
    return response, 200


if __name__ == '__main__':
    app.run(debug=True)
