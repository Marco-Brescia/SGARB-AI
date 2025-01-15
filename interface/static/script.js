// Seleziona l'input file e l'area del placeholder
const fileInput = document.getElementById('file');
const imagePlaceholder = document.querySelector('.image-placeholder');

// Aggiungi un listener per mostrare un'anteprima dell'immagine
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            imagePlaceholder.innerHTML = `<img src="${reader.result}" alt="Preview" style="max-width: 100%; max-height: 100%; border-radius: 8px;">`;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        if (data.result) {
            const result = data.result;
            const confidence = data.confidence;

            // Seleziona i blocchi
            const blockLeft = document.getElementById('block_perc_left');
            const blockRight = document.getElementById('block_perc_right');
            const AiConfidence = document.getElementById('perc-IA');
            const HumanConfidence = document.getElementById('perc-Real');

            // Aggiusta le classi in base al risultato
            if (result === 'IA') {
                AiConfidence.innerHTML = confidence + '%';
                blockLeft.classList.add('active');
                blockLeft.classList.remove('inactive');
                HumanConfidence.innerHTML = '';
                blockRight.classList.add('inactive');
                blockRight.classList.remove('active');
            } else {
                HumanConfidence.innerHTML = confidence + '%';
                blockRight.classList.add('active');
                blockRight.classList.remove('inactive');
                AiConfidence.innerHTML = '';
                blockLeft.classList.add('inactive');
                blockLeft.classList.remove('active');
            }
        } else {
            alert('Errore nella classificazione');
        }
    } catch (err) {
        console.error('Errore:', err);
        alert('Errore nella comunicazione con il server.');
    }
});