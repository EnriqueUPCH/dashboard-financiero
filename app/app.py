import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from utils.carga import load_excel
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
    grafico_tiempo
)



st.set_page_config(
    page_title="Análisis de Gastos - BCP",
    layout="wide"
)

st.title("📊 Análisis de gastos personales")
st.caption("Tarjeta de crédito · Datos BCP")


df = load_excel("./data/raw/VisaOroBCPQore.xlsx")

df = procesar_fechas_y_montos(
    df,
    fecha_col="Fecha",
    monto_col="Monto",
    desc_col="Descripcion"
)

df_gastos = obtener_gastos(df)
df_aportes = obtener_aportes(df)
df_gastos = limpiar_descripcion(df_gastos, "Descripcion")
df_aportes = limpiar_descripcion(df_aportes, "Descripcion")
df_gastos = limpiar_pais(df_gastos)
df_aportes = limpiar_pais(df_aportes)

patrones = cargar_patrones("./data/references/catergorias2.csv")

df_gastos[["Categoria", "Supercategoria"]] = (
    df_gastos["Descripcion_limpia"]
    .apply(lambda x: pd.Series(clasificar_descripcion(x, patrones)))
)

st.dataframe(df_gastos)
st.dataframe(df_aportes)
df = limpiar_descripcion(df, "Descripcion")
df = aplicar_matching(df, patrones)
df = limpiar_pais(df)


df_gastos = aplicar_matching(df_gastos, patrones)
st.plotly_chart(grafico_categoria(df_gastos,"monto_abs"))
st.plotly_chart(grafico_supercategoria_pie(df_gastos,"monto_abs"))
st.plotly_chart(grafico_tiempo(df_gastos, freq="M", monto="monto_abs"))

df_gastos["Mes"] = df_gastos["Fecha"].dt.to_period("M").astype(str)

from utils.graficos import (
    grafico_gasto_mensual,
    grafico_categorias_mes
)

st.subheader("📅 Análisis mensual")
st.plotly_chart(grafico_gasto_mensual(df_gastos), use_container_width=True)
meses = sorted(df_gastos["Mes"].unique())
mes_seleccionado = st.selectbox(
    "Selecciona un mes",
    meses,
    index=len(meses) - 1
)
st.plotly_chart(
    grafico_categorias_mes(df_gastos, mes_seleccionado),
    use_container_width=True
)
