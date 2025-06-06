
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from monitor.models import Filtro
import csv
from .models import Filtro
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.http import JsonResponse
import hashlib
import requests
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import UrlMonitor, BoletinUrl
import urllib3
from django.core.paginator import Paginator # 🟣 ​Para poder implementar paginación
from .models import UrlMonitor, BoletinUrl
# Deshabilitar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def index(request):
    active_tab = request.GET.get('tab', 'todos')  # Por defecto, "todos"
    page_number = request.GET.get('page') # 🟣​ Página en la que se está
    busqueda = request.GET.get('busqueda', '').strip().lower()  # Captura el filtro de búsqueda
    # Base queryset
    base_urls = UrlMonitor.objects.filter(is_failed=False).order_by('-has_changed', 'last_checked')

    # Diccionario para mapear pestañas a filtros
    tab_filters = {
        'boe': BoletinUrl.objects.all().order_by('has_changed', 'last_checked'),
        'pendientes': UrlMonitor.objects.filter(has_changed=True, is_checked=False).order_by('last_checked'),
        'vistos': UrlMonitor.objects.filter(is_checked=True).order_by('last_checked'),
        'todos': base_urls,
    }

    # Obtener URLs según pestaña
    urls = tab_filters.get(active_tab, base_urls)

    # Procesar pestaña "fallidas" de forma dinámica
    if active_tab == 'fallidas':
        urls = UrlMonitor.objects.filter(is_failed=True).order_by('last_checked')

    #🟣​ Paginación para optimizar la página web. 25 enlaces por página
    paginator = Paginator(urls, 25)
    page_obj = paginator.get_page(page_number)

    total_counts = {
        'todos': UrlMonitor.objects.all().count(),
        'boe': BoletinUrl.objects.all().count(),
        'pendientes': UrlMonitor.objects.filter(has_changed=True, is_checked=False).count(),
        'vistos': UrlMonitor.objects.filter(is_checked=True).count(),
        'fallidas': UrlMonitor.objects.filter(is_failed=True).count(),
    }

    return render(request, 'monitor/index.html', {
        'urls': urls,
        'active_tab': active_tab,
        'page_obj': page_obj, #🟣 ​número de páginas
        'total_counts': total_counts,
        'busqueda': busqueda, #para enviar búsqueda al html
    })


def reset_status(request):
    if request.method == 'POST':
        active_tab = request.POST.get('tab', 'web')

        if active_tab == 'boe':
            urls = BoletinUrl.objects.all()
            for url in urls:
                url.has_changed = False
                url.is_checked = False
                url.last_checked = None
                url.save()
        else:
            urls = UrlMonitor.objects.all()
            for url in urls:
                url.has_changed = False
                url.is_checked = False
                url.status_code = None
                url.is_failed = False
                url.contador_palabras = 0  # 🟡 Aquí lo pones
                # No borres html_anterior, html_actual ni hash_md5
                url.save()

    return redirect('/')




# nuevo codigo Alejandro 28/5/2025 se implementa codigo aqui se explica que se hace punto por punto.

"""
check_changes verifica cambios en URLs según la pestaña activa, comparando hashes MD5 del contenido web.  
Actualiza estados, HTML previo y actual, y cuenta diferencias de palabras si detecta cambios.  
Maneja errores, guarda resultados y redirige mostrando la pestaña actualizada.
"""

def check_changes(request):
    active_tab = request.POST.get('tab', 'todos')

    if active_tab == 'boe':
        urls = BoletinUrl.objects.all()
    else:
        urls = UrlMonitor.objects.all()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36',
    }

    for url_entry in urls:
        try:
            response = requests.get(url_entry.url, headers=headers, timeout=30, verify=False)
            new_html = response.text
            new_hash = hashlib.md5(new_html.encode('utf-8')).hexdigest()

            if url_entry.hash != new_hash:
                url_entry.has_changed = True
                url_entry.is_checked = False
                url_entry.hash = new_hash

                # Guardar HTML anterior y actual
                anterior_html = url_entry.html_actual or ""
                url_entry.html_anterior = anterior_html
                url_entry.html_actual = new_html

                if anterior_html:
                    anterior_palabras = set(anterior_html.split())
                    actual_palabras = set(new_html.split())
                    diferencias = actual_palabras.symmetric_difference(anterior_palabras)
                    url_entry.contador_palabras = len(diferencias)
                else:
                    url_entry.contador_palabras = 0

            else:
                url_entry.has_changed = False
                url_entry.contador_palabras = 0

            url_entry.status_code = response.status_code

            if response.status_code >= 500 or response.status_code == 404:
                url_entry.is_failed = True
            else:
                url_entry.is_failed = False

      
        except Exception as e:
            print(f"Error inesperado en {url_entry.url}: {e}")
            url_entry.status_code = None
            url_entry.is_failed = True
            url_entry.has_changed = False
            url_entry.contador_palabras = 0

        url_entry.last_checked = timezone.now()
        url_entry.save()

    return redirect(f'/?tab={active_tab}')

