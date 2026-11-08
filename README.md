# NYC Taxi · Pipeline de datos y dashboard

Pipeline de extremo a extremo con los viajes de taxis amarillos de Nueva York: descarga los datos oficiales de la **NYC Taxi & Limousine Commission (TLC)**, los limpia y transforma a **Apache Parquet**, y los muestra en un dashboard interactivo con **Plotly Dash**.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![Apache Parquet](https://img.shields.io/badge/Apache%20Parquet-50ABF1?logo=apacheparquet&logoColor=white)
![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-3F4F75?logo=plotly&logoColor=white)

## Qué resuelve

Cada mes de la TLC trae millones de viajes con registros imposibles: distancias de cero o de miles de millas, montos negativos y fechas fuera del mes publicado. El pipeline los filtra, deja solo las columnas que se usan y guarda un Parquet compacto que el dashboard carga en segundos.

## Arquitectura

```mermaid
flowchart LR
    A[NYC TLC<br/>Parquet mensual] -->|01_ingest.py| B[data/taxi_data_MM.parquet]
    B -->|02_etl.py<br/>limpieza + variables| C[data/taxi_final_dataset.parquet]
    C -->|app.py| D[Dashboard Dash<br/>localhost:8050]
```

| Etapa | Archivo | Qué hace |
|---|---|---|
| Ingesta | [`01_ingest.py`](01_ingest.py) | Descarga los meses configurados por partes, con timeout y sin dejar archivos a medio bajar. Si un mes ya está descargado, lo omite. |
| ETL | [`02_etl.py`](02_etl.py) | Lee solo las columnas necesarias, descarta viajes fuera del mes, distancias fuera de (0, 100] millas y montos fuera de (0, 1.000] USD. Crea la hora y el día de la semana y guarda el resultado en Parquet. |
| Dashboard | [`app.py`](app.py) | Filtro por día de la semana, KPIs (viajes, tarifa y distancia promedio), demanda por hora e histograma de distancias. |

## Cómo ejecutarlo

Requisitos: Python 3.10 o superior y conexión a internet para la descarga.

```bash
git clone https://github.com/josemartinlabarca/Pipeline-NYC-taxi-Dashboard.git
cd Pipeline-NYC-taxi-Dashboard
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python 01_ingest.py               # descarga enero y febrero de 2025
python 02_etl.py                  # genera data/taxi_final_dataset.parquet
python app.py                     # abre http://127.0.0.1:8050
```

Para descargar otros meses, cambia `YEAR` y `MONTHS` al inicio de `01_ingest.py`. Para activar la recarga automática mientras desarrollas, ejecuta `DASH_DEBUG=1 python app.py`. Úsalo solo en tu máquina, porque la consola de depuración permite ejecutar código.

## Decisiones

- **Parquet en vez de CSV:** formato columnar y comprimido; leer solo 4 columnas es mucho más rápido que cargar el archivo completo.
- **Límites de limpieza explícitos:** los umbrales están como constantes al inicio de `02_etl.py`, para ajustarlos sin tocar la lógica.
- **Fechas fuera del mes:** los archivos de la TLC traen algunos viajes con fechas de otros años; se descartan para que la demanda por hora sea correcta.

## Fuente de datos

[NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). Los archivos descargados quedan en `data/`, que está en `.gitignore`.
