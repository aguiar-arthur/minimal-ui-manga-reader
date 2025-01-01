document.addEventListener('DOMContentLoaded', () => {
    const imageWidthInput = document.getElementById('imageWidth');
    const imageHeightInput = document.getElementById('imageHeight');
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const imageDisplay = document.getElementById('imageDisplay');
    const imageNumberDisplay = document.createElement('div');

    let images = [];
    let currentIndex = 0;

    // Set default width and height for the image
    imageDisplay.style.width = `${imageWidthInput.value}px`;
    imageDisplay.style.height = `${imageHeightInput.value}px`;

    // Append the image number display to the gallery container
    document.querySelector('#gallery').appendChild(imageNumberDisplay);

    prevButton.addEventListener('click', () => navigateImages(-1));
    nextButton.addEventListener('click', () => navigateImages(1));

    imageWidthInput.addEventListener('input', () => {
        if (imageDisplay.src) {
            imageDisplay.style.width = `${imageWidthInput.value}px`;
        }
    });

    imageHeightInput.addEventListener('input', () => {
        if (imageDisplay.src) {
            imageDisplay.style.height = `${imageHeightInput.value}px`;
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowLeft') {
            navigateImages(-1);
        } else if (event.key === 'ArrowRight') {
            navigateImages(1);
        }
    });

    function navigateImages(direction) {
        if (!images.length) return;

        currentIndex += direction;

        if (currentIndex < 0) {
            currentIndex = 0;
        } else if (currentIndex >= images.length) {
            currentIndex = images.length - 1;
        }

        updateGallery();
    }

    function updateGallery() {
        if (!images.length) {
            imageDisplay.style.display = 'none';
            prevButton.disabled = nextButton.disabled = true;
            imageNumberDisplay.textContent = '';
        } else {
            imageDisplay.src = images[currentIndex];
            imageDisplay.style.display = 'block';

            imageDisplay.style.width = `${imageWidthInput.value}px`;
            imageDisplay.style.height = `${imageHeightInput.value}px`;

            prevButton.disabled = currentIndex === 0;
            nextButton.disabled = currentIndex === images.length - 1;
            imageNumberDisplay.textContent = `Image ${currentIndex + 1} of ${images.length}`;
        }
    }

    window.initializeGallery = (fetchedImages) => {
        images = fetchedImages;
        currentIndex = 0;
        updateGallery();
    };
});
