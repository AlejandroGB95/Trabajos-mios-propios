import requests
import re
import os
from pypdf import PdfReader
import pandas as pd
from datetime import datetime

def descargar_pdf(url, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error al descargar el PDF desde {url}: {e}")
        return False

def extraer_texto_pdf(filename):
    try:
        with open(filename, 'rb') as archivo:
            lector_pdf = PdfReader(archivo)
            texto = ""
            for pagina in lector_pdf.pages:
                texto += pagina.extract_text()
        return texto
    except Exception as e:
        print(f"Error al leer el PDF {filename}: {e}")
        return ""

def extraer_datos(texto, url):
    datos = []
    #Expresiones regulares----------------------------------------------------

    # Buscar posibles bloques que contengan todo junto
    bloques = re.findall(r"(Ayuntamiento.*?convoca.*?plazas.*?\.)", texto, re.IGNORECASE | re.DOTALL)

    for bloque in bloques:
        # Ayuntamiento
        ayto_match = re.search(r"(Ayuntamiento de [A-ZÁÉÍÓÚÑa-zñ\s]+)", bloque)
        ayuntamiento = ayto_match.group(1).strip() if ayto_match else "No encontrado"

        # Nombre de la oposición
        oposicion_match = re.search(r"(convoca .*?plazas de [A-ZÁÉÍÓÚÑa-zñ\s]+)", bloque)
        oposicion = oposicion_match.group(1).strip().capitalize() if oposicion_match else "No encontrado"

        # Lugar
        lugar_match = re.search(r"en ([A-ZÁÉÍÓÚÑa-zñ\s]+),?\s+a (?:través|cargo|favor|instancias)", bloque)
        lugar = lugar_match.group(1).strip() if lugar_match else ayuntamiento

        # Fecha
        fecha_match = re.search(r"(\d{1,2} de [a-zA-Z]+ de \d{4})", bloque)
        fecha = fecha_match.group(1).strip() if fecha_match else "No encontrada"
        #Expresiones regulares-----------------------------------------------------------------
        datos.append({
            'Ayuntamiento': ayuntamiento,
            'Oposición': oposicion,
            'Lugar': lugar,
            'Fecha': fecha,
            'Fuente (URL)': url
        })

    return datos

def procesar_urls(urls):
    resultados = []

    for url in urls:
        print(f"Procesando: {url}")
        nombre_pdf = 'temporal.pdf'

        if not descargar_pdf(url, nombre_pdf):
            continue

        texto = extraer_texto_pdf(nombre_pdf)
        datos = extraer_datos(texto, url)
        resultados.extend(datos)

        os.remove(nombre_pdf)

    return resultados

def guardar_en_excel(datos):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_excel = f"oposiciones_extraidas_{timestamp}.xlsx"

    df = pd.DataFrame(datos)
    df.to_excel(archivo_excel, index=False)

    print(f"\n✅ Resultados guardados en '{archivo_excel}'")

# ------------------
# USO DEL SCRIPT
# ------------------

urls = [
    'https://www.boe.es/boe/dias/2025/03/28/pdfs/BOE-S-2025-75.pdf',
    'https://www.boe.es/boe/dias/2025/04/11/pdfs/BOE-S-2025-88.pdf'
]

datos = procesar_urls(urls)
guardar_en_excel(datos)
