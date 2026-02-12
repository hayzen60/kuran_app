function toggleSection(id) {
    var el = document.getElementById(id);
    if (el.style.display === "block") {
        el.style.display = "none";
    } else {
        el.style.display = "block";
    }
}

// Sayfa açıldığında Arapça otomatik açık olsun
window.addEventListener("DOMContentLoaded", function() {
    var arabic = document.getElementById("arabic");
    if (arabic) {
        arabic.style.display = "block";
    }
});

function toggleFavorite(sureName) {
    let favs = JSON.parse(localStorage.getItem("favorites")) || [];

    if (favs.includes(sureName)) {
        favs = favs.filter(s => s !== sureName);
        alert("Favorilerden kaldırıldı");
    } else {
        favs.push(sureName);
        alert("Favorilere eklendi");
    }

    localStorage.setItem("favorites", JSON.stringify(favs));
}
