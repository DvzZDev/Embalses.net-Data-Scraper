import mysql.connector
import requests
from bs4 import BeautifulSoup
import datetime;

# Conexión a la base de datos
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
    capacidad = columns[1].text.strip()
    embalsada = columns[2].text.strip()
    porcentaje_embalsada = float(columns[3].text.strip().replace('(', '').replace(')', '').replace('%', ''))
    variacion = columns[4].text.strip()
    porcentaje_variacion = float(columns[5].text.strip().replace('(', '').replace(')', '').replace('%', ''))
    fecha_modificacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Verifica si la fila existe
    try:
        cursor.execute(
            """
            INSERT INTO CUENCA (fecha_modificacion, cuenca, capacidad, embalsada, porcentaje_embalsada, variacion, porcentaje_variacion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            fecha_modificacion = VALUES(fecha_modificacion),
            capacidad = VALUES(capacidad),
            embalsada = VALUES(embalsada),
            porcentaje_embalsada = VALUES(porcentaje_embalsada),
            variacion = VALUES(variacion),
            porcentaje_variacion = VALUES(porcentaje_variacion)
            """,
            (fecha_modificacion, cuenca, capacidad, embalsada, porcentaje_embalsada, variacion, porcentaje_variacion),
        )
        cursor.fetchall()  # Consume todos los resultados
        print(f"Datos insertados o actualizados para la cuenca {cuenca}")
    except Exception as e:
        print(f"Error executing SQL query: {e}")
# Hacemos commit de la transacción
conn.commit()

