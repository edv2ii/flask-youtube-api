from flask import Flask, request, jsonify
from flask_cors import CORS  # เพิ่มการ import นี้
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# เพิ่มการตั้งค่า CORS
CORS(app)

# หน้าแรก (Route "/")
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the YouTube Video Title API. Use /get_video_name to get video title.'})

# Route สำหรับ /get_video_name (POST method)
@app.route('/get_video_name', methods=['POST'])
def get_video_name():
    try:
        # รับ URL จาก request
        youtube_url = request.json.get('url')

        # ตรวจสอบว่ามี URL หรือไม่
        if not youtube_url:
            return jsonify({'error': 'No URL provided'}), 400

        # ใช้ requests เพื่อดึง HTML ของลิงก์
        response = requests.get(youtube_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch the YouTube page'}), 500

        # ใช้ BeautifulSoup เพื่อ parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # ดึง title ของคลิป
        title_tag = soup.find('title')
        video_title = title_tag.text.replace('- YouTube', '').strip() if title_tag else 'Unknown Title'

        return jsonify({'title': video_title})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
