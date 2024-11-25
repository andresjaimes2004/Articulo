from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from PIL import Image
import requests
import time
import cv2
import numpy as np
import os
import sys
# import pytesseract

def get_ruta(ruta_relativa):
    ruta_base = os.path.dirname(__file__)  # Obtiene el directorio actual del archivo
    ruta_completa = os.path.join(ruta_base, ruta_relativa)  # Crea la ruta completa
    return os.path.abspath(ruta_completa)  # Convierte a absoluta

extension_path = get_ruta('./Buster-Captcha-Solver-for-Humans-Chrome-Web-Store.crx')
numberDocument = sys.stdin.readline()

# Configura ChromeOptions
chrome_options = Options()
chrome_options.add_extension(extension_path)
chrome_options.add_argument('--remote-allow-origins=*')
service = Service(executable_path=get_ruta('./chromedriver.exe'))

# Crea una instancia de ChromeDriver con la extensión
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)
wait2 = WebDriverWait(driver, 15)
action = ActionChains(driver)

def execute_form_process(driver, doc_text, doc_number, retry_count=2):
    try:
        # Abre el navegador con la extensión cargada
        for attempt in range(retry_count):
            input = wait.until(
                EC.presence_of_element_located((By.ID, 'cedulaInput'))
            )
            input.clear()
            time.sleep(2)
            input.send_keys(doc_number)

            iframe = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="captchaAntecedentes"]/div/div/iframe'))
            )
            driver.switch_to.frame(iframe)
            time.sleep(2)
        
            captcha = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'recaptcha-checkbox-border'))
            )
            time.sleep(2)
            captcha.click()
            time.sleep(2)
            driver.switch_to.default_content()
            try:
                # Verificar si el iframe sigue existiendo después del clic
                iframe2 = wait2.until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div[4]/iframe'))
                )
                
                # Si el iframe se encuentra y es válido, procedemos
                if iframe2 and iframe2.tag_name == 'iframe':
                    driver.switch_to.frame(iframe2)
                    time.sleep(2)

                    # Asegurarse de que el general_div tenga contenido
                    general_div = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'rc-buttons'))
                    )
        
                    shadowHost = general_div.find_element(By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[5]')
                    shadowHost.click()
                    time.sleep(2)
                    driver.switch_to.default_content()
                    
                # else:
                #     print(f'No se encontró el iframe o no es un iframe válido')

            except Exception as e:
                # Si el iframe no es necesario, simplemente ignoramos la interacción
                print("El iframe no es necesario, CAPTCHA validado con éxito")

            consult = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="j_idt17"]'))
            )
            consult.click()
            time.sleep(5)

            span = wait.until(
                EC.presence_of_element_located((By.ID,'form:mensajeCiudadano'))
            )
            if span:
                time.sleep(2)
                # Obtener los div hijos
                child_b = span.find_elements(By.TAG_NAME, 'b')
                # time.sleep(2)
                nombre = child_b[2]
                situacion = child_b[3]
                return True
            else:
                return False
        return None
    except Exception as e:
        return None

try:
    
    documento = numberDocument
    max_retries = 2

    processed = None
    driver.get("https://antecedentes.policia.gov.co:7005/WebJudicial/antecedentes.xhtml")
    time.sleep(5)

    terminos = wait.until(
        EC.presence_of_element_located((By.ID, 'aceptaOption:0'))
    )
    terminos.click()
    time.sleep(2)
    buttonTerminos = wait.until(
        EC.presence_of_element_located((By.ID, 'continuarBtn'))
    )
    buttonTerminos.click()
    time.sleep(5)
    
    for retry in range(max_retries):
        processed = execute_form_process(driver, "Cédula de Ciudadanía", documento)
        if processed:
            break
    if not processed:
        for retry in range(max_retries):
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
        processed = not processed
        print("-----------------")
        print(f"Situacion: {processed}")
        print("-----------------")

    time.sleep(5)

except Exception as e:
    print("-----------------")
    print("No se pudieron obtener los datos")
    print("-----------------")
finally:
    driver.quit()

