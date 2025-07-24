#!/usr/bin/env python3
"""
Simple HTTP server to serve Naomi Musalaba's portfolio website locally.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Configuration
PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    """Start the local development server."""
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"* Naomi Musalaba's Portfolio Server")
            print(f"* Serving directory: {DIRECTORY}")
            print(f"* Server running at: http://localhost:{PORT}")
            print(f"* Mobile access: http://<your-ip>:{PORT}")
            print(f"* Opening browser...")
            print(f"* Press Ctrl+C to stop the server")
            print("-" * 50)
            
            # Open browser automatically
            webbrowser.open(f'http://localhost:{PORT}')
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n* Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"* Port {PORT} is already in use. Try a different port.")
            print(f"* You can modify the PORT variable in this script.")
        else:
            print(f"* Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
