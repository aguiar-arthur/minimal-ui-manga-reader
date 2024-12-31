document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const fetchButton = document.getElementById('fetchButton');
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const imageDisplay = document.getElementById('imageDisplay');
    const imageWidthInput = document.getElementById('imageWidth');
    const imageHeightInput = document.getElementById('imageHeight');
    const statusMessage = document.getElementById('statusMessage');
    
    let images = [];
    let currentIndex = 0;

    fetchButton.addEventListener('click', async () => {
        const url = urlInput.value;
        if (!url) {
            statusMessage.textContent = "Please enter a valid URL.";
            return;
        }

        statusMessage.textContent = "Fetching images...";
        try {
            const response = await fetch('/fetch-images', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
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
            statusMessage.textContent = "An error occurred.";
        }
    });

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) currentIndex--;
        updateGallery();
    });

    nextButton.addEventListener('click', () => {
        if (currentIndex < images.length - 1) currentIndex++;
        updateGallery();
    });

    // Update image width when the input value changes
    imageWidthInput.addEventListener('input', () => {
        if (imageDisplay.src) {
            imageDisplay.style.width = `${imageWidthInput.value}px`;
        }
    });

    // Update image height when the input value changes
    imageHeightInput.addEventListener('input', () => {
        if (imageDisplay.src) {
            imageDisplay.style.height = `${imageHeightInput.value}px`;
        }
    });

    function updateGallery() {
        if (images.length === 0) {
            imageDisplay.style.display = 'none';
            prevButton.disabled = true;
            nextButton.disabled = true;
        } else {
            imageDisplay.src = images[currentIndex];
            imageDisplay.style.width = `${imageWidthInput.value}px`; // Set initial width
            imageDisplay.style.height = `${imageHeightInput.value}px`; // Set initial height
            imageDisplay.style.display = 'block';
            prevButton.disabled = currentIndex === 0;
            nextButton.disabled = currentIndex === images.length - 1;
        }
    }
});
