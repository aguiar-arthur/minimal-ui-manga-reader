import requests
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from io import BytesIO
from PIL import Image

def view_images_from_urls(image_urls):
    """
    Displays a list of images from the provided URLs, with keyboard navigation support.
    Parameters:
        image_urls (list): List of image URLs to display.
    """
    # Initialize index to track the current image
    current_index = 0

    # Fetch the image from the URL
    def fetch_image(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            img_array = np.array(img)
            return img_array
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image: {e}")
            return np.zeros((100, 100, 3), dtype=np.uint8)  # Placeholder blank image

    # Function to update the image plot
    def update_image():
        img_array = fetch_image(image_urls[current_index])
        ax.imshow(img_array)
        ax.axis('off')  # Hide axes
        plt.draw()

    # Function to handle keyboard arrows
    def on_key(event):
        nonlocal current_index
        if event.key == 'right':  # Right arrow for next image
            current_index = (current_index + 1) % len(image_urls)
        elif event.key == 'left':  # Left arrow for previous image
            current_index = (current_index - 1) % len(image_urls)
        update_image()

    # Create the plot
    fig, ax = plt.subplots()
    ax.axis('off')  # Hide axes initially
    update_image()  # Show the first image
    
    # Set the figure to fullscreen mode
    fig_manager = plt.get_current_fig_manager()
    fig_manager.full_screen_toggle()

    # Connect the key press events to the callback function
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Show the plot
    plt.show()
