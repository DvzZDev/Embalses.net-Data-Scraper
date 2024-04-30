import mysql.connector

# Crear la conexión a la base de datos
conn = mysql.connector.connect(
  host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
  port=4000,
  user="DfWYA9vQa8C3KYP.root",
  password="bITJL8OzxMkIstMi",
  database="CuencasHidrograficas",
  ssl_ca="C:\\Users\\Administrator\\Documents\\REPOS\\Cuencas_Hidrograficas\\isrgrootx1.pem",
  charset='utf8'  # Asegúrate de que la conexión a la base de datos se hace en UTF-8
)

# Crear un cursor
cursor = conn.cursor()

# Ejecutar una consulta SQL
cursor.execute("SELECT * from `EMBALSE`")

# Obtener los resultados
results = cursor.fetchall()

# Cerrar la conexión
conn.close()