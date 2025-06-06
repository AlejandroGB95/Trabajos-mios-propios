# 🗂️ Scraping Oposiciones

### ❓ ¿Qué estamos haciendo?

Este proyecto busca hacer el trabajo de un equipo más rápido y sencillo, automatizando la comprobación diaria de más de 500 enlaces relacionados con convocatorias de oposiciones.

### ❓ ¿Cómo visualizar el proyecto?

1. Descarga o clona este repositorio.
2. Asegúrate de tener Python instalado y con la versión 3.13.3.
3. Abre el proyecto en Visual Studio Code (o tu editor favorito).
4. Instala las dependencias escribiendo en la terminal:

   ```bash
   pip install -r requirements.txt

5. Abre la terminal y ejecuta el siguiente comando:

   ```bash
   python manage.py runserver
   
  En sistemas Linux o Mac, puede que sea necesario cambiar `python` por `python3`.

6. En consola aparecerá una IP local con la que podrás acceder a la web y ver lo que tenemos hecho.

### ❓ ¿Cómo crear un nuevo ejecutable para cualquier versión con pyinstaller?

Abrir terminal y ejecutar:

pyinstaller --onefile `
--add-data "manage.py;." `
--add-data "url_monitor;url_monitor" `
--add-data "monitor;monitor" `
--add-data "monitor;templates" `
--add-data "monitor;static" `
--add-data "db.sqlite3;." `
--add-data "generar_preload.py;." `
--add-data "Lista _urls_de_boletines.xlsx;." `
--add-data "ServiciosSgtoConv2025.xlsx;." `
start_app.py

Este ejecutable servira para cualquier entorno, incluso sin python.