import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar el directorio de descarga
download_directory = "C:\\Users\\Administrator\\Documents\\Datos Cuencas Hidrograficas"

# Crear el directorio si no existe
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Configurar el webdriver de Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Para ejecución en background
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(options=chrome_options)

# URL de la página
url = "https://www.saihguadiana.com/E/DATOS"

# Acceder a la página
driver.get(url)

try:
    # Esperar hasta que el botón de descarga esté disponible
    xls_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Exportar Excel']"))
    )
    
    # Hacer clic en el botón de descarga
    xls_button.click()

    # Esperar un momento para que se complete la descarga
    time.sleep(10)  # Esperar 10 segundos para asegurarse de que la descarga se complete

    # Obtener la fecha y hora actual en formato legible
    current_datetime = datetime.now().strftime("%Y-%m-%d")

    # Renombrar el archivo xls descargado
    downloaded_file = os.path.join(download_directory, 'RESUMEN DATOS EN TIEMPO REAL.xlsx')
    renamed_file = os.path.join(download_directory, f'Datos_Cuenca_Guadiana_{current_datetime}.xlsx')
    os.rename(downloaded_file, renamed_file)
    print("Archivo xls descargado exitosamente en:", renamed_file)
    
finally:
    # Cerrar el navegador
    driver.quit()
