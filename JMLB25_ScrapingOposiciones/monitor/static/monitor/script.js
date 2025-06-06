function aplicarFiltroDesdeSidebar(tab) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set("tab", tab);
    window.location.search = urlParams.toString();
}

function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
        const c = cookies[i].trim();
        if (c.startsWith(name + "=")) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return "";
}

document.addEventListener('DOMContentLoaded', () => {

    const navButtons = Array.from(document.querySelectorAll('.windows .barra button'));
    const params = new URLSearchParams(window.location.search);
    const activeTab = params.get('tab') || 'todos';

    navButtons.forEach(button => {
        const filter = button.getAttribute('data-filtro');

        //Filtros Genéricos
        if (button.id === 'filtros-genericos') {
            if (window.location.pathname.includes('filtros_genericos')) {
                button.classList.add('activo');
            } else {
                button.classList.remove('activo');
            }
            return;
        }

        if (filter === activeTab) {
            button.classList.add('activo');
        } else {
            button.classList.remove('activo');
        }

        button.addEventListener('click', () => {
            navButtons.forEach(b => {
                if (b.id !== 'filtros-genericos') {
                    b.classList.remove('activo');
                }
            });
            button.classList.add('activo');

            const newFilter = button.getAttribute('data-filtro');
            const newURL = new URL(window.location);
            newURL.searchParams.set('tab', newFilter);
            window.location.href = newURL.toString();
        });
    });

    //Barra lateral
    const sidebar = document.getElementById('sidebar');
    const toggleLateralButton = document.getElementById('toggle-lateral');

    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    if (isCollapsed) {
        sidebar.classList.add('collapsed');
    } else {
        sidebar.classList.remove('collapsed');
    }

    if (toggleLateralButton) {
        toggleLateralButton.addEventListener('click', () => {
            const collapsed = sidebar.classList.toggle('collapsed');
            localStorage.setItem('sidebar-collapsed', collapsed);
        });
    }

    if (document.getElementById("urlbutton")) {
        document.getElementById("urlbutton").addEventListener("click", () => aplicarFiltroDesdeSidebar("todos"));
    }
    if (document.getElementById("boletinbutton")) {
        document.getElementById("boletinbutton").addEventListener("click", () => aplicarFiltroDesdeSidebar("boe"));
    }

    // Botón Filtros
    const filterToggle = document.getElementById('filter-toggle');
    const filterOptions = document.getElementById('filter-options');

    if (filterToggle && filterOptions) {
        filterToggle.addEventListener('click', () => {
            filterOptions.style.display = (filterOptions.style.display === 'none') ? 'block' : 'none';
        });
    }

    //Filtro MD5
    const filterMd5 = document.getElementById("filter-md5");
    if (filterMd5) {
        filterMd5.addEventListener("click", async function () {
            const texto = prompt("Introduce el texto para calcular su hash MD5:");
            if (texto) {
                if (typeof md5 !== 'undefined') {
                    const hash = await md5(texto);
                    alert("Hash MD5:\n" + hash);
                } else {
                    alert("Error: La librería MD5 no está cargada. Asegúrate de que 'js-md5.min.js' está incluido.");
                }
            }
        });
    }

    //Filtro General
    const filterGeneral = document.getElementById("filter-general");
    if (filterGeneral) {
        filterGeneral.addEventListener("click", function () {
            alert("Filtro general activado (simulado)");
        });
    }

    //Filtro por Palabras Clave
    const filterKeywords = document.getElementById("filter-keywords");
    if (filterKeywords) {
        filterKeywords.addEventListener("click", function () {
            alert("Filtro por palabras clave activado (simulado)");
        });
    }

    // nuevo codigo Alejandro 19/5/2025 se implementa codigo para guardar el check y que se quede guardado
    document.querySelectorAll('input.check').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const formData = new FormData();
            formData.append('id', this.value);
            formData.append('estado', this.checked);
            fetch('/ajax/marcar/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert('Error al guardar el estado del checkbox.');
                }
            });
        });
    });

    //Buscador
    const searchInput = document.getElementById("urlInput");
    const savedQuery = localStorage.getItem("searchQuery");
    if (searchInput && savedQuery) {
        searchInput.value = savedQuery;
    }

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            localStorage.setItem("searchQuery", searchInput.value);
        });
    }

    const resetButton = document.getElementById("icon-button");
    if (resetButton) {
        resetButton.addEventListener("click", function() {
            if (searchInput) {
                searchInput.value = "";
            }
            localStorage.removeItem("searchQuery");

            const currentTab = new URLSearchParams(window.location.search).get('tab') || 'todos';
            window.location.href = `?tab=${currentTab}`;
        });
    }

});