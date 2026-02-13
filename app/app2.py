import streamlit as st
import pandas as pd
import sys
from pathlib import Path

from streamlit.dataframe_util import DataFormat

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.carga import load_excel,load_csv 
from utils.limpieza import (
    procesar_fechas_y_montos,
    limpiar_descripcion,
    obtener_gastos,
    obtener_aportes,
    limpiar_pais
) 
from utils.matching import (
    cargar_patrones,
    clasificar_descripcion,
    aplicar_matching
)
from utils.graficos import (
    grafico_categoria,
    grafico_supercategoria_pie,
    grafico_tiempo,
    grafico_gasto_mensual,
    grafico_categorias_mes
)



st.set_page_config(
    page_title="Análisis de Gastos - BCP",
    layout="wide"
)

st.title("📊 Análisis de gastos personales")
st.caption("Tarjeta de crédito · Datos BCP")


st.sidebar.title("📂 Cargar datos")

uploaded_file = st.sidebar.file_uploader( 
    "Arrastra tu archivo",
    type=["xlsx", "csv"]
)

from utils.carga import load_excel, load_csv

if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = load_excel(uploaded_file)
    else:
        df = load_csv(uploaded_file)
else:
    st.info("👈 Sube un archivo para comenzar")
    st.stop()

df = procesar_fechas_y_montos(
    df,
    fecha_col="Fecha",
    monto_col="Monto",
    desc_col="Descripcion"
)

df = limpiar_descripcion(df, "Descripcion")
df = limpiar_pais(df)

patrones = cargar_patrones("./data/references/catergorias2.csv")
df = aplicar_matching(df, patrones)

df["Mes"] = df["Fecha"].dt.to_period("M").astype(str)

st.sidebar.subheader("🌍 Filtros")

paises = ["Todos"] + sorted(df["Pais"].unique().tolist())
pais = st.sidebar.selectbox("País", paises)

df_base = df if pais == "Todos" else df[df["Pais"] == pais]

st.sidebar.subheader("💰 Tipo de movimiento")

tipo_mov = st.sidebar.radio(
    "Selecciona",
    ["Gastos", "Aportes", "Ambos"]
)

st.dataframe(df_base)

if tipo_mov == "Gastos":
    df_base = df[df["Monto"] < 0].copy()
    monto_col = "monto_abs"   # solo aquí usamos abs

elif tipo_mov == "Aportes":
    df_base = df[df["Monto"] > 0].copy()
    monto_col = "Monto"

else:  # Ambos
    df_base = df.copy()
    monto_col = "Monto"       # 👈 CLAVE


supers = ["Todas"] + sorted(df_base["supercategoria"].unique().tolist())
supercat = st.sidebar.selectbox("Categoria Global", supers)

if supercat != "Todas":
    df_base = df_base[df_base["supercategoria"] == supercat]

fecha_min = df["Fecha"].min()
fecha_max = df["Fecha"].max()

rango = st.sidebar.date_input(
    "Rango de fechas",
    value=(fecha_min, fecha_max)
)

### Main Parte

df_base = df_base[
    (df_base["Fecha"] >= pd.to_datetime(rango[0])) &
    (df_base["Fecha"] <= pd.to_datetime(rango[1]))
]
col1, col2, col3 = st.columns(3)

col1.metric("💸 Total gasto", f"S/ {df[monto_col].sum():,.2f}")
col2.metric("📊 Transacciones", len(df))
col3.metric("📅 Meses", df["Mes"].nunique())



mes = st.selectbox(
    "Mes",
    sorted(df_base["Mes"].unique()),
    index=len(df_base["Mes"].unique()) - 1
)
if tipo_mov == "Gastos" or tipo_mov == "Aportes":
    st.plotly_chart(
        grafico_gasto_mensual(df_base,monto_col),
        use_container_width=True
    )

    st.plotly_chart(
        grafico_categorias_mes(df_base, mes,monto_col),
        use_container_width=True
    )
else:
    st.text("Linea de tiempo por meses")
    df_line = (
    df
    .set_index("Fecha")
    .groupby("tipo_movimiento")["monto_abs"]
    .resample("M")
    .sum()
    .reset_index()
    )
    df_line = df_line.pivot(
    index="Fecha",
    columns="tipo_movimiento",
    values="monto_abs"
    ).reset_index()

    st.line_chart(
    df_line,
    x="Fecha",
    y=df_line.columns[1:],  # todas menos Fecha
    color=["#FF4B4B", "#00C49F"]
    )
    st.dataframe(df_line)
from utils.export import exportar_excel

st.divider()
st.subheader("📥 Exportar reporte")

excel_file = exportar_excel(df_base)

st.download_button(
    label="Descargar reporte en Excel",
    data=excel_file,
    file_name="reporte_financiero.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
