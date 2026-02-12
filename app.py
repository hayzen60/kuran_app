from flask import Flask, request, render_template
import requests
import json
import os

app = Flask(__name__)

# JSON yükle (OFFLINE VERİ)
DATA_PATH = os.path.join("data", "sureler.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    SURELER = json.load(f)

sureler = {
    "1": "Fatiha",
    "2": "Bakara",
    "3": "Ali İmran",
    "4": "Nisa",
    "5": "Maide",
    "6": "Enam",
    "7": "Araf",
    "8": "Enfal",
    "9": "Tevbe",
    "10": "Yunus",
    "36": "Yasin",
    "55": "Rahman",
    "67": "Mülk",
    "78": "Nebe",
    "114": "Nas"
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sureler")
def sure_listesi():
    return render_template("sureler.html", sureler=sureler)

@app.route("/sure")
def sure():
    query = request.args.get("query")

    if not query:
        return "Sure bulunamadı"

    query = str(query).strip()

    # JSON'da sure var mı?
    if query not in SURELER:
        return f"Sure bulunamadı: {query}"

    sure_name = SURELER[query]["name"]

    # Değişkenleri BAŞTA tanımla (çok önemli)
    arabic_text = ""
    turkish_text = ""
    translit_text = ""
    audio_url = None
    is_offline = False

    try:
        arabic_url = f"https://api.alquran.cloud/v1/surah/{query}/ar"
        turkish_url = f"https://api.alquran.cloud/v1/surah/{query}/tr.diyanet"
        translit_url = f"https://api.alquran.cloud/v1/surah/{query}/en.transliteration"

        arabic_data = requests.get(arabic_url, timeout=5).json()
        turkish_data = requests.get(turkish_url, timeout=5).json()
        translit_data = requests.get(translit_url, timeout=5).json()

        arabic_text = " ".join([a["text"] for a in arabic_data["data"]["ayahs"]])
        turkish_text = " ".join([t["text"] for t in turkish_data["data"]["ayahs"]])
        translit_text = " ".join([tr["text"] for tr in translit_data["data"]["ayahs"]])

        audio_url = f"https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy/{query}.mp3"

    except:
        arabic_text = "İnternet bağlantısı yok"
        is_offline = True

    return render_template(
        "sure.html",
        sure_adi=sure_name,
        arabic_text=arabic_text,
        translit_text=translit_text,
        turkish_text=turkish_text,
        audio_url=audio_url,
        is_offline=is_offline
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

