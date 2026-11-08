# 02_etl.py
# Limpia los viajes descargados, crea variables de tiempo y guarda un Parquet liviano para el dashboard.
import glob
import os
import sys

import pandas as pd

ENTRADA = "data/taxi_data_*.parquet"
SALIDA = "data/taxi_final_dataset.parquet"

# Solo se leen las columnas que se usan: ahorra memoria y tiempo de lectura
COLUMNAS = ["tpep_pickup_datetime", "trip_distance", "total_amount", "passenger_count"]

# Límites de calidad: fuera de estos rangos el registro se considera un error de captura
DISTANCIA_MAX_MILLAS = 100
MONTO_MAX_USD = 1000

ORDEN_DIAS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def periodo_del_archivo(ruta: str, year: int) -> pd.Period:
    """data/taxi_data_01.parquet -> Period('2025-01')"""
    mes = int(os.path.basename(ruta).split("_")[-1].split(".")[0])
    return pd.Period(year=year, month=mes, freq="M")


def main(year: int = 2025) -> int:
    print("--- INICIANDO PROCESO ETL ---")
    archivos = sorted(glob.glob(ENTRADA))
    if not archivos:
        print("No hay archivos en data/. Ejecuta primero: python 01_ingest.py")
        return 1

    partes = []
    for ruta in archivos:
        df_mes = pd.read_parquet(ruta, columns=COLUMNAS)
        df_mes["tpep_pickup_datetime"] = pd.to_datetime(df_mes["tpep_pickup_datetime"])
        # La TLC incluye algunos viajes con fechas fuera del mes publicado: se descartan
        periodo = periodo_del_archivo(ruta, year)
        df_mes = df_mes[df_mes["tpep_pickup_datetime"].dt.to_period("M") == periodo]
        partes.append(df_mes)
        print(f"{ruta}: {len(df_mes):,} viajes del período {periodo}")

    df = pd.concat(partes, ignore_index=True)
    filas_crudas = len(df)
    print(f"Total de filas cargadas: {filas_crudas:,}")

    # Limpieza: distancias y montos imposibles
    df = df[df["trip_distance"].between(0, DISTANCIA_MAX_MILLAS, inclusive="right")]
    df = df[df["total_amount"].between(0, MONTO_MAX_USD, inclusive="right")]
    descartadas = filas_crudas - len(df)
    print(f"Filas descartadas por anomalías: {descartadas:,} ({descartadas / filas_crudas:.1%})")

    # Ingeniería de características
    df["hour"] = df["tpep_pickup_datetime"].dt.hour.astype("int8")
    df["day_of_week"] = pd.Categorical(
        df["tpep_pickup_datetime"].dt.day_name(), categories=ORDEN_DIAS, ordered=True
    )

    df_final = df[["tpep_pickup_datetime", "trip_distance", "total_amount", "hour", "day_of_week", "passenger_count"]]
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    df_final.to_parquet(SALIDA, index=False)

    print(f"Dataset limpio: {len(df_final):,} viajes -> {SALIDA}")
    print("--- FIN DEL PROCESO ETL ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
