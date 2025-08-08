from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return {'status': 'ok', 'message': 'Minimal Flask app is running'}

@app.route('/health')
def health():
    return {'status': 'healthy', 'port': os.getenv('PORT', 'unknown')}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
