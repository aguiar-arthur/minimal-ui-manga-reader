import requests
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from io import BytesIO
from PIL import Image

def view_images_from_urls(image_urls):
    """
    Displays a list of images from the provided URLs, with buttons and keyboard navigation support.
    Parameters:
        image_urls (list): List of image URLs to display.
        img_width (int): Desired width of the displayed image.
        img_height (int): Desired height of the displayed image.
    """
    # Initialize index to track the current image
    current_index = 0

    # Fetch the image from the URL
    def fetch_image(url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img_array = np.array(img)
        return img_array

    # Function to update the image plot
    def update_image():
        img_array = fetch_image(image_urls[current_index])
        ax.imshow(img_array)
        ax.axis('off')  # Hide axes
        plt.draw()

    # Function for the "Next" button
    def next_image(event):
        nonlocal current_index
        current_index = (current_index + 1) % len(image_urls)  # Loop back to the first image
        update_image()

    # Function for the "Previous" button
    def prev_image(event):
        nonlocal current_index
        current_index = (current_index - 1) % len(image_urls)  # Loop back to the last image
        update_image()

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

    # Create buttons for navigation
    ax_next = plt.axes([0.8, 0.01, 0.1, 0.075])  # Next button position
    ax_prev = plt.axes([0.1, 0.01, 0.1, 0.075])  # Previous button position

    button_next = Button(ax_next, 'Next')
    button_prev = Button(ax_prev, 'Previous')

    # Attach button click events
    button_next.on_clicked(next_image)
    button_prev.on_clicked(prev_image)

    # Connect the key press events to the callback function
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Show the plot
    plt.show()
