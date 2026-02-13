import pandas as pd
from io import BytesIO


def exportar_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        # -----------------------
        # Datos originales
        # -----------------------
        df.to_excel(writer, sheet_name="Datos", index=False)

        # -----------------------
        #  Resumen mensual
        # -----------------------
        resumen_mensual = (
            df.groupby("Mes", as_index=False)["Monto"]
            .sum()
            .sort_values("Mes")
        )

        resumen_mensual.to_excel(writer, sheet_name="Resumen_Mensual", index=False)

        # -----------------------
        #Resumen categoría
        # -----------------------
        resumen_categoria = (
            df.groupby("categoria", as_index=False)["Monto"]
            .sum()
            .sort_values("Monto", ascending=False)
        )

        resumen_categoria.to_excel(writer, sheet_name="Resumen_Categoria", index=False)

        # ----------------------
        #  Balance por tipo
        # -----------------------
        if "tipo_movimiento" in df.columns:

            balance = (
                df.groupby("tipo_movimiento", as_index=False)["Monto"]
                .sum()
            )

            balance.to_excel(writer, sheet_name="Balance", index=False)

    output.seek(0)
    return output
