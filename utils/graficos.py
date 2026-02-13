import plotly.express as px

def grafico_categoria(df,monto):
    resumen = df.groupby("categoria")[monto].sum().reset_index()
    return px.bar(
        resumen,
        x="categoria",
        y=monto, 
        title="Gastos por categoría"
    )


def grafico_supercategoria_pie(df, monto):
    resumen = df.groupby("supercategoria")[monto].sum().reset_index()
    return px.pie(
        resumen,
        names="supercategoria",
        values=monto,
        title="Distribución por supercategoría"
    )


def grafico_tiempo(df, freq="M", monto = "monto_abs"):
    resumen = (
        df
        .set_index("Fecha")
        .resample(freq)[monto]
        .sum()
        .reset_index()
    )

    return px.line(
        resumen,
        x="Fecha",
        y=monto,
        title="Evolución de gastos en el tiempo"
    )

import plotly.express as px

def grafico_gasto_mensual(df,monto):
    mensual = (
        df.groupby("Mes", as_index=False)[monto]
        .sum()
        .sort_values("Mes")
    )

    fig = px.bar(
        mensual,
        x="Mes",
        y=monto,
        title="Gasto total por mes",
        labels={
            "Mes": "Mes",
            "monto_abs": "Monto gastado"
        }
    )

    return fig
def grafico_categorias_mes(df, mes,monto):
    df_mes = df[df["Mes"] == mes]

    categorias = (
        df_mes.groupby("categoria", as_index=False)[monto]
        .sum()
        .sort_values(monto, ascending=False)
    )

    fig = px.pie(
        categorias,
        names="categoria",
        values=monto,
        title=f"Distribución por categoría · {mes}"
    )

    return fig
def grafico_gasto_mensual(df,monto):
    df_m = (
        df.groupby("Mes", as_index=False)[monto]
        .sum()
        .sort_values("Mes")
    )

    fig = px.bar(
        df_m,
        x="Mes",
        y=monto,
        title="Gasto mensual",
        labels={
            "Mes": "Mes",
            "monto_abs": "Monto gastado"
        }
    )

    return fig