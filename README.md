# Embalses.net Data Scraper

## Descripción
Este es un script de Node.js que scrapea datos de la página web "https://www.embalses.net/cuencas.php". El script recoge información sobre los embalses y las cuencas en España y guarda los datos en un archivo JSON.

## Requisitos

- Node.js v14 o superior
- npm (Node Package Manager)


## Instalación
#### Para usar este script, primero debes clonar el repositorio desde GitHub. Puedes hacerlo usando el siguiente comando en tu terminal:
```bash
git clone https://github.com/DvzZDev/Embalses.net-Data-Scraper.git
```
## Dependencias

Para ejecutar este script, necesitarás las siguientes dependencias:

- **axios**: Para hacer solicitudes HTTP.
- **cheerio**: Para analizar y seleccionar elementos HTML.
- **fs**: Para escribir los datos en un archivo.
- **progress**: Para visualizar el progreso del scrapeo.

#### Puedes instalar todas estas dependencias con npm usando el siguiente comando:

```sh
npm install axios cheerio fs progress
```

## USO
#### Una vez instaladas las dependencias tendremos que ejecutar el script, tarda entre 4 a 5, ya que tiene que recopilar bastante información.
```bash
node scraper.js
```
#### Cuando termine el script se generará en el proyecto un archivo embalsesData.json que contendrá toda la información.
```json
"Alcantara ": {
    "fecha_modificacion": "2024-05-23 22:36:38",
    "cuenca": "Tajo",
    "agua_embalsada": "3045",
    "agua_embalsada_por": "96.36",
    "variacion_ultima_semana": "-10",
    "variacion_ultima_semana_por": "-0.32",
    "capacidad_total": "3160",
    "misma_semana_ultimo_año": "2.423",
    "misma_semana_ultimo_año_por": "76.68",
    "misma_semana_10años": "2.425",
    "misma_semana_10años_por": "76.77"
  },
  "Alcorlo ": {
    "fecha_modificacion": "2024-05-23 22:36:38",
    "cuenca": "Tajo",
    "agua_embalsada": "138",
    "agua_embalsada_por": "76.67",
    "variacion_ultima_semana": "0",
    "variacion_ultima_semana_por": "0.00",
    "capacidad_total": "180",
    "misma_semana_ultimo_año": "67",
    "misma_semana_ultimo_año_por": "37.22",
    "misma_semana_10años": "99",
    "misma_semana_10años_por": "55.22"
  },

```
#### Podremos convertir este JSON de vuelta a un objeto con JavaScript para su análisis y uso.
```JavaScript
//Importamos FileSystem
const fs = require("fs");

// Lee el archivo JSON
const data = JSON.parse(fs.readFileSync("./embalsesData.json", "utf8"));

// Busca el embalse por su nombre,(Necesitaremos dejar siempre un espacio en blanco al final de la busqueda)
const embalseBuscado = data["San Juan "];

//Imprime el resultado
console.log(embalseBuscado);
```

## Embalses.net
"Los datos obtenidos por el script son recopilados de [embalses.net](https://www.embalses.net/), una fuente confiable de información sobre embalses y reservas de agua. 


## Licencia
Este proyecto es de código abierto, lo que significa que el código fuente está disponible para que cualquiera lo examine, modifique y distribuya según sus necesidades. Si puede serte útil igual que me está siendo a mí adelante!!
