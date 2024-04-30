import mysql.connector
import requests
from bs4 import BeautifulSoup

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

    # Verifica si la fila existe
    cursor.execute("SELECT * FROM CUENCA WHERE cuenca = %s", (cuenca,))
    row = cursor.fetchone()

    if row is None:
        # Si la fila no existe, inserta una nueva
        cursor.execute(
            "INSERT INTO CUENCA (cuenca, capacidad, embalsada, porcentaje_embalsada, variacion, porcentaje_variacion) VALUES (%s, %s, %s, %s, %s, %s)",
            (cuenca, capacidad, embalsada, porcentaje_embalsada, variacion, porcentaje_variacion),
        )
        print(f"Datos insertados para la cuenca {cuenca}")
    else:
        # Si la fila existe, actualízala
        cursor.execute(
            "UPDATE CUENCA SET capacidad = %s, embalsada = %s, porcentaje_embalsada = %s, variacion = %s, porcentaje_variacion = %s WHERE cuenca = %s",
            (capacidad, embalsada, porcentaje_embalsada, variacion, porcentaje_variacion, cuenca),
        )
        print(f"Datos actualizados para la cuenca {cuenca}")

        

# Hacemos commit de la transacción
conn.commit()

