#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

TEXT = ""

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TextBox</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Consolas, monospace; background: #0a0a0a; color: #e0e0e0; max-width: 620px; margin: 0 auto; padding: 40px 20px; min-height: 100vh; }
h1 { font-size: 28px; color: #cc2222; margin-bottom: 24px; letter-spacing: 2px; }
textarea {
  width: 100%; height: 240px; padding: 14px; font-size: 15px; font-family: Consolas, monospace;
  background: #141414; color: #e0e0e0; border: 1px solid #2a2a2a; border-radius: 6px;
  resize: vertical; outline: none; transition: border-color 0.2s;
}
textarea:focus { border-color: #cc2222; }
textarea::placeholder { color: #555; }
.actions { display: flex; gap: 10px; margin-top: 14px; align-items: center; }
button {
  padding: 10px 22px; font-size: 14px; font-family: Consolas, monospace; cursor: pointer;
  border: 1px solid #2a2a2a; border-radius: 4px; color: #e0e0e0; background: #1a1a1a;
  transition: background 0.2s, border-color 0.2s;
}
button:hover { background: #222; border-color: #cc2222; }
button:active { background: #cc2222; color: #fff; }
#status { margin-left: auto; font-size: 13px; color: #cc2222; opacity: 0; transition: opacity 0.3s; }
#status.show { opacity: 1; }
</style>
</head>
<body>
<h1>TextBox</h1>
<textarea id="box" placeholder="Paste text here..." spellcheck="false"></textarea>
<div class="actions">
  <button onclick="save()">Save</button>
  <button onclick="copyText()">Copy</button>
  <span id="status"></span>
</div>
<script>
const box = document.getElementById('box');
const status = document.getElementById('status');
function flash(msg) {
  status.textContent = msg;
  status.classList.add('show');
  setTimeout(() => status.classList.remove('show'), 1800);
}
async function save() {
  await fetch('/text', {method: 'POST', body: box.value});
  flash('Saved');
}
async function load() {
  const r = await fetch('/text');
  box.value = await r.text();
}
function copyText() {
  box.select();
  document.execCommand('copy');
  flash('Copied');
}
load();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/text":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(TEXT.encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())

    def do_POST(self):
        global TEXT
        length = int(self.headers.get("Content-Length", 0))
        TEXT = self.rfile.read(length).decode()
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    port = 80
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Running on http://0.0.0.0:{port}")
    server.serve_forever()
