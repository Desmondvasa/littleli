from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp

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
        
    try:
        ydl_opts = {
            'format': 'bestaudio/m4a/best/mp4',
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'cookies.txt',
            'noplaylist': True,
            'extractor_args': {
                'youtube': ['client=ANDROID'],
                'youtubetab': ['skip=authcheck']
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            
            return jsonify({
                'success': True,
                'title': info.get('title', '音樂解析成功'),
                'audio_url': info['url']
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)