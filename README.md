# 🚖 NYC Taxi Data Pipeline & Analytics Dashboard

<p align="center">
  <b>Un proyecto completo de Big Data, ingeniería de datos y visualización interactiva de extremo a extremo utilizando Python, Pandas, Apache Parquet y Plotly Dash.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Engineering-orange?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly%20Dash-Interactive%20UI-green?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Ubuntu-Linux-yellow?style=for-the-badge&logo=ubuntu&logoColor=white" />
</p>

---

## 📌 Sobre el Proyecto
Este repositorio implementa un flujo de trabajo moderno (Pipeline) diseñado para procesar millones de registros de la **NYC Taxi and Limousine Commission (TLC)**. El objetivo es transformar datos masivos y crudos en un panel de control interactivo en tiempo real, optimizando el rendimiento mediante el uso de formatos de almacenamiento analítico avanzados (`.parquet`).

---

## ⚙️ Arquitectura del Pipeline

El flujo de trabajo se divide en 3 etapas principales:

1. **Ingesta automatizada (`01_ingest.py`):** Descarga de manera programática los datasets oficiales mensuales directamente desde los servidores de la NYC TLC en formato binario optimizado.
2. **Transformación ETL (`02_etl.py`):** 
   * Limpieza de datos (filtrado de anomalías, distancias y montos negativos/ceros).
   * Ingeniería de características (*Feature Engineering*: extracción de horas pico, días de la semana).
   * Exportación en formato comprimido **Apache Parquet** para máxima velocidad de lectura.
3. **Visualización Interactiva (`app.py`):** Interfaz web analítica desarrollada con **Plotly Dash**, que incluye tarjetas de resumen dinámicas (KPIs) y gráficos interactivos filtrables por día.

---

## 🛠️ Tecnologías y Librerías Utilizadas
* **Python** (Lenguaje principal)
* **Pandas & NumPy** (Manipulación y análisis de datos)
* **PyArrow** (Gestión de archivos Parquet)
* **Requests** (Automatización de solicitudes HTTP)
* **Plotly & Dash** (Desarrollo del Dashboard web interactivo)

---

## 🚀 Guía de Instalación y Ejecución Local

Sigue estos pasos en tu terminal (compatible con Linux/Ubuntu y WSL):

### 1. Clonar el repositorio
```bash
git clone [https://github.com/josemartinlabarca/Pipeline-NYC-taxi-Dashboard.git](https://github.com/josemartinlabarca/Pipeline-NYC-taxi-Dashboard.git)
cd Pipeline-NYC-taxi-Dashboard
