   function editarFiltro(id, nombre, palabras) {
            document.getElementById('filtro_id').value = id;
            document.getElementById('nuevo_filtro').value = nombre;
            document.getElementById('contenido_filtro').value = palabras;
            document.getElementById('filtro-form').action = editarFiltroUrl;
            document.getElementById('filtro-submit').textContent = "Guardar edición";
            document.getElementById('cancelar-edicion').style.display = "inline-block";
        }
    
        function cancelarEdicion() {
            document.getElementById('filtro_id').value = "";
            document.getElementById('nuevo_filtro').value = "";
            document.getElementById('contenido_filtro').value = "";
            document.getElementById('filtro-form').action = crearFiltroUrl;
            document.getElementById('filtro-submit').textContent = "Guardar";
            document.getElementById('cancelar-edicion').style.display = "none";
        }
document.addEventListener('DOMContentLoaded', function() {

    // Filtros
    const form = document.getElementById('filtro-form');
    const contenidoInput = document.getElementById('contenido_filtro');
    const errorMsg = document.getElementById('error-msg');

    const regex = /^([a-zA-ZÁÉÍÓÚáéíóúÑñ0-9]+(?:, [a-zA-ZÁÉÍÓÚáéíóúÑñ0-9]+)*)$/;

    if (form && contenidoInput && errorMsg) {
        form.addEventListener('submit', function(e) {
            const contenido = contenidoInput.value.trim();

            if (!regex.test(contenido)) {
                e.preventDefault();
                errorMsg.textContent = "Contenido incorrecto. Por favor, añade palabras separadas por coma y un espacio.";
                errorMsg.style.display = 'block';
                contenidoInput.focus();
            } else {
                errorMsg.style.display = 'none';
            }
        });

        contenidoInput.addEventListener('input', function() {
            if (regex.test(contenidoInput.value.trim())) {
                errorMsg.style.display = 'none';
            }
        });
    }

    //Funcionalidad filtros
    document.querySelectorAll('.editar-btn').forEach(button => {
        button.addEventListener('click', () => {
            const form = button.parentElement.querySelector('.form-editar');
            if (form) { 
                form.style.display = (form.style.display === 'none') ? 'block' : 'none';
            }
        });
    });

    if (typeof jQuery !== 'undefined') { 
        $(document).ready(function() {
            $('.check-filtro').change(function() {
                const id = $(this).val();
                window.location.href = `{% url 'index' %}` + `?filtro_aplicado=${id}`;
            });
        });
    }
});