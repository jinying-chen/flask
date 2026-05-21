from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World!'  # 首頁要有內容

if __name__ == '__main__':
    app.run()