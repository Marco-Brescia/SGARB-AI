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
