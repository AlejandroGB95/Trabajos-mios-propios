#-Fernando
import os
import sys
from django.core.management import execute_from_command_line

#Establecer la variable del entono para los setting del proyecto-Fernando
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "url_monitor.settings")
    # Ejecuta el comando de Django con los argumentos pasados.
    execute_from_command_line(sys.argv)