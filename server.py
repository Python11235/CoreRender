import http.server
import socketserver
import os
import sys
import signal

PORT = int(os.environ.get("PORT", 5000))

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        '': 'application/octet-stream',
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.woff2': 'font/woff2',
        '.woff': 'font/woff',
    }

    def log_message(self, format, *args):
        if args[1] != '404':
            sys.stdout.write(f"{self.client_address[0]} - {format % args}\n")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

def shutdown(sig, frame):
    print("\nShutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

httpd = ThreadedHTTPServer(("0.0.0.0", PORT), Handler)
print(f"CoreRender running on port {PORT}")
httpd.serve_forever()
