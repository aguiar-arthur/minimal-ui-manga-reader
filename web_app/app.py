from flask import Flask, render_template, request, jsonify
import re
import requests

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
    regex_pattern = data.get('regexPattern', IMAGE_REGEX)  # Default to existing regex if not provided
    
    try:
        content = get_content_from_url(url)
        urls = get_media_from_content(regex_pattern, content)
        
        return jsonify({"success": True, "images": urls})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def get_content_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    content = response.text
    return content

def get_media_from_content(regex_pattern, html_content):
    urls = []
        
    additional_urls = re.findall(regex_pattern, html_content)
    for img_url in additional_urls:
        urls.append(img_url)
    return urls


if __name__ == '__main__':
    app.run(debug=True)

