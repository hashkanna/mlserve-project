#!/usr/bin/env python3
"""Simple HTTP server to serve the MLServe UI."""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path


class UIHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for serving the UI with proper MIME types."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="ui", **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


def main():
    """Start the UI server."""
    # Check if UI directory exists
    ui_dir = Path("ui")
    if not ui_dir.exists():
        print("❌ UI directory not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    if not (ui_dir / "index.html").exists():
        print("❌ index.html not found in ui/ directory!")
        sys.exit(1)
    
    PORT = 3000
    
    try:
        with socketserver.TCPServer(("", PORT), UIHandler) as httpd:
            print("🚀 MLServe UI Server Starting...")
            print("=" * 50)
            print(f"📱 UI URL: http://localhost:{PORT}")
            print(f"🔗 API URL: http://localhost:8000")
            print(f"📊 Ray Dashboard: http://localhost:8265")
            print("=" * 50)
            print()
            print("🎯 Demo Instructions:")
            print("1. Make sure your MLServe API is running (python main.py)")
            print("2. Open the UI in your browser")
            print("3. Try image classification with sample images")
            print("4. Run load tests to see autoscaling")
            print("5. Check Ray Dashboard for detailed metrics")
            print()
            print("Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Try to open browser automatically
            try:
                webbrowser.open(f"http://localhost:{PORT}")
                print("🌐 Opening browser automatically...")
            except:
                print("💡 Please open http://localhost:3000 in your browser")
            
            print()
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("Thank you for using MLServe!")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use!")
            print("Please stop other applications using this port or use a different port.")
        else:
            print(f"❌ Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()