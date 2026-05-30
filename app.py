from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # 允許跨網域存取，這樣你的 APK 才連得進來

@app.route('/api/parse', methods=['POST'])
def parse_video():
    data = request.json
    youtube_url = data.get('url')
    
    if not youtube_url:
        return jsonify({'error': '請提供網址'}), 400
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        # 加入這行偽裝參數，騙過 YouTube 的機器人檢查
        'extractor_args': {
            'youtube': ['client=ANDROID']
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            # 取得 YouTube 的直連音訊串流網址
            audio_url = info.get('url')
            title = info.get('title', '未知歌曲')
            
            return jsonify({
                'success': True,
                'title': title,
                'audio_url': audio_url
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # 在本地測試時啟動，部署到雲端時雲端平台會自動指定 port
    app.run(host='0.0.0.0', port=5000)