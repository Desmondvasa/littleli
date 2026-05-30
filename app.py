from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import urllib.request
import json
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/api/parse', methods=['POST'])
def parse_video():
    data = request.json
    youtube_url = data.get('url')
    
    if not youtube_url:
        return jsonify({'error': '請提供網址'}), 400
        
    match = re.search(r'(?:youtu\.be\/|v=|\/v\/|embed\/|\?v=|\&v=)([0-9A-Za-z_-]{11})', youtube_url)
    if not match:
        return jsonify({'error': '無效的 YouTube 網址'}), 400
        
    video_id = match.group(1)
    
    cobalt_nodes = [
        "https://cobalt-api.peppe8o.com",
        "https://api.cobalt.buss.lol",
        "https://co.e-z.host"
    ]
    
    for node in cobalt_nodes:
        try:
            req = urllib.request.Request(
                node,
                data=json.dumps({"url": f"https://www.youtube.com/watch?v={video_id}", "downloadMode": "audio", "aFormat": "mp3"}).encode('utf-8'),
                headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
            )
            response = urllib.request.urlopen(req, timeout=5)
            info = json.loads(response.read().decode('utf-8'))
            if 'url' in info:
                return jsonify({'success': True, 'title': '🎶 音樂準備就緒', 'audio_url': info['url']})
        except:
            continue

    piped_nodes = [
        "https://pipedapi.kavin.rocks",
        "https://pipedapi.smnz.de",
        "https://api.piped.projectsegfau.lt"
    ]
    
    for node in piped_nodes:
        try:
            req = urllib.request.Request(f"{node}/streams/{video_id}", headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=5)
            info = json.loads(response.read().decode('utf-8'))
            if 'audioStreams' in info and len(info['audioStreams']) > 0:
                audio_url = next((s['url'] for s in info['audioStreams'] if 'mp4a' in s.get('mimeType', '')), info['audioStreams'][0]['url'])
                return jsonify({'success': True, 'title': info.get('title', '🎶 音樂準備就緒'), 'audio_url': audio_url})
        except:
            continue

    return jsonify({'success': False, 'error': '所有雲端節點皆忙碌中，請稍後再試'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)