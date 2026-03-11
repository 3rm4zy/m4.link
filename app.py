from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the generated index.html"""
    return send_from_directory('html', 'index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    # Run Flask on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=False)