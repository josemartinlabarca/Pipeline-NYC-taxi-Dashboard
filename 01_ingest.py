# 01_ingest.py
# Descarga los viajes de taxis amarillos (Yellow Taxi) publicados por la NYC TLC en formato Parquet.
import os
import sys

import requests

# Año y meses a descargar (cambia el rango si quieres más volumen)
YEAR = 2025
MONTHS = range(1, 3)  # 1 (enero) y 2 (febrero)

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
DATA_DIR = "data"


def descargar_mes(year: int, month: int) -> bool:
    """Descarga un mes y lo guarda en data/. Devuelve True si se descargó bien."""
    url = BASE_URL.format(year=year, month=month)
    destino = os.path.join(DATA_DIR, f"taxi_data_{month:02d}.parquet")
    temporal = destino + ".part"

    if os.path.exists(destino):
        print(f"Mes {month:02d}: ya existe {destino}, se omite.")
        return True

    print(f"Mes {month:02d}: descargando {url}")
    try:
        # Descarga por partes para no cargar el archivo completo en memoria
        with requests.get(url, stream=True, timeout=60) as respuesta:
            respuesta.raise_for_status()
            with open(temporal, "wb") as archivo:
                for bloque in respuesta.iter_content(chunk_size=1024 * 1024):
                    archivo.write(bloque)
    except requests.RequestException as error:
        print(f"  -> Error al descargar el mes {month:02d}: {error}")
        if os.path.exists(temporal):
            os.remove(temporal)
        return False

    # Se renombra al final para no dejar archivos a medio descargar con el nombre definitivo
    os.replace(temporal, destino)
    print(f"  -> Guardado en {destino}")
    return True


def main() -> int:
    os.makedirs(DATA_DIR, exist_ok=True)
    print("--- INICIANDO INGESTA DE DATOS ---")
    resultados = [descargar_mes(YEAR, m) for m in MONTHS]
    if not all(resultados):
        print("--- INGESTA TERMINADA CON ERRORES ---")
        return 1
    print("--- INGESTA FINALIZADA CORRECTAMENTE ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
