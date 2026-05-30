from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.request
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/parse', methods=['POST'])
def parse_video():
    data = request.json
    youtube_url = data.get('url')
    
    if not youtube_url:
        return jsonify({'error': '請提供網址'}), 400
        
    # 建立多個解析節點 (容錯機制)：如果 Render 被官方擋住，就自動切換備用社群節點
    cobalt_nodes = [
        'https://api.cobalt.tools/',
        'https://cobalt-api.peppe8o.com/',
        'https://api.cobalt.buss.lol/'
    ]
    
    last_error = "未知錯誤"
    
    for api_endpoint in cobalt_nodes:
        try:
            req = urllib.request.Request(
                api_endpoint,
                data=json.dumps({
                    "url": youtube_url,
                    "downloadMode": "audio",
                    "audioFormat": "mp3"
                }).encode('utf-8'),
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                }
            )
            
            response = urllib.request.urlopen(req)
            cobalt_data = json.loads(response.read().decode('utf-8'))
            
            if cobalt_data.get('url'):
                return jsonify({
                    'success': True,
                    'title': '🎶 雲端解析完畢，音樂準備就緒！',
                    'audio_url': cobalt_data['url']
                })
        except urllib.error.HTTPError as e:
            last_error = str(e.code)
            continue  # 遇到 403 或 404，無縫切換到陣列中的下一個節點
        except Exception as e:
            last_error = str(e)
            continue
            
    # 如果三個節點都掛了，才會回傳失敗
    return jsonify({'success': False, 'error': f'所有解析節點皆無法連線 (最後錯誤碼: {last_error})'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)