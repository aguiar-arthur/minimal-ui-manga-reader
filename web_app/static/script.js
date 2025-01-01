document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const fetchButton = document.getElementById('fetchButton');
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const imageDisplay = document.getElementById('imageDisplay');
    const imageWidthInput = document.getElementById('imageWidth');
    const imageHeightInput = document.getElementById('imageHeight');
    const statusMessage = document.getElementById('statusMessage');
    const regexPatternInput = document.getElementById('regexPattern');
    const jsonPatternInput = document.getElementById('jsonPattern');
    const endpointSelect = document.getElementById('endpointSelect');
    const imageNumberDisplay = document.createElement('div');

    let images = [];
    let currentIndex = 0;

    // Set default width and height for the image
    imageDisplay.style.width = `${imageWidthInput.value}px`;
    imageDisplay.style.height = `${imageHeightInput.value}px`;

    // Append the image number display to the gallery container
    document.querySelector('#gallery').appendChild(imageNumberDisplay);

    fetchButton.addEventListener('click', async () => {
        const url = urlInput.value;
        const selectedEndpoint = endpointSelect.value; // Get the selected endpoint
        const regexPattern = regexPatternInput.value || '';
        const jsonPattern = jsonPatternInput.value || '';

        if (!url) {
            statusMessage.textContent = "Please enter a valid URL.";
            return;
        }

        statusMessage.textContent = "Fetching images...";

        const requestBody = {
            url,
            ...(selectedEndpoint === '/regex/extract-media' && { regexPattern }),
            ...(selectedEndpoint === '/json/extract-media' && { jsonPattern }),
        };

        try {
            const response = await fetch(selectedEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody),
            });
            const result = await response.json();

            if (result.success) {
                images = result.images;
                if (images.length > 0) {
                    currentIndex = 0;
                    updateGallery();
                    statusMessage.textContent = "";
                } else {
                    statusMessage.textContent = "No images found.";
                }
            } else {
                statusMessage.textContent = `Error: ${result.error}`;
            }
        } catch (error) {
            statusMessage.textContent = "An error occurred while fetching images.";
        }
    });

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
        if (images.length === 0) return;

        currentIndex += direction;

        if (currentIndex < 0) {
            currentIndex = 0;
        } else if (currentIndex >= images.length) {
            currentIndex = images.length - 1;
        }

        updateGallery();
    }

    function updateGallery() {
        if (images.length === 0) {
            imageDisplay.style.display = 'none';
            prevButton.disabled = true;
            nextButton.disabled = true;
            imageNumberDisplay.textContent = ''; // Clear image number if no images
        } else {
            imageDisplay.src = images[currentIndex];
            imageDisplay.style.width = `${imageWidthInput.value}px`;
            imageDisplay.style.height = `${imageHeightInput.value}px`;
            imageDisplay.style.display = 'block';
            prevButton.disabled = currentIndex === 0;
            nextButton.disabled = currentIndex === images.length - 1;

            // Update the image number display
            imageNumberDisplay.textContent = `Image ${currentIndex + 1} of ${images.length}`;
        }
    }
});
