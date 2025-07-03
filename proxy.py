from flask import Flask, request, Response, render_template_string
import requests
import logging

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
    url = request.args.get("url")
    if not url:
        return "URLが指定されていません", 400
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "ja,en;q=0.9",
            "Referer": "https://www.google.com/"
        }
        r = requests.get(url, headers=headers, timeout=6)
        return Response(r.content, status=r.status_code, content_type=r.headers.get('Content-Type', 'text/html'))
    except Exception as e:
        return f"⚠️ アクセスエラー: {e}", 500

