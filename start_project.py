import http.server
import urllib.parse
import urllib.request
import sys
import json
import os

PORT = 8000

class GameProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        local_path = urllib.parse.unquote(self.path.split('?')[0]).lstrip('/')
        if not local_path:
            local_path = 'index.html'

        # Check local file availability
        is_missing = False
        if not os.path.exists(local_path):
            is_missing = True
        else:
            if os.path.getsize(local_path) < 1024:
                try:
                    with open(local_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if "No Content:" in f.read(200):
                            is_missing = True
                except Exception:
                    pass
        
        if self.path.startswith('/template/'):
            is_missing = True

        if is_missing:
            # DO NOT use urllib.parse.quote here because self.path already contains ?query=string and is properly encoded by the browser!
            live_url = "https://thinghiemvui.basf.com" + self.path
            
            # TRUE PROXY for small files prone to CORS issues in XHR (templates, fonts)
            if self.path.startswith('/template/') or self.path.startswith('/fonts/'):
                try:
                    import ssl
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE

                    print(f"[*] True Proxy fetching: {live_url}")
                    req = urllib.request.Request(live_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')
                        if 'Content-Type' in response.headers:
                            self.send_header('Content-Type', response.headers['Content-Type'])
                        self.end_headers()
                        self.wfile.write(response.read())
                    return
                except Exception as e:
                    print(f"[*] True Proxy failed: {e}")
                    self.send_error(404, "Proxy failed to fetch")
                    return

            # 302 REDIRECT for large files (videos) compatible with <video src="...">
            self.send_response(302)
            self.send_header('Location', live_url)
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            print(f"[*] Redirected missing large asset to live server: {self.path}")
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            self.rfile.read(content_length)

        if '/user/' in self.path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
        else:
            self.send_error(501, "Unsupported method ('POST')")

try:
    with http.server.ThreadingHTTPServer(("", PORT), GameProxyHandler) as httpd:
        print(f"[*] SMART HYBRID + TRUE PROXY Server running at http://localhost:{PORT}")
        httpd.serve_forever()
except OSError as e:
    print(f"Error: {e}. Port {PORT} is already in use.")
    sys.exit(1)
