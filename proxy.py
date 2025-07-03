from flask import Flask, request, Response, render_template_string, redirect, url_for
import requests
from urllib.parse import urlparse, urljoin
import logging
from bs4 import BeautifulSoup

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Secure Web Gateway</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { background: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
    .container { background: #1e1e1e; padding: 30px; border-radius: 12px; box-shadow: 0 0 20px rgba(0,0,0,0.6); width: 100%; max-width: 400px; text-align: center; }
    .logo { font-size: 24px; margin-bottom: 20px; color: #00c4cc; font-weight: bold; }
    input, button { width: 100%; padding: 12px; margin-top: 10px; border-radius: 6px; border: none; font-size: 16px; }
    input { background: #2c2c2c; color: #fff; }
    button { background: #00c4cc; color: #000; cursor: pointer; }
    button:hover { background: #00e6e6; }
    footer { margin-top: 20px; font-size: 12px; color: #777; }
  </style>
</head>
<body>
  <div class="container">
    <div class="logo">Secure Access Gateway</div>
    <form action="/proxy" method="get">
      <input type="text" name="url" placeholder="https://example.com" required>
      <button type="submit">接続</button>
    </form>
    <footer>© 2025 SafeConnect</footer>
  </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/proxy')
def proxy():
    target_url = request.args.get("url")
    if not target_url:
        return "URLが指定されていません", 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "ja,en;q=0.9",
            "Referer": "https://www.google.com/"
        }
        r = requests.get(target_url, headers=headers, timeout=6)
        content_type = r.headers.get('Content-Type', '')

        if "text/html" in content_type:
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup.find_all(["a", "link", "script", "img", "form"]):
                attr = "href" if tag.name in ["a", "link"] else "src" if tag.name in ["script", "img"] else "action" if tag.name == "form" else None
                if attr and tag.has_attr(attr):
                    raw = tag[attr]
                    if raw.startswith("http"):
                        proxied_url = f"/proxy?url={raw}"
                    else:
                        joined = urljoin(target_url, raw)
                        proxied_url = f"/proxy?url={joined}"
                    tag[attr] = proxied_url
            return str(soup)
        else:
            return Response(r.content, status=r.status_code, content_type=content_type)

    except Exception as e:
        return f"⚠️ アクセスエラー: {e}", 500
