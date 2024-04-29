import mysql.connector
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_embalses_net(url):
    # Realizar la solicitud HTTP
    response = requests.get(url)
    
    # Comprobar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar la tabla de embalses
        table = soup.find('table', {'class': 'Tabla'})
        
        # Extraer los datos de la tabla
        data = []
        rows = table.find_all('tr')
        for row in rows[1:]:  # Saltar la primera fila (encabezados)
            cols = row.find_all('td')
            embalse = cols[0].text.strip()
            capacidad = float(cols[1].text.strip().replace(' Hm3', '').replace(',', '.'))
            almacenamiento = float(cols[2].text.strip().replace(' Hm3', '').replace(',', '.'))
            porcentaje_llenado = (almacenamiento / capacidad) * 100
            data.append({'Embalse': embalse, 'Capacidad': capacidad, 'Almacenamiento': almacenamiento, 'Porcentaje Llenado': porcentaje_llenado})
        
        return data
    else:
        # Si la solicitud no fue exitosa, imprimir el código de estado
        print("Error al realizar la solicitud. Código de estado:", response.status_code)
        return None

def create_table(cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS cuenca_del_tajo (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            fecha DATE,
                            embalse VARCHAR(255),
                            capacidad FLOAT,
                            almacenamiento FLOAT,
                            porcentaje_llenado FLOAT,
                            ultima_actualizacion DATE
                        )''')
        if cursor.rowcount == -1:
            print("Tabla creada correctamente.")
        else:
            print("Tabla actualizada correctamente.")
    except mysql.connector.Error as err:
        print("Error al crear la tabla:", err)

def insert_data(cursor, data):
    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    
    for embalse in data:
        # Verificar si los datos ya existen en la base de datos
        cursor.execute("SELECT COUNT(*) FROM cuenca_del_tajo WHERE embalse = %s", (embalse['Embalse'],))
        count = cursor.fetchone()[0]
        
        if count == 0:
            try:
                cursor.execute('''INSERT INTO cuenca_del_tajo (fecha, embalse, capacidad, almacenamiento, porcentaje_llenado, ultima_actualizacion)
                                  VALUES (%s, %s, %s, %s, %s, %s)''', (fecha_actual, embalse['Embalse'], embalse['Capacidad'], embalse['Almacenamiento'], embalse['Porcentaje Llenado'], fecha_actual))
                print("Datos insertados correctamente.")
            except mysql.connector.Error as err:
                print("Error al insertar datos:", err)
        else:
            try:
                cursor.execute('''UPDATE cuenca_del_tajo SET capacidad = %s, almacenamiento = %s, porcentaje_llenado = %s, ultima_actualizacion = %s
                                  WHERE embalse = %s''', (embalse['Capacidad'], embalse['Almacenamiento'], embalse['Porcentaje Llenado'], fecha_actual, embalse['Embalse']))
                print("Datos actualizados correctamente.")
            except mysql.connector.Error as err:
                print("Error al actualizar datos:", err)

def main():
    url = "https://www.embalses.net/cuenca-3-tajo.html"
    embalses_data = scrape_embalses_net(url)
    
    if embalses_data:
        # Conexión a la base de datos
        try:
            conn = mysql.connector.connect(
                host="127.0.0.2",
                port="3306",
                user="root",
                password="david578",
                database="cuencas_hidrograficas"
            )
            cursor = conn.cursor()
            
            # Crear tabla si no existe
            create_table(cursor)
            
            # Insertar datos
            insert_data(cursor, embalses_data)
            
            # Guardar cambios
            conn.commit()
            
            # Cerrar la conexión
            conn.close()
            print("Proceso completado exitosamente.")
        except mysql.connector.Error as err:
            print("Error de conexión a la base de datos:", err)

if __name__ == "__main__":
    main()
