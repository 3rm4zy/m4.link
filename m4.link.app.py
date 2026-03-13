from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import os
import json

class CustomHTTPHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        # Strip paramaters and other bs from the URL
        path = urlparse(self.path).path

        # Health check
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            return
        
        # Serve index.html
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('html/index.html', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # 404 for everything else
        self.send_error(404)

if __name__ == '__main__':
    os.chdir('/app')
    server = HTTPServer(('0.0.0.0', 5000), CustomHTTPHandler)
    print("Server running on http://0.0.0.0:5000")
    server.serve_forever()