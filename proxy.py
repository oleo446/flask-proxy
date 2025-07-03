from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Proxy simple</title>
</head>
<body>
    <h2>Entrez l'URL que vous souhaitez afficher :</h2>
    <form method="get">
        <input type="text" name="url" size="70" placeholder="https://exemple.com">
        <input type="submit" value="Afficher">
    </form>
    <hr>
    {% if content %}
        <h3>Contenu de {{ url }}</h3>
        <div style="border:1px solid #ccc; padding:10px; max-height:600px; overflow:auto;">
            {{ content|safe }}
        </div>
    {% elif error %}
        <p style="color:red;">Erreur : {{ error }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    url = request.args.get('url')
    content = None
    error = None
    if url:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/115.0.0.0 Safari/537.36",
                "Accept-Language": "fr-FR,fr;q=0.9"
            }
            resp = requests.get(url, headers=headers, timeout=10)
            resp.encoding = resp.apparent_encoding
            content = resp.text
        except Exception as e:
            error = str(e)
    return render_template_string(HTML, url=url, content=content, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

