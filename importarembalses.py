import requests
from bs4 import BeautifulSoup
import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
  host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
  port=4000,
  user="DfWYA9vQa8C3KYP.root",
  password="bITJL8OzxMkIstMi",
  database="CuencasHidrograficas",
  ssl_ca="C:\\Users\\Administrator\\Documents\\REPOS\\Cuencas_Hidrograficas\\isrgrootx1.pem",
  charset='utf8'
)

# Creamos un cursor
cursor = conn.cursor()

# Creamos la tabla 'DATOS' si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS DATOS (
        pantano VARCHAR(255),
        capacidad INT,
        embalsada INT,
        variacion FLOAT,
        porcentaje_agua FLOAT,
        porcentaje_variacion FLOAT,
        cuenca_name VARCHAR(255)
    )
""")

# URL de la página
url = 'https://www.embalses.net/cuencas.php'

# Hacemos la petición a la página
res = requests.get(url)

# Parseamos el contenido de la página
soup = BeautifulSoup(res.text, 'html.parser')

# Buscamos todos los 'tr' con la clase 'ResultadoCampo'
rows = soup.find_all('tr', class_='ResultadoCampo')

# Iteramos sobre cada fila
for row in rows:
    # Buscamos todos los 'td' dentro de la fila
    tds = row.find_all('td')
    
    # Extraemos el enlace de la cuenca y el nombre de la cuenca
    cuenca_name = tds[0].text.strip()

    # Iteramos sobre cada fila de la tabla
    for row_tabla in rows:
        # Buscamos todos los 'td' dentro de la fila
        tds_tabla = row_tabla.find_all('td')
        
        # Check if there are enough 'td' elements
        if len(tds_tabla) >= 4:
            # Extraemos los datos de cada 'td'
            pantano = tds_tabla[0].text.strip().replace('[+]', '')  # Aquí se eliminan los caracteres '[+]'
            capacidad = int(tds_tabla[1].text.strip())
            embalsada = int(tds_tabla[2].text.strip())

            # Extraemos solo el número de la cadena
            variacion_str = tds_tabla[3].text.strip().replace('(', '').replace(')', '').replace('%', '')
            variacion = float(variacion_str)

            # Calculamos el porcentaje de agua que tiene el embalse
            porcentaje_agua = round((embalsada / capacidad) * 100, 2)

            # Calculamos el porcentaje de la variación
            porcentaje_variacion = round((variacion / capacidad) * 100, 2)

            # Insertamos los datos en la tabla DATOS
            query = "INSERT INTO DATOS (cuenca_name, pantano, capacidad, embalsada, variacion, porcentaje_agua, porcentaje_variacion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (cuenca_name, pantano, capacidad, embalsada, variacion, porcentaje_agua, porcentaje_variacion)
            cursor.execute(query, values)

# Hacemos commit de la transacción
conn.commit()

# Cerramos el cursor y la conexión
cursor.close()
conn.close()