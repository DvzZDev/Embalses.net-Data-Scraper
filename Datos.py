import requests
from bs4 import BeautifulSoup
import mysql.connector
import datetime
fecha_modificacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
conn = mysql.connector.connect(
    host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
    port=4000,
    user="DfWYA9vQa8C3KYP.root",
    password="bITJL8OzxMkIstMi",
    database="CuencasHidrograficas",
    ssl_ca="C:\\Users\\Administrator\\Documents\\REPOS\\Cuencas_Hidrograficas\\isrgrootx1.pem",
)
cursor = conn.cursor()

# URL de la página web que queremos scrappear
url = "https://www.embalses.net/cuencas.php"

# Realizamos la petición a la web
response = requests.get(url)

# Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
soup = BeautifulSoup(response.text, 'html.parser')

# Obtenemos la tabla donde están los datos
table = soup.find('table', {'class': 'Tabla'})

# Recorremos todas las filas de la tabla para extraer los datos
rows = table.find_all('tr', {'class': 'ResultadoCampo'})

for row in rows:
  columns = row.find_all('td')
  cuenca = columns[0].text.strip()
  cuenca_link = columns[0].find('a')['href']  # Obtenemos el enlace de la cuenca

  # Hacemos una nueva petición a la URL de la cuenca
  cuenca_response = requests.get(f"https://www.embalses.net/{cuenca_link}")
  cuenca_soup = BeautifulSoup(cuenca_response.text, 'html.parser')

  # Aquí puedes recorrer la tabla asociada a la cuenca
  cuenca_table = cuenca_soup.find('table', {'class': 'Tabla'})
  cuenca_rows = cuenca_table.find_all('tr', {'class': 'ResultadoCampo'})

  for cuenca_row in cuenca_rows:
    cuenca_columns = cuenca_row.find_all('td')
    if len(cuenca_columns) >= 3:
      embalse = cuenca_columns[0].text.strip()
      embalse = embalse.replace('Ã±', 'ñ').replace('[+]', '')
      embalse_link = cuenca_columns[0].find('a')['href']  # Obtenemos el enlace del embalse

      print(f"Embalse: {embalse} | Cuenca: {cuenca}")

      # Hacemos una nueva petición a la URL del embalse
      embalse_response = requests.get(f"https://www.embalses.net/{embalse_link}")
      embalse_soup = BeautifulSoup(embalse_response.text, 'html.parser')

      # Buscamos todos los divs con la clase "SeccionCentral_Caja"
      divs = embalse_soup.find_all('div', {'class': 'SeccionCentral_Caja'})

      # Comprobamos que hay al menos dos divs
      if len(divs) < 2:
        print(f"No se encontraron al menos dos divs con la clase 'SeccionCentral_Caja' en el embalse {embalse}")
      else:
        # Obtenemos el segundo div
        second_div = divs[1]

        # Extraemos los datos de cada elemento "div" con clase "FilaSeccion" en el segundo div
        import re

        # Crear un diccionario para almacenar los datos de cada FilaSeccion
        datos = {}

        # Aquí estaba el error. Deberías buscar los divs "FilaSeccion" en el segundo div
        fila_seccion_divs = second_div.find_all('div', {'class': 'FilaSeccion'})

        import logging

        # Configurar el logging
        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        for i, fila_seccion_div in enumerate(fila_seccion_divs):
          fecha_modificacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          campo_div = fila_seccion_div.find('div', {'class': 'Campo'})
          resultado_divs = fila_seccion_div.find_all('div', {'class': 'Resultado'})
          unidad_divs = fila_seccion_div.find_all('div', {'class': ['Unidad', 'Unidad2']})

          if campo_div and resultado_divs and unidad_divs:
            fila_datos = []
            for resultado_div, unidad_div in zip(resultado_divs, unidad_divs):
              resultado = resultado_div.text.strip()
              fila_datos.append(resultado)

            if i == 0:
              agua_embalsada = fila_datos[0]
              agua_embalsada_por = fila_datos[1] if len(fila_datos) > 1 else None
              logging.info(f"Iteración {i}: agua_embalsada = {agua_embalsada}, agua_embalsada_por = {agua_embalsada_por}")
            elif i == 1:
              variacion_ultima_semana = fila_datos[0]
              variacion_ultima_semana_por = fila_datos[1] if len(fila_datos) > 1 else None
              logging.info(f"Iteración {i}: variacion_ultima_semana = {variacion_ultima_semana}, variacion_ultima_semana_por = {variacion_ultima_semana_por}")
            elif i == 2:
              capacidad_total = fila_datos[0]
              logging.info(f"Iteración {i}: capacidad_total = {capacidad_total}")
            elif i == 3:
              misma_semana_ultimo_año = fila_datos[0]
              misma_semana_ultimo_año_por = fila_datos[1] if len(fila_datos) > 1 else None
              logging.info(f"Iteración {i}: misma_semana_ultimo_año = {misma_semana_ultimo_año}, misma_semana_ultimo_año_por = {misma_semana_ultimo_año_por}")
            elif i == 4:
              misma_semana_10años = fila_datos[0]
              misma_semana_10años_por = fila_datos[1] if len(fila_datos) > 1 else None
              logging.info(f"Iteración {i}: misma_semana_10años = {misma_semana_10años}, misma_semana_10años_por = {misma_semana_10años_por}")

        # Insertar los datos en la tabla EMBALSES o actualizarlos si ya existen
        # Extraer las filas de la tabla
        filas = table.find_all('tr')

    
        # Preparar la sentencia SQL INSERT
        # Preparar la sentencia SQL INSERT ... ON DUPLICATE KEY UPDATE
        sql = """
        INSERT INTO datos_embalses(
          fecha_modificacion,
          nombre_embalse,
          nombre_cuenca,
          agua_embalsada,
          agua_embalsadapor,
          variacion_ultima_semana,
          variacion_ultima_semanapor,
          capacidad_total,
          misma_semana_ultimo_año,
          misma_semana_ultimo_añopor,
          misma_semana_10años,
          misma_semana_10añospor
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
          fecha_modificacion = VALUES(fecha_modificacion),
          agua_embalsada = VALUES(agua_embalsada),
          agua_embalsadapor = VALUES(agua_embalsadapor),
          variacion_ultima_semana = VALUES(variacion_ultima_semana),
          variacion_ultima_semanapor = VALUES(variacion_ultima_semanapor),
          capacidad_total = VALUES(capacidad_total),
          misma_semana_ultimo_año = VALUES(misma_semana_ultimo_año),
          misma_semana_ultimo_añopor = VALUES(misma_semana_ultimo_añopor),
          misma_semana_10años = VALUES(misma_semana_10años),
          misma_semana_10añospor = VALUES(misma_semana_10añospor)
        """

        # Ejecutar la sentencia SQL con los datos
        cursor.execute(sql, (
          fecha_modificacion,
          embalse,
          cuenca,
          agua_embalsada,
          agua_embalsada_por,
          variacion_ultima_semana,
          variacion_ultima_semana_por,
          capacidad_total,
          misma_semana_ultimo_año,
          misma_semana_ultimo_año_por,
          misma_semana_10años,
          misma_semana_10años_por
        ))

        # Confirmar los cambios
        conn.commit()