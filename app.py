from flask import Flask, request, render_template
import requests

app = Flask(__name__)

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

    return render_template(
        "sure.html",
        sure_adi=sure_adi,
        arabic_text=arabic_text,
        translit_text=translit_text,
        turkish_text=turkish_text,
        audio_url=audio_url
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

