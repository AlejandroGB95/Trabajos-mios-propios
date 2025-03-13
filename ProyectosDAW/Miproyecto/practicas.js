 // script.js

 function toggleMenu(menuId) {
    var menu = document.getElementById(menuId);
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

function search(event) {
    // Capturamos la tecla 'Enter' (keyCode 13)
    if (event.keyCode === 13) {
        var query = document.getElementById('searchInput').value;
        if (query) {
            // Redirige a Google con el término de búsqueda
            window.location.href = 'https://www.google.com/search?q=' + encodeURIComponent(query);
        }
    }
}

// Cierra el menú desplegable si se hace clic fuera de él
window.onclick = function(event) {
    if (!event.target.matches('.menu-btn')) {
        var dropdowns = document.getElementsByClassName("menu-dropdown");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
}

function holamundo(){
    alert("Hola, esto es un trabajo para el medac y para mi portafolio, te apetece ver un capitulo de Solo leveling ?")}
    holamundo();