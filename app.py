from flask import Flask, send_file

app = Flask(__name__)

# 當有人連線到你的 Render 網址時，直接把漂亮的 App 介面派發給他
@app.route('/')
def home():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)