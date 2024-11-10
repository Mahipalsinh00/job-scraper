from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

def fetch_webpage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("Webpage fetched successfully")  # Debug statement
    return response.content

def parse_content(content, tag, class_name):
    soup = BeautifulSoup(content, 'html.parser')
    print("Parsing content")  # Debug statement
    if class_name:
        data = soup.find_all(tag, class_=class_name)
    else:
        data = soup.find_all(tag)
    print(f"Found {len(data)} items")  # Debug statement
    return [item.get_text(strip=True) for item in data]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    tag = request.form['tag']
    class_name = request.form['class_name']
    try:
        content = fetch_webpage(url)
        data = parse_content(content, tag, class_name)
        print("Scraped Data:", data)  # Debug statement

        return jsonify({'message': 'Data scraped successfully', 'data': data})
    except Exception as e:
        print(f"Error: {e}")  # Debug statement
        return jsonify({'message': f'Error: {e}'})

if __name__ == '__main__':
    app.run(debug=True)
