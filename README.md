# SCRAPER EMBALSES.NET

## Descripción
Tenemos un script de Node.js que scrapea datos de la página web "https://www.embalses.net.es". El script recoge información sobre los embalses y las cuencas en España y guarda los datos en un archivo JSON para su posterior uso.

## Dependencias
Para ejecutar este script, necesitarás las siguientes dependencias:
- `axios`: Para hacer solicitudes HTTP.
- `cheerio`: Para analizar y seleccionar elementos HTML.
- `fs`: Para escribir los datos en un archivo.
- `progress`: Para visualizar el progreso del raspado.

Puedes instalar todas estas dependencias con npm usando el siguiente comando:
```bash
npm install axios cheerio fs progress
```
## Instalación
Para usar este script, primero debes clonar el repositorio desde GitHub. Puedes hacerlo usando el siguiente comando en tu terminal:
```bash
git clone https://github.com/DvzZDev/Embalses.net-Data-Scraper.git
```

## Uso
Una vez tengamos clonado el repositorio solo queda ejecutarlo para poder generar el archivo JSON, el script tarda unos 4-5 minutos en finalizar, ya que tiene que procesar bastante información.
```bash
node scraper.js
```
Este JSON lo podríamos transformar, de vuelta en un objeto en JS para poder usarlo de la forma que queramos.
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
## JSON
Cuando el script termine se generara un JSON en la misma carpeta del proyecto. Solo tendremos que abrirlo y tendremos todos los datos hidrograficos sobre los embalses de españa. 
```JSON
"Alcantara ": {
    "fecha_modificacion": "2024-05-23 23:02:38",
    "cuenca": "Tajo",
    "agua_embalsada": "3045",
    "agua_embalsada_por": "96.36",
    "variacion_ultima_semana": "-10",
    "variacion_ultima_semana_por": "-0.32",
    "capacidad_total": "3160",
    "misma_semana_ultimo_year": "2.423",
    "misma_semana_ultimo_year_por": "76.68",
    "misma_semana_10years": "2.425",
    "misma_semana_10years_por": "76.77"
  },
  "Alcorlo ": {
    "fecha_modificacion": "2024-05-23 23:02:38",
    "cuenca": "Tajo",
    "agua_embalsada": "138",
    "agua_embalsada_por": "76.67",
    "variacion_ultima_semana": "0",
    "variacion_ultima_semana_por": "0.00",
    "capacidad_total": "180",
    "misma_semana_ultimo_year": "67",
    "misma_semana_ultimo_year_por": "37.22",
    "misma_semana_10years": "99",
    "misma_semana_10years_por": "55.22"
  },
  "Almoguera ": {
    "fecha_modificacion": "2024-05-23 23:02:38",
    "cuenca": "Tajo",
    "agua_embalsada": "6",
    "agua_embalsada_por": "85.71",
    "variacion_ultima_semana": "0",
    "variacion_ultima_semana_por": "0.00",
    "capacidad_total": "7",
    "misma_semana_ultimo_year": "6",
    "misma_semana_ultimo_year_por": "85.71",
    "misma_semana_10years": "5",
    "misma_semana_10years_por": "84.29"
  }, 
```
