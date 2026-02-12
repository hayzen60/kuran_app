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