# nuevo codigo Alejandro 28/5/2025 se implementa codigo nuevo

def mark_all_checked(request):
    active_tab = request.POST.get('tab', 'todos')
    if active_tab == 'boe':
        BoletinUrl.objects.filter(has_changed=True, is_checked=False).update(is_checked=True)
    else:
        UrlMonitor.objects.filter(has_changed=True, is_checked=False).update(is_checked=True)
    return redirect(f'/?tab={active_tab}')



# nuevo codigo Alejandro 14/5/2025 se implementa codigo para guardar el check y que se quede guardado

def marcar_checkbox_ajax(request):
    if request.method == 'POST':
        url_id = request.POST.get('id')
        estado = request.POST.get('estado') == 'true'
        UrlMonitor.objects.filter(id=url_id).update(is_checked=estado)
        return JsonResponse({'success': True})
  
# nuevo codigo Alejandro 14/5/2025 se implementa codigo para guardar el check y que se quede guardado

# nuevo codigo Alejandro 19/5/2025 se implementa codigo para importar archivo


def importar_archivo(request):
    try:
        if request.method == 'POST':
            archivo = request.FILES.get('archivo')
            if not archivo:
                return render(request, 'monitor/importar.html', {'error': 'Archivo no enviado'})

            nombre = archivo.name.split('.')[0]
            contenido = archivo.read().decode('utf-8')

            print("Archivo recibido:", archivo.name)
            print("Contenido archivo:", contenido)

            # Crea o actualiza el Filtro
            filtro, creado = Filtro.objects.update_or_create(
                nombre=nombre,
                defaults={'palabras': contenido}
            )

            # Guarda el archivo en el campo FileField correctamente
            filtro.archivo.save(archivo.name, archivo)
            filtro.save()

            # Guarda el archivo asociado (opcional si tu modelo lo tiene)
            if hasattr(filtro, 'archivo'):
                filtro.archivo.save(archivo.name, ContentFile(contenido.encode('utf-8')))
                filtro.save()

            return redirect('filtros_genericos')

        return render(request, 'monitor/importar.html')

    except Exception as e:
        print(">>> ERROR EN VISTA importar_archivo:", str(e))
        return render(request, 'monitor/importar.html', {
            'error': f'Ocurrió un error inesperado: {str(e)}'
        })

# nuevo codigo Alejandro 19/5/2025 se implementa codigo para exportar archivo


