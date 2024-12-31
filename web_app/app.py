from flask import Flask, render_template, request, jsonify
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Regex pattern to match .jpg URLs
IMAGE_REGEX = r'(https?://[^\s]+?\.jpg)'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-images', methods=['POST'])
def fetch_images():
    data = request.json
    url = data.get('url')
    
    try:
        # Fetch the URL content
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        
        # Use BeautifulSoup to parse the content
        soup = BeautifulSoup(html_content, 'html.parser')
        urls = []

        # Extract <img> tags in the order they appear
        for img_tag in soup.find_all('img', src=True):
            img_url = img_tag['src']
            if img_url.endswith('.jpg'):
                urls.append(img_url)
        
        # Fallback: Add additional .jpg URLs from the raw HTML (regex order preserved)
        additional_urls = re.findall(IMAGE_REGEX, html_content)
        for img_url in additional_urls:
            if img_url not in urls:  # Avoid duplicates
                urls.append(img_url)
        
        return jsonify({"success": True, "images": urls})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)

