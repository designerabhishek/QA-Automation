#!/usr/bin/env python3
"""
Simple deployment test script to verify the app works without Selenium.
This helps isolate whether the 502 error is from Selenium/Chrome or the Flask app itself.
"""

from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return {'status': 'ok', 'message': 'Flask app is running'}

@app.route('/health')
def health():
    return {'status': 'healthy'}

@app.route('/test')
def test():
    return {'test': 'success', 'port': os.getenv('PORT', 'unknown')}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
