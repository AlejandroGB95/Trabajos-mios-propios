<?php
 //conectar con el servidor
    $servidor = "localhost";
    $usuario = "root";
    $clave = "";
    $baseDeDatos = "trabajo";

    $enlaces = mysqli_connect ($servidor, $usuario,$clave, $baseDeDatos);
?>
<!--http://localhost/ProyectosDAW/Miproyecto/Index.php-->  <!--comentario para ver la pagina web-->
<?php
if(isset($_POST['trabajo'])){

$nombre = $_POST['nombre'];
$apellido = $_POST['apellido'];
$email = $_POST['email'];
$telefono = $_POST['telefono'];

// Sentencia SQL 
$insertarDatos = "INSERT INTO registro (nombre, apellido, email, telefono) VALUES ('$nombre', '$apellido', '$email', '$telefono')";

// Ejecución de la consulta
$ejecutarInsertar = mysqli_query($enlaces, $insertarDatos);

}

?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solo Leveling - Fan Page</title>
    <link rel="stylesheet" href="solo leveling/estilo.css">
</head>
<body>
    <!-- Contenido principal -->
    <div class="main-content">
        <section id="trailer">
            <h1>Tráiler de Solo Leveling - Temporada 2</h1>
            <div class="video-container">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/ZTA77U48F2E?si=LX2bUzqzb05QQWf2" allowfullscreen></iframe>
            </div>
        </section>

        <section id="formulario">
            <h2>Regístrate para más información</h2>
            <form action="http://localhost/ProyectosDAW/Miproyecto/registro.php" name="trabajo" method="post" class="user-form" href="index.php">
                <label for="nombre">Nombre:</label>
                <input type="text" id="nombre" name="nombre" required>

                <label for="apellido">Apellido:</label>
                <input type="text" id="apellido" name="apellido" required>

                <label for="edad">Edad:</label>
                <input type="number" id="edad" name="edad" min="10" max="100" required>

                <label for="correo">Correo Electrónico:</label>
                <input type="email" id="correo" name="email" required>

                <label for="telefono">Teléfono de Contacto:</label>
                <input type="tel" id="telefono" name="telefono" required>

                <button type="submit" name="trabajo">Enviar</button>
            </form>
        </section>

        <!-- Sección de redes sociales -->
        <section id="social">
            <h2>Síguenos en nuestras Redes Sociales</h2>
            <div class="social-icons">
                <a href="https://twitter.com" class="social-icon twitter" target="_blank"><i class="fab fa-twitter"></i></a>
                <a href="https://instagram.com" class="social-icon instagram" target="_blank"><i class="fab fa-instagram"></i></a>
                <a href="https://facebook.com" class="social-icon facebook" target="_blank"><i class="fab fa-facebook-f"></i></a>
            </div>
        </section>
    </div>

</body>
</html>
