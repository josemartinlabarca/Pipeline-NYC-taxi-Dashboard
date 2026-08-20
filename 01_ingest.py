# 01_ingest.py
import pandas as pd
import requests
import os

# 1. Crear la carpeta 'data' si no existe para evitar errores de ruta
os.makedirs("data", exist_ok=True)

# 2. Definir la URL base oficial de donde la NYC TLC aloja los viajes de Taxis Amarillos (Yellow Taxi) del año 2025
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-"

print("--- INICIANDO PROCESO DE INGESTA DE DATOS ---")

# 3. Iterar para descargar los primeros 2 meses (puedes cambiar el rango si deseas más volumen)
for month in range(1, 3):  # Rango: 1 (Enero) y 2 (Febrero)
    # Formatear el mes a dos dígitos (ej. 1 pasa a "01")
    month_str = f"{month:02d}"
    
    # Construir la URL completa del archivo Parquet mensual
    url = f"{base_url}{month_str}.parquet"
    print(f"Descargando datos del mes {month_str}...")
    print(f"URL: {url}")
    
    # Realizar la solicitud HTTP GET para descargar el archivo
    response = requests.get(url)
    
    # Verificar si la descarga fue exitosa (código HTTP 200)
    if response.status_code == 200:
        file_path = f"data/taxi_data_{month_str}.parquet"
        
        # Guardar el contenido binario descargado en el archivo local dentro de la carpeta 'data/'
        with open(file_path, "wb") as f:
            f.write(response.content)
            
        print(f"-> ¡Éxito! Archivo guardado en: {file_path}\n")
    else:
        print(f"-> Error: No se pudo descargar el mes {month_str}. Código de estado: {response.status_code}\n")

print("--- INGESTA FINALIZADA CORRECTAMENTE ---")
