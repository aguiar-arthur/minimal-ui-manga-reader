from image_viewer import view_images_from_urls
from lxml import html
import requests
import jmespath

JSON_PROP = '[*].image'
LXML = '//img/@src'
URL = ""

def get_response_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def filter_valid_image_urls(image_urls):
    """
    Filters the list of image URLs to return only those with valid image file extensions.

    Parameters:
        image_urls (list): List of image URLs to filter.
    
    Returns:
        list: Filtered list containing only valid image URLs.
    """
    # List of valid image file extensions (common ones)
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg')

    # Use regular expression to filter URLs with valid image extensions
    filtered_urls = [
        url for url in image_urls if url.lower().endswith(valid_extensions)
    ]
    
    return filtered_urls

def html_fetch_images():
    """
    Extracts data from HTML using XPath queries.

    :return: JSON response with extracted data or an error message.
    """

    # Fetch the content from the URL
    response = get_response_from_url(URL)
    content = response.text
    tree = html.fromstring(content)

    # Apply the XPath query to extract data
    result = tree.xpath(LXML)
    view_images_from_urls(filter_valid_image_urls(result))

def json_query():
    """
    Processes a JSON query and returns the result.

    :return: JSON response with the queried result or an error message.
    """
    response = get_response_from_url(URL)
    content = response.json()
    result = jmespath.search(JSON_PROP, content)
    view_images_from_urls(filter_valid_image_urls(result))

