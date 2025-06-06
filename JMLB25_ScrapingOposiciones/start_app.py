# -Fernando
import os
import sys
import threading
import time
import webbrowser
# Importar la función de gestión de comandos de Django y llamar a setup() -Fernando
from django.core.management import execute_from_command_line
import django

# Obtener la ruta absoluta para el ejecutable -Fernando
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # sys._MEIPASS es el directorio temporal donde PyInstaller extrae los archivos -Fernando
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_monitor.settings")

django.setup()

# Funciones para la lógica -Fernando
# Aplicar migraciones -Fernando
def apply_migrations():
    print("Aplicando migraciones de Django...")
    execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
    print("Migraciones aplicadas exitosamente.")

#Iniciar servidor -Fernando
def start_django_server():
    print("Iniciando servidor Django en http://127.0.0.1:8000/ ...")
    execute_from_command_line([sys.argv[0], 'runserver', '--noreload'])

# Esperar para que el servidor arranque y abrir -Fernando
def open_browser_later():
    time.sleep(3)  
    url = "http://127.0.0.1:8000/"
    print(f"Abriendo navegador a {url}")
    webbrowser.open(url)

# Punto de entrada principal -Fernando
if __name__ == '__main__':
    print("Preparando para iniciar la aplicación Django...")
    apply_migrations()
    browser_thread = threading.Thread(target=open_browser_later)
    browser_thread.daemon = True
    browser_thread.start()
    start_django_server()