from flask import Flask, request, send_from_directory
from flask import Flask, request
import requests

app = Flask(__name__)

sureler = {
    "fatiha": 1,
    "bakara": 2,
    "yasin": 36,
    "rahman": 55,
    "mulk": 67,
    "nebe": 78,
    "nas": 114
}

@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2e7d32">
<link rel="manifest" href="/manifest.json">
<style>
body {
    font-family: Arial;
    background-color: #f2f2f2;
    padding: 20px;
    text-align: center;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
input {
    width: 80%;
    padding: 12px;
    margin-top: 10px;
    font-size: 16px;
}
button {
    padding: 12px 20px;
    margin-top: 10px;
    font-size: 16px;
    background: #2e7d32;
    color: white;
    border: none;
    border-radius: 6px;
}
</style>
</head>
<body>

<div class="card">
    <h2>📖 Kuran Uygulaması</h2>
    <form action="/sure">
        <input name="query" placeholder="Sure adı veya numarası">
        <br>
        <button type="submit">Ara</button>
    </form>
    <p>Örnek: yasin, rahman, 1</p>
</div>

</body>
</html>
"""

@app.route("/sure")
def get_sure():
    query = request.args.get("query")

    if not query:
        return "Sure giriniz"

    query = query.lower().strip()

    if query.isdigit():
        sure_id = query
    else:
        if query in sureler:
            sure_id = sureler[query]
        else:
            return "Sure bulunamadı"

    arabic_url = f"https://api.alquran.cloud/v1/surah/{sure_id}/ar"
    turkish_url = f"https://api.alquran.cloud/v1/surah/{sure_id}/tr.diyanet"
    translit_url = f"https://api.alquran.cloud/v1/surah/{sure_id}/en.transliteration"

    arabic_data = requests.get(arabic_url).json()
    turkish_data = requests.get(turkish_url).json()
    translit_data = requests.get(translit_url).json()

    sure_adi = arabic_data["data"]["englishName"]
    arabic_ayahs = arabic_data["data"]["ayahs"]
    turkish_ayahs = turkish_data["data"]["ayahs"]
    translit_ayahs = translit_data["data"]["ayahs"]

    arabic_text = " ".join([a["text"] for a in arabic_ayahs])
    turkish_text = " ".join([t["text"] for t in turkish_ayahs])
    translit_text = " ".join([tr["text"] for tr in translit_ayahs])

    audio_url = f"https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy/{sure_id}.mp3"

    result = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{
    font-family: Arial;
    background-color: #f2f2f2;
    padding: 15px;
}}
.card {{
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}
.arabic {{
    font-size: 26px;
    text-align: right;
    line-height: 2;
}}
.translit {{
    font-size: 18px;
    font-style: italic;
    line-height: 1.8;
}}
.meal {{
    font-size: 18px;
    line-height: 1.8;
}}
audio {{
    width: 100%;
}}
</style>
</head>
<body>

<div class="card">
<h2>{sure_adi} Suresi</h2>

<h3>Dinle</h3>
<audio controls>
    <source src="{audio_url}" type="audio/mpeg">
</audio>

<h3>Arapça</h3>
<p class="arabic">{arabic_text}</p>

<h3>Okunuş</h3>
<p class="translit">{translit_text}</p>

<h3>Türkçe Meal</h3>
<p class="meal">{turkish_text}</p>

</div>
</body>
</html>
"""

    return result

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
