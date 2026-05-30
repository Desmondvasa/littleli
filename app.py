from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import json

app = Flask(__name__)
# 開啟 CORS，允許你的網頁/APK 連線進來
CORS(app)

@app.route('/api/parse', methods=['POST'])
def parse_video():
    data = request.json
    youtube_url = data.get('url')
    
    if not youtube_url:
        return jsonify({'error': '請提供網址'}), 400
        
    try:
        # 大腦代替手機，以伺服器的身分向 Cobalt 請求
        req = urllib.request.Request(
            'https://api.cobalt.tools/api/json',
            data=json.dumps({
                "url": youtube_url,
                "isAudioOnly": True
            }).encode('utf-8'),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        )
        
        response = urllib.request.urlopen(req)
        cobalt_data = json.loads(response.read().decode('utf-8'))
        
        if 'url' in cobalt_data:
            return jsonify({
                'success': True,
                'title': '🎶 雲端解析完畢，音樂準備就緒！',
                'audio_url': cobalt_data['url']
            })
        else:
            return jsonify({'success': False, 'error': cobalt_data.get('text', '未知的解析錯誤')}), 500
            
    except urllib.error.HTTPError as e:
        return jsonify({'success': False, 'error': f'伺服器拒絕連線 (錯誤碼: {e.code})'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)