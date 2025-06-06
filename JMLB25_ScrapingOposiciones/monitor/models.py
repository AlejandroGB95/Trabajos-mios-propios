from django.db import models

class UrlMonitor(models.Model):
    url = models.URLField()
    hash = models.CharField(max_length=32, blank=True, null=True)
    has_changed = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    last_checked = models.DateTimeField(blank=True, null=True)
# nuevo codigo Alejandro 28/5/2025 se implementa codigo para el difflib del html   

# Campos para guardar y comparar el contenido HTML de una URL:
# - html_anterior y html_actual almacenan el HTML previo y el más reciente.
# - hash_md5 guarda un hash del contenido actual para detectar cambios rápido.
# - last_checked indica la fecha y hora de la última revisión.
# - is_checked y has_changed indican si se revisó y si hubo cambios.
# - contador_palabras mide cuántas palabras cambiaron entre versiones.

    html_anterior = models.TextField(blank=True, null=True)
    html_actual = models.TextField(blank=True, null=True)
    hash_md5 = models.CharField(max_length=64, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    is_checked = models.BooleanField(default=False)
    has_changed = models.BooleanField(default=False)

    # Nuevo campo para contar las palabras 
    contador_palabras = models.IntegerField(default=0)
# nuevo codigo Alejandro 28/5/2025 se implementa codigo para el difflib del html   

    # NUEVOS CAMPOS para detectar errores
    status_code = models.IntegerField(blank=True, null=True)  
    is_failed = models.BooleanField(default=False)            

    def __str__(self):
        return self.url


class BoletinUrl(models.Model):
    url = models.URLField()
    hash = models.CharField(max_length=32, blank=True, null=True)
    has_changed = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    last_checked = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.url



class Filtro(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    palabras = models.TextField()  # palabras separadas por coma
    archivo = models.FileField(upload_to='filtros/', null=True, blank=True) 
# nuevo codigo Alejandro 21/5/2025 se implementa codigo para filtrado
    

# nuevo codigo Alejandro 21/5/2025 se implementa codigo para filtrado
    def __str__(self):
        return self.nombre
    
# nuevo codigo Alejandro 19/5/2025 se implementa codigo para filtrado
# modificado por Samuel 21/05/2025
class FiltroGenerico(models.Model):
    nombre = models.CharField(max_length=100)
    palabras = models.TextField()  # <-- Este campo debe existir

    def __str__(self):
        return self.nombre
    


