import requests
import matplotlib.pyplot as plt
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
        ax.imshow(img_array)  # Display the image with default aspect ratio
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

    # Create the plot with a larger figure size (adjust width and height as needed)
    fig, ax = plt.subplots(figsize=(16, 12))  # Size in inches (width, height)

    # Set the aspect ratio to 'auto' to scale the image to fit within the plot
    ax.set_aspect('auto', adjustable='box')

    # Update the image with the first one
    update_image()

    # Set the figure to fullscreen mode
    fig_manager = plt.get_current_fig_manager()
    fig_manager.full_screen_toggle()
    
    # Connect the key press events to the callback function
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Remove padding/margins to fit image better
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Show the plot
    plt.show()
