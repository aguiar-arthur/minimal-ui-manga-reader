import pygame
import requests
from io import BytesIO
from PIL import Image
import numpy as np

def fetch_image(url):
    """
    Fetches an image from a URL and returns it as a pygame surface.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')  # Ensure the image is in RGB format
        img_array = np.array(img)
        return pygame.surfarray.make_surface(img_array.swapaxes(0, 1))  # Convert to Pygame surface
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")
        return pygame.Surface((800, 600))  # Return an empty surface in case of error

def view_images_from_urls(image_urls):
    """
    Displays a list of images from the provided URLs, with zoom and scroll functionality.
    Parameters:
        image_urls (list): List of image URLs to display.
    """
    pygame.init()

    # Set the window to fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()  # Get current screen size
    pygame.display.set_caption("Manga Viewer")

    # Initialize variables for zoom and scroll
    zoom_factor = 1.0  # Start with no zoom
    offset_x, offset_y = 0, 0  # Scroll offset
    current_index = 0  # To track the image being displayed

    # Fetch the first image
    image_surface = fetch_image(image_urls[current_index])

    # Main loop
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fill screen with black
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse scroll for scrolling
                if event.button == 4:  # Scroll up (move image up)
                    offset_y += 10
                elif event.button == 5:  # Scroll down (move image down)
                    offset_y -= 10
            elif event.type == pygame.KEYDOWN:  # Keypress for zoom
                if event.key == pygame.K_EQUALS:  # Plus key for zoom in
                    zoom_factor *= 1.1
                elif event.key == pygame.K_MINUS:  # Minus key for zoom out
                    zoom_factor /= 1.1

        # Get original image dimensions
        original_width, original_height = image_surface.get_size()

        # Scale image to fit the screen if it is larger
        if original_width > SCREEN_WIDTH or original_height > SCREEN_HEIGHT:
            scaling_factor = min(SCREEN_WIDTH / original_width, SCREEN_HEIGHT / original_height)
            new_width = int(original_width * scaling_factor * zoom_factor)
            new_height = int(original_height * scaling_factor * zoom_factor)
            scaled_image = pygame.transform.smoothscale(image_surface, (new_width, new_height))
        else:
            # Keep the original size for smaller images
            if zoom_factor != 1.0:
                new_width = int(original_width * zoom_factor)
                new_height = int(original_height * zoom_factor)
                scaled_image = pygame.transform.smoothscale(image_surface, (new_width, new_height))
            else:
                scaled_image = image_surface

        # Adjust the image position to simulate scrolling
        image_rect = scaled_image.get_rect(center=(SCREEN_WIDTH // 2 + offset_x, SCREEN_HEIGHT // 2 + offset_y))

        # Draw the image
        screen.blit(scaled_image, image_rect)

        # Update the screen
        pygame.display.flip()

        # Handle key events for navigation
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:  # Right arrow for next image
            current_index = (current_index + 1) % len(image_urls)
            image_surface = fetch_image(image_urls[current_index])
        elif keys[pygame.K_LEFT]:  # Left arrow for previous image
            current_index = (current_index - 1) % len(image_urls)
            image_surface = fetch_image(image_urls[current_index])

    pygame.quit()
