# 📊 Dashboard Financiero Personal

Aplicación interactiva desarrollada con **Streamlit** para el análisis de gastos y aportes personales a partir de archivos Excel o CSV.

---

## 🌐 Demo en vivo

[👉 LINK_DEMO](https://financialappdashboard.streamlit.app/)

---

## 🎯 Problema que resuelve

Muchos usuarios descargan sus movimientos bancarios en Excel pero no cuentan con una herramienta visual para:

- Analizar su flujo de caja
- Identificar categorías dominantes
- Evaluar su balance mensual
- Generar reportes ejecutivos

Este proyecto transforma datos crudos en un dashboard financiero interactivo.

---

## 🚀 Funcionalidades

### 📂 Carga de datos
- Drag & Drop de archivos Excel o CSV
- Procesamiento automático de fechas y montos

### 🎛 Filtros dinámicos
- Tipo de movimiento (Gastos / Aportes / Ambos)
- Filtro por mes
- Filtro por categoría

### 📊 Visualizaciones interactivas
- Movimiento mensual
- Evolución temporal
- Comparativo Gastos vs Aportes
- Distribución por categoría
- Distribución por supercategoría

### 📥 Exportación profesional
- 📊 Excel multi-hoja:
  - Datos filtrados
  - Resumen mensual
  - Resumen por categoría
  - Balance por tipo
- 📄 PDF ejecutivo:
  - KPIs principales
  - Resumen por categoría

---

## 🛠 Tecnologías utilizadas

- Python 3.10+
- Streamlit
- Pandas
- Plotly
- XlsxWriter
- ReportLab

---

## 🧠 Arquitectura del proyecto
dashboard-financiero/
│
├── app/
│ └── app2.py # Aplicación principal
│
├── utils/
│ ├── carga.py # Carga de archivos
│ ├── limpieza.py # Procesamiento de datos
│ ├── matching.py # Clasificación por patrones
│ ├── graficos.py # Visualizaciones
│ ├── export.py # Exportación Excel
│ └── export_pdf.py # Generación de PDF
│
├── assets/ # Capturas del dashboard
├── requirements.txt
└── README.md


---

## 📸 Capturas

```markdown
![Dashboard](assets/dashboard.png)


