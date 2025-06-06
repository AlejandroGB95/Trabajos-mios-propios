import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

def descargar_boletines(url, output_dir="boletines_melilla"):
    """Descarga los boletines de Melilla desde la URL dada."""

    os.makedirs(output_dir, exist_ok=True)

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 30)

    try:
        # Actualizar el selector XPATH
        download_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@onclick, "window.open(\'/descargar/")]')))

        print(f"Se encontraron {len(download_links)} boletines.")

        for i, link in enumerate(download_links, start=1):
            try:
                onclick_attribute = link.get_attribute("onclick")
                # extraer la url relativa del pdf
                pdf_url_relative = onclick_attribute.split("window.open('")[1].split("');")[0]
                # crear la url completa.
                pdf_url = urljoin(url, pdf_url_relative)

                print(f"URL del PDF {i}: {pdf_url}")

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                response = requests.get(pdf_url, headers=headers)
                response.raise_for_status()

                filename = os.path.join(output_dir, f"boletin_{i:03d}.pdf")
                with open(filename, "wb") as f:
                    f.write(response.content)

                print(f"✅ PDF {i} descargado correctamente: {filename}")

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Error al descargar el PDF {i}: {e}")
            except Exception as e:
                print(f"⚠️ Error con el boletín {i}: {e}")

    except Exception as e:
        print(f"❌ No se encontraron boletines. Error: {e}")

    driver.quit()
    print("Descarga completa.")

url_bomemelilla = "https://bomemelilla.es/bomes/2025"
descargar_boletines(url_bomemelilla)