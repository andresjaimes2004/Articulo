from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import requests
import json
import os
import sys

def get_ruta(ruta_relativa):
    ruta_base = os.path.dirname(__file__)  # Obtiene el directorio actual del archivo
    ruta_completa = os.path.join(ruta_base, ruta_relativa)  # Crea la ruta completa
    return os.path.abspath(ruta_completa)  # Convierte a absoluta

numberDocument = sys.stdin.readline()
extension_path = r"Buster-Captcha-Solver-for-Humans-Chrome-Web-Store.crx"

chrome_options = Options()
# chrome_options.add_extension(extension_path)
chrome_options.add_argument('--remote-allow-origins=*')
service = Service(executable_path=get_ruta('chromedriver.exe'))


driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

def iframe_is_blank(driver):
    try:
        iframe_content = driver.page_source
        if "no admite pÃ¡ginas web que contengan el elemento IFRAME" in iframe_content or iframe_content.strip() == "":
            return True
        return False
    except Exception as e:
        # print(f"Error verificando el iframe: {e}")
        return True

def execute_form_process(driver, doc_text, doc_number, retry_count=2):
    try:
        driver.get("https://www.sisben.gov.co/Paginas/consulta-tu-grupo.html")
        time.sleep(5)
        
        for attempt in range(retry_count):
            iframe = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField"]/section/div/div[1]/div[12]/div/div/iframe'))
            )
            driver.switch_to.frame(iframe)
            
            if iframe_is_blank(driver):
                # print(f"El iframe está vacío o no es compatible. Reintentando {attempt + 1}/{retry_count}")
                driver.switch_to.default_content()
                driver.refresh()
                time.sleep(5)
                continue

            form = wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/form'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", form)

            select_element = wait.until(
                EC.presence_of_element_located((By.ID, 'TipoID'))
            )
            select = Select(select_element)
            select.select_by_visible_text(doc_text)

            input_element = wait.until(
                EC.presence_of_element_located((By.ID, 'documento'))
            )
            input_element.clear()
            time.sleep(2)
            input_element.send_keys(doc_number)
            time.sleep(2)

            inputBtn = wait.until(
                EC.presence_of_element_located((By.ID, 'botonenvio'))
            )
            inputBtn.click()
            time.sleep(4)

            labels = driver.find_elements(By.CSS_SELECTOR, '.etiqueta1.pl-3')
            values = driver.find_elements(By.CSS_SELECTOR, '.campo1.pt-1.pl-2.font-weight-bold')
            if labels == []:
                # print(f"Formulario con {doc_text} no encontró resultados.")
                return None

            nombres = values[0].text.strip()
            apellidos = values[1].text.strip()
            tipoDocumento = values[2].text.strip()
            numeroDoc = values[3].text.strip()
            municipio = values[4].text.strip()
            departamento = values[5].text.strip()

            return {
                'nombres': nombres,
                'apellidos': apellidos,
                'tipoDocumento': tipoDocumento,
                'numeroDoc': numeroDoc,
                'municipio': municipio,
                'departamento': departamento
            }
        
        # print(f"No se pudo procesar el formulario después de {retry_count} intentos con {doc_text}")
        return None

    except Exception as e:
        # print(f'Error al procesar con {doc_text}: {e}')
        return None

try:
    documento = numberDocument
    max_retries = 2

    processed = None
    for retry in range(max_retries):
        # print(f"Intento {retry + 1} con Cédula de Ciudadanía...")
        processed = execute_form_process(driver, "Cédula de Ciudadanía", documento)
        if processed:
            break
        # else:
            # print(f"Fallo el intento {retry + 1} con Cédula de Ciudadanía. Recargando...")

    if not processed:
        # print("Intentando con Tarjeta de Identidad...")
        for retry in range(max_retries):
            # print(f"Intento {retry + 1} con Tarjeta de Identidad...")
            processed = execute_form_process(driver, "Tarjeta de Identidad", documento)
            if processed:
                break
            # else:
                # print(f"Fallo el intento {retry + 1} con Tarjeta de Identidad. Recargando...")
        if not processed:
            print("-----------------")
            print("No se pudieron obtener los datos")
            print("-----------------")
    if processed:
        json_string = json.dumps(processed)
        print("-----------------")
        print(f"Datos: {json_string}")
        print("-----------------")
    #     # nombres = processed['nombres']
    #     # municipio = processed['municipio']
    #     # print(processed)
    #     url = 'http://localhost:4000/usuarios'
    #     response = requests.post(url, json=processed)
    #     if response.status_code == 200:
    #         print("Datos enviados correctamente")
    #     else:
    #         print(f"Error: {response.status_code}")    
    # else:
    #     print("No se pudieron obtener datos")

    time.sleep(5)

except Exception as e:
    # print(f'Error general: {e}')
    print("No se pudieron obtener datos")
finally:
    driver.quit()

