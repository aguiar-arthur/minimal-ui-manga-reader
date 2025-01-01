from flask import Flask, render_template, request, jsonify
from lxml import html
import re
import requests

app = Flask(__name__)

IMAGE_REGEX = r'(https?://[^\s]+?\.jpg)'
JSON_PROP = 'page_url'
LXML = '//img/@src'

def get_response_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

@app.route('/regex')
def index_regex():
    return render_template('regex.html')

@app.route('/json')
def index_json():
    return render_template('json.html')

@app.route('/lxml')
def html_json():
    return render_template('lxml.html')

@app.route('/regex/extract-media', methods=['POST'])
def regex_fetch_images():
    data = request.json
    url = data.get('url')
    
    try:
        response = get_response_from_url(url)

        content = response.text
        regex_pattern = data.get('regexPattern', IMAGE_REGEX)
        urls = get_media_from_raw_text(regex_pattern, content)

        return jsonify({"success": True, "images": urls})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/json/extract-media', methods=['POST'])
def json_fetch_images():
    data = request.json
    url = data.get('url')
    try:
        response = get_response_from_url(url)

        json_pattern = data.get('jsonPattern', JSON_PROP)
        content = response.json()
        
        if (data.get('jsonFilter')):
            filter = data.get('jsonFilter')
            content = content.get(filter)

        urls =  get_from_json(content, json_pattern)

        return jsonify({"success": True, "images": urls})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/lxml/extract-media', methods=['POST'])
def html_fetch_images():
    data = request.json
    url = data.get('url')
    
    try:
        response = get_response_from_url(url)

        content = response.text
        lxml = data.get('lxmlQuery', LXML)

        urls = get_from_html(content, lxml)

        return jsonify({"success": True, "images": urls})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def get_media_from_raw_text(regex_pattern, html_content):
    urls = []
        
    additional_urls = re.findall(regex_pattern, html_content)
    for img_url in additional_urls:
        urls.append(img_url)
    return urls

def get_from_json(content, json_pattern): 
    urls = []

    for json in content:
        urls.append(json.get(json_pattern))

    return urls

def get_from_html(content, lxml): 
    tree = html.fromstring(content)
    urls = tree.xpath(lxml)

    return urls


if __name__ == '__main__':
    app.run(debug=True)

