#----------------------------------------------------------------------------------------------
# enlace para selenium CHROME para la instalacion
# https://googlechromelabs.github.io/chrome-for-testing/#stable
#----------------------------------------------------------------------------------------------
#lista de comandos que se puede usar con chrome drive 
#https://chromium.googlesource.com/chromium/src/+/master/docs/chromedriver_status.md
#-----------------------------------------------------------------------------------------------
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Crear un directorio para almacenar los PDFs descargados
output_dir = "boletines_boe_2025"
os.makedirs(output_dir, exist_ok=True)

# Usar Service en lugar de executable_path
service = Service(ChromeDriverManager().install())  # Esto maneja la instalación automática de ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar sin abrir ventana del navegador (opcional)

# Inicia el WebDriver
driver = webdriver.Chrome(service=service, options=options)

# URL del Boletín Oficial del Estado (BOE)
url = "https://www.boe.es/diario_boe/txt.php?id=BOE-B-2024-25012"
driver.get(url)

# Esperar a que se cargue la página completamente
time.sleep(5)

# Buscar el enlace de descarga del PDF en la página
try:
   # Encontrar y hacer clic en el botón de descarga
    download_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div/div/div/nav/div/div[2]/ul/li/ul/li[1]/a")
    time.sleep(3)
    download_button.click()
    time.sleep(5)

    # Completar la URL si es necesario (agregar el dominio base)
    pdf_url = "https://www.boe.es/diario_boe/txt.php?id=BOE-B-2024-25012" + pdf_url

    print(f"🔗 URL del PDF: {pdf_url}")

    # Descargar el PDF
    response = requests.get(pdf_url)
    if response.status_code == 200:
        # Guardar el PDF en el directorio de salida
        filename = os.path.join(output_dir, "boe_bulletin_2025.pdf")
        with open(filename, "wb") as f:
            f.write(response.content)

        # Verificar que el archivo se ha guardado
        if os.path.exists(filename):
            print(f"✅ PDF descargado correctamente: {filename}")
        else:
            print(f"❌ Error al guardar el PDF")
    else:
        print(f"⚠️ Error al descargar el PDF: {response.status_code}")

except Exception as e:
    print(f"❌ No se encontró el PDF. Error: {e}")

# Cerrar el navegador
driver.quit()

print(f"\n✅ Descarga completa.")



