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
      print(f"Embalse: {embalse} | Cuenca: {cuenca}")

      # Insertar los datos en la tabla EMBALSES o actualizarlos si ya existen
      query = """
      INSERT INTO EMBALSES (embalse, cuenca) VALUES (%s, %s)
      ON DUPLICATE KEY UPDATE embalse = VALUES(embalse), cuenca = VALUES(cuenca)
      """
      cursor.execute(query, (embalse, cuenca))
      print(f"Datos insertados o actualizados para el embalse {embalse} en la cuenca {cuenca}")

print("Haciendo commit de la transacción...")
conn.commit()

print("Cerrando el cursor y la conexión...")
cursor.close()
conn.close()

print("¡Hecho!")