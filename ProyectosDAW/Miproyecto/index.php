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

// Sentencia SQL 
$insertarDatos = "INSERT INTO formulario (nombre, apellido, email) VALUES ('$nombre', '$apellido', '$email')";

// Ejecución de la consulta
$ejecutarInsertar = mysqli_query($enlaces, $insertarDatos);

}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Pagina Web</title>
    <link rel="stylesheet" type="text/css" href="miestilo1.css"> 
</head>
<body>
    <header>
      
        <nav class="navbar">
            <img src="Imagenes/anime flv.png" alt="Logo">
    
            <!-- Botón Inicio -->
            <button class="menu-btn" onclick="toggleMenu('menuInicio')">Inicio</button>
            <div id="menuInicio" class="menu-dropdown">
                <!-- Opciones de Inicio (vacío para este ejemplo) -->
            </div>
    
            <!-- Botón Menu -->
            <button class="menu-btn" onclick="toggleMenu('menuMenu')">Animes</button>
            <div id="menuMenu" class="menu-dropdown">
                <a href="https://www3.animeflv.net/anime/ore-dake-level-up-na-ken">Solo Leveling</a>
                <a href="https://www3.animeflv.net/anime/one-piece-tv">One Piece</a>
                <a href="https://www3.animeflv.net/browse?q=pokemon">Pokemon</a>
            </div>
            <button class="menu-btn" onclick="toggleMenu('menuAyuda')">Registro</button>
            <div id="menuAyuda" class="menu-dropdown">
                <a href="registro.php">Registrar</a>
            </div>
    
            <!-- Botón Ayuda -->
            <button class="menu-btn" onclick="toggleMenu('menuAyuda')">Ayuda</button>
            <div id="menuAyuda" class="menu-dropdown">
                <a href="#inicio">Error</a>
                <a href="#soporte">Soporte</a>
            </div>
          
            <input name="trabajo" method="post" type="text" id="searchInput" name="busqueda" placeholder="Buscar..." onkeydown="search(event)">
        </nav>
</header>
<section>
    <form action="http://localhost/ProyectosDAW/Miproyecto/Index.php" name="trabajo" method="post">
        <fieldset>
            <legend>Inscribirse en AnimeFLV</legend>
            Nombre:<br>
            <input type="text" name="nombre" placeholder="Alejandro" required>
            <br>
            <br>
            Apellidos:<br>
            <input type="text" name="apellido" placeholder="Garcia" required>
            <br>
            <br>
              <input type="radio" name="gender" value="female">Mujer
            <input type="radio" name="gender" value="male">Hombre
            <input type="radio" name="gender" value="male">Otro
            <br>
            <br>
            Color favorito:
            <input type="color" name="color"><br><br>
           <label for="email">Introduce tu correo:</label>
            <input type="email" id="email" name="email" placeholder="animeid-españa@gmail.com" required>
            <br>
            <br>
            <label for="edad">Ingrese su edad:</label>
          <input type="number" id="edad" name="edad" min="0" max="100" required>
            <br>
            <br>
           <input type="submit" name="trabajo">
           <input type="reset">
          </fieldset>
         </form>
        <article><iframe src="https://www.youtube.com/embed/ZTA77U48F2E?si=LX2bUzqzb05QQWf2" allowfullscreen></iframe></article>
    </section>
<footer>
    <h5>Alejandro Garcia Benitez</h5>
    <p>Siguenos en nuestras Redes</p>
    <div id="sprite" onclick="window.location.href='https://forum.netmarble.com/slv_en/list/38/1';"></div>
     <div id="sprite1" onclick="window.location.href='https://x.com/Sololv_ARISE_GL?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor';"></div>
     <div id="sprite3" onclick="window.location.href='https://www.instagram.com/sololeveling_en/?hl=es';"></div>
    <br>
    <br>
     <p><b>Ningun video se encuentra alojado en nuestra pagina web</b></p>
     <p>
     <a>Terminos y condiones  Politicas y Privacidad Sobre Anime</a>
     </p>
  </footer> 

<script>holamundo()</script>
<script src="practicas.js"></script>
</body>
</html>