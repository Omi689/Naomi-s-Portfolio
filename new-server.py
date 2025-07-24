#!/usr/bin/env python3
"""
Simple HTTP server for Naomi Musalaba's Portfolio Website
Serves the new professional portfolio with proper MIME types
"""

import http.server
import socketserver
import os
import mimetypes

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Serve new-portfolio.html as the default page
        if self.path == '/' or self.path == '/index.html':
            self.path = '/new-portfolio.html'
        
        # Set proper MIME types
        if self.path.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            try:
                with open(self.path[1:], 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404)
            return
        
        if self.path.endswith('.js'):
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            try:
                with open(self.path[1:], 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404)
            return
        
        super().do_GET()

def run_server(port=8001):
    """Run the portfolio server"""
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"Naomi's Portfolio Server running at http://localhost:{port}")
            print(f"Serving files from: {os.path.dirname(os.path.abspath(__file__))}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {port} is already in use. Trying port {port + 1}...")
            run_server(port + 1)
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    run_server()
