import re
import pandas as pd

def cargar_patrones(path):
    return pd.read_csv(path).sort_values("prioridad")


def clasificar_descripcion(desc, patrones):
    if pd.isna(desc):
        return "Otros", "Otros"

    for _, row in patrones.iterrows():
        if re.search(row["patron"], desc, re.IGNORECASE):
            return row["categoria"], row["supercategoria"]

    return "Otros", "Otros"

def aplicar_matching(df, patrones):
    df["categoria"] = "otros"
    df["supercategoria"] = "otros"

    for _, patron in patrones.iterrows():
        mask = df["Descripcion_limpia"].str.contains(
            patron["patron"], case=False, na=False
        )
        df.loc[mask, "categoria"] = patron["categoria"]
        df.loc[mask, "supercategoria"] = patron["supercategoria"]

    return df
