# 02_etl.py
import pandas as pd
import glob
import os

print("--- INICIANDO PROCESO ETL ---")

# 1. Buscar todos los archivos parquet descargados en la carpeta data/
files = glob.glob("data/taxi_data_*.parquet")

if not files:
    print("¡Error! No se encontraron archivos parquet en la carpeta data/. Ejecuta primero el script de ingesta.")
    exit()

print(f"Archivos encontrados para procesar: {files}")

# 2. Cargar y concatenar todos los archivos en un solo DataFrame de Pandas
df_list = [pd.read_parquet(f) for f in files]
df = pd.concat(df_list, ignore_index=True)
print(f"Total de filas crudas cargadas: {len(df):,}")

# 3. Limpieza de datos (Filtros de calidad)
# Eliminamos viajes con distancias en cero/negativas o tarifas totales menores o iguales a cero
df = df[(df['trip_distance'] > 0) & (df['total_amount'] > 0)]
print(f"Filas después de limpiar anomalías: {len(df):,}")

# 4. Ingeniería de características (Feature Engineering)
# Convertir la fecha de inicio del viaje a tipo datetime de Pandas
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])

# Extraer la hora del día (0 a 23) y el nombre del día de la semana (Monday, Tuesday, etc.)
df['hour'] = df['tpep_pickup_datetime'].dt.hour
df['day_of_week'] = df['tpep_pickup_datetime'].dt.day_name()

# 5. Seleccionar únicamente las columnas clave para optimizar rendimiento y memoria
cols_to_keep = ['tpep_pickup_datetime', 'trip_distance', 'total_amount', 'hour', 'day_of_week', 'passenger_count']
df_final = df[cols_to_keep]

# 6. Guardar el dataset limpio y optimizado en formato Parquet
os.makedirs("data", exist_ok=True)
output_file = "data/taxi_final_dataset.parquet"
df_final.to_parquet(output_file, index=False)

print(f"¡ETL completado con éxito!")
print(f"Dataset optimizado guardado en: {output_file}")
print("--- FIN DEL PROCESO ETL ---")