def exportar_archivo(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtros.txt"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Palabras'])  # Cabecera

    for filtro in Filtro.objects.all():
        writer.writerow([filtro.id, filtro.nombre, filtro.palabras])

    return response


# nuevo codigo Alejandro 19/5/2025 se implementa codigo para renderizar archivo
def filtros_genericos(request):
    filtros = Filtro.objects.all()
    filtro_aplicado_id = request.GET.get('filtro_aplicado')

    urls = UrlMonitor.objects.all().order_by('-last_checked') # ajusta a tu modelo de URL

    if filtro_aplicado_id:
        filtro = Filtro.objects.get(id=filtro_aplicado_id)
        palabras = [p.strip() for p in filtro.palabras.split(',')]
        urls = urls.filter(url__icontains=palabras[0])  # ejemplo: aplicar el primer filtro

    paginator = Paginator(urls, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'monitor/filtros_genericos.html', {
        'filtros': filtros,
        'filtro_aplicado_id': int(filtro_aplicado_id) if filtro_aplicado_id else None,
        'page_obj': page_obj,
    })

# nuevo codigo Alejandro 19/5/2025 se implementa codigo para borrar importación 


@require_POST
def reset_importacion(request):
    Filtro.objects.all().delete()  # borra todos los filtros importados
    return redirect('filtros_genericos')  # redirige a la vista de filtros
# nuevo codigo Alejandro 19/5/2025 se implementa codigo para borrar importación 

# nuevo codigo Alejandro 21/5/2025 se implementa codigo para crear filtro 


def crear_filtro(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        palabras = request.POST.get('palabras') 

        filtro = Filtro(nombre=nombre, palabras=palabras)
        filtro.save()
        return redirect('filtros_genericos')  

# nuevo codigo Alejandro 21/5/2025 se implementa codigo para crear filtro

# nuevo codigo Alejandro 21/5/2025 se implementa codigo para ver el filtro activo


def vista_index(request):
    filtro_aplicado_id = request.GET.get('filtro_aplicado')
    filtro_aplicado = None
    if filtro_aplicado_id:
        try:
            filtro_aplicado = Filtro.objects.get(id=filtro_aplicado_id)
        except Filtro.DoesNotExist:
            pass
    
    context = {
        'filtro_aplicado': filtro_aplicado,
    }
    return render(request, 'monitor/index.html', context)
# nuevo codigo Alejandro 21/5/2025 se implementa codigo para ver el filtro activo

# nuevo código Doramas 30/5/2025 para editar el contenido y nombre de los filtros
def editar_filtro(request):
    filtro_id = request.POST.get("id")
    filtro = get_object_or_404(Filtro, id=filtro_id)
    filtro.nombre = request.POST.get("nombre")
    filtro.palabras = request.POST.get("palabras")
    filtro.save()
    return redirect('filtros_genericos')
# nuevo código Doramas 30/5/2025 para editar el contenido y nombre de los filtros

# nuevo código Raúl 22/5/2025 para el buscador de la página de inicio
def buscar_urls(request):
    busqueda = request.GET.get('busqueda', '').strip().lower()
    
    # Filtrar URLs que contengan la palabra buscada
    urls = UrlMonitor.objects.all()
    if busqueda:
        urls = urls.filter(url__icontains=busqueda)

    paginator = Paginator(urls, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    total_counts = {
        'todos': UrlMonitor.objects.all().count(),
        'boe': BoletinUrl.objects.all().count(),
        'pendientes': UrlMonitor.objects.filter(has_changed=True, is_checked=False).count(),
        'vistos': UrlMonitor.objects.filter(is_checked=True).count(),
        'fallidas': UrlMonitor.objects.filter(is_failed=True).count(),
    }

    return render(request, 'monitor/index.html', {
        'urls': urls,
        'busqueda': busqueda,
        'page_obj': page_obj,
        'total_counts': total_counts,
        'active_tab': 'todos',
    })
# nuevo codigo Alejandro 28/5/2025 se implementa codigo para ver el difflib y comparar el html

"""
La función check_urls revisa cada URL en la base de datos para detectar cambios comparando hashes MD5.
Si hay cambios, actualiza el contenido, cuenta las diferencias en palabras y marca la URL como modificada.
Finalmente, guarda los resultados y redirige a la página principal.
"""



def check_urls(request):
    urls = UrlMonitor.objects.all()

    for url in urls:
        try:
     
            response = requests.get(url.url, timeout=10)
            new_html = response.text

            # MD5 actual
            new_hash = hashlib.md5(new_html.encode('utf-8')).hexdigest()

            # Comparar con hash anterior
            if new_hash != url.hash_md5:
                url.has_changed = True

                # Comparar palabras si hay HTML anterior
                if url.html_anterior:
                    anterior_palabras = set(url.html_anterior.split())
                    actual_palabras = set(new_html.split())
                    diferencias = actual_palabras.symmetric_difference(anterior_palabras)
                    url.contador_palabras = len(diferencias)
                else:
                    url.contador_palabras = 0

                url.html_anterior = url.html_actual or ""
                url.html_actual = new_html
                url.hash_md5 = new_hash
                url.last_checked = timezone.now()

            else:
                url.has_changed = False
                url.contador_palabras = 0

            url.save()

        except Exception as e:
            print(f"Error al comprobar {url.url}: {e}")

    return redirect('index')  
# nuevo codigo Alejandro 28/5/2025 se implementa codigo para ver el difflib y comparar el html
