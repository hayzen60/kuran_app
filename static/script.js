// Sure isimleri
const surahNames = {
    "1": "Fatiha",
    "2": "Bakara",
    "36": "Yasin",
    "55": "Rahman",
    "67": "Mülk",
    "78": "Nebe",
    "114": "Nas"
};

// Bölüm aç / kapat
function toggleSection(id) {
    const el = document.getElementById(id);
    if (!el) return;

    if (el.style.display === "block") {
        el.style.display = "none";
    } else {
        el.style.display = "block";
    }
}

// Favoriye ekle / kaldır
function toggleFavorite(sureId) {
    let favs = JSON.parse(localStorage.getItem("favorites")) || [];

    if (favs.includes(sureId)) {
        favs = favs.filter(s => s !== sureId);
        alert("Favorilerden kaldırıldı");
    } else {
        favs.push(sureId);
        alert("Favorilere eklendi");
    }

    localStorage.setItem("favorites", JSON.stringify(favs));
}

// Ana sayfada favorileri göster
document.addEventListener("DOMContentLoaded", function () {
    const list = document.getElementById("favoritesList");
    if (!list) return;

    const favs = JSON.parse(localStorage.getItem("favorites")) || [];
    list.innerHTML = "";

    if (favs.length === 0) {
        list.innerHTML = "<p>Henüz favori yok</p>";
        return;
    }

    favs.forEach(function (sureId) {
        const btn = document.createElement("button");

        btn.textContent = surahNames[sureId] || ("Sure " + sureId);
        btn.style.marginTop = "8px";

        btn.onclick = function () {
            window.location.href = "/sure?query=" + sureId;
        };

        list.appendChild(btn);
    });
});

// Son okunan sureyi kaydet
function saveLastRead(sureId) {
    localStorage.setItem("lastRead", sureId);
}

// Ana sayfada son okunanı göster
document.addEventListener("DOMContentLoaded", function () {
    const last = localStorage.getItem("lastRead");
    const container = document.getElementById("lastReadSection");

    if (!container) return;
    if (!last) return;

    const btn = document.createElement("button");
    btn.textContent = "Son Okunan: " + (surahNames[last] || ("Sure " + last));
    btn.style.marginTop = "10px";

    btn.onclick = function () {
        window.location.href = "/sure?query=" + last;
    };

    container.appendChild(btn);
});
