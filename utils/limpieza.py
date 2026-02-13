import pandas as pd

def procesar_fechas_y_montos(df, fecha_col, monto_col, desc_col):
    df[fecha_col] = pd.to_datetime(df[fecha_col])
    df[desc_col] = (
        df[desc_col]
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )
    df["tipo_movimiento"] = df[monto_col].apply(
        lambda x: "GASTO" if x < 0 else "PAGO"
    )
    df["monto_abs"] = df[monto_col].abs()
    return df


def limpiar_descripcion(df, desc_col):
    df["Descripcion_base"] = (
        df[desc_col]
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df["Pais"] = df["Descripcion_base"].str.extract(r"\b([A-Z]{2})$")

    df["Descripcion_sin_geo"] = (
        df["Descripcion_base"]
        .str.replace(r"\bLIMA\b", "", regex=True)
        .str.replace(r"\bORLANDO\b", "", regex=True)
        .str.replace(r"\bPE\b|\bFL\b", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df["Descripcion_limpia"] = (
        df["Descripcion_sin_geo"]
        .str.replace(r"^(VM\*|IZI\*)", "", regex=True)
        .str.replace(r"(TELE|CLAR)\d+", r"\1", regex=True)
        .str.replace(r"\d+", "", regex=True)
        .str.strip()
    )

    return df

def obtener_gastos(df):
    gasto = df[df["tipo_movimiento"] == "GASTO"]
    return gasto

def obtener_aportes(df):
    pago = df[df["tipo_movimiento"] == "PAGO"]
    return pago

def limpiar_pais(df):
    df["Pais"] = df["Pais"].fillna("PE")
    return df
