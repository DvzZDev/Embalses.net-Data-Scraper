import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime

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
        pantano VARCHAR(255) UNIQUE,
        capacidad INT,
        embalsada INT,
        variacion INT,
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
    cuenca_link = tds[0].find('a')['href']
    cuenca_name = tds[0].text.strip()

    # Hacemos la petición a la página de la cuenca
    res_cuenca = requests.get(cuenca_link)

    # Parseamos el contenido de la página de la cuenca
    soup_cuenca = BeautifulSoup(res_cuenca.text, 'html.parser')

    # Buscamos la tabla con la clase 'Tabla'
    tabla = soup_cuenca.find('table', class_='Tabla')

    # Buscamos todas las filas dentro de la tabla
    rows_tabla = tabla.find_all('tr', class_='ResultadoCampo')

    # Iteramos sobre cada fila de la tabla
    for row_tabla in rows_tabla:
        # Buscamos todos los 'td' dentro de la fila
        tds_tabla = row_tabla.find_all('td')
        
        # Check if there are enough 'td' elements
        if len(tds_tabla) >= 4:
            # Extraemos los datos de cada 'td'
            a = tds_tabla[0].find('a')
            pantano = a.text.strip().replace('[+]', '')  # Aquí se eliminan los caracteres '[+]'
            pantano = pantano.replace('Ã±', 'ñ')  # Aquí se reemplazan los caracteres 'Ã±' por 'ñ'
            capacidad = int(tds_tabla[1].text.strip())
            embalsada = int(tds_tabla[2].text.strip())
            variacion = int(tds_tabla[3].text.strip())
            FechaActualizacion = datetime.now();
            FechaActualizacion_str = FechaActualizacion.strftime("%Y-%m-%d")
            # Calculamos el porcentaje de agua que tiene el embalse
            porcentaje_agua = round((embalsada / capacidad) * 100, 2)

            # Calculamos el porcentaje de la variación
            porcentaje_variacion = round((variacion / capacidad) * 100, 2)

            # Insertamos los datos en la tabla DATOS
            query = """
                INSERT INTO DATOS (cuenca_name, pantano, capacidad, embalsada, variacion, porcentaje_agua, porcentaje_variacion, FechaActualizacion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    capacidad = VALUES(capacidad),
                    embalsada = VALUES(embalsada),
                    variacion = VALUES(variacion),
                    porcentaje_agua = VALUES(porcentaje_agua),
                    porcentaje_variacion = VALUES(porcentaje_variacion),
                    cuenca_name = VALUES(cuenca_name),
                    FechaActualizacion = VALUES(FechaActualizacion)
            """
            values = (cuenca_name, pantano, capacidad, embalsada, variacion, porcentaje_agua, porcentaje_variacion, FechaActualizacion_str)
            cursor.execute(query, values)

            # Imprimimos en la consola los datos que se acaban de insertar
            print(f"Datos insertados o actualizados: {values}")

# Hacemos commit de la transacción
conn.commit()

# Cerramos el cursor y la conexión
cursor.close()
conn.close()