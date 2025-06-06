document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("toggle-theme");
    const icon = document.getElementById("theme-icon");

    // if (localStorage.getItem("theme") === "dark") {
    //     document.documentElement.classList.add("dark-mode");
    // }

    const lightIcon = toggleButton.getAttribute("data-light-icon");
    const darkIcon = toggleButton.getAttribute("data-dark-icon");

    function updateThemeIcon() {
        icon.src = document.documentElement.classList.contains("dark-mode") ? lightIcon : darkIcon;
    }

    updateThemeIcon();

    toggleButton.addEventListener("click", () => {
        document.documentElement.classList.toggle("dark-mode");
        const nuevoTema = document.documentElement.classList.contains("dark-mode") ? "dark" : "light";
        localStorage.setItem("theme", nuevoTema); 
        updateThemeIcon();
    });
});


