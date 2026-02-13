Las categorías se asignan antes de la BD

Los pagos se guardan, pero se excluyen del análisis

No hay hora → análisis diario/mensual

Las reglas están versionadas en CSV

Esto se escribe en el README.

 Paso 1: Obtener el estado de cuenta

Objetivo:
Tener los movimientos bancarios en un formato trabajable (Excel / CSV).

Qué hiciste:

Descargaste el estado de cuenta del BCP Perú desde la web.

Lo llevaste a un archivo que luego se puede leer con Python (pandas).

 Sin este paso, no hay datos que analizar.

Paso 2: Cargar y revisar la estructura de los datos

Objetivo:
Confirmar que el archivo se leyó bien y entender qué columnas tenemos.

Qué validaste:

Columnas:
- Fecha
- Descripcion
- Moneda
- Monto


Y los tipos:

Fecha → object

Descripcion → object

Moneda → object

Monto → float64

 Aquí verificamos que:

El Monto es numérico (clave para cálculos).

No hay columnas raras o mal leídas.

 Paso 3: Verificar calidad de datos (datos faltantes)

Objetivo:
Asegurarnos de que no haya valores nulos que rompan análisis o gráficos.

Resultado:

Fecha          0
Descripcion    0
Moneda         0
Monto          0


 Conclusión:

 No hay datos faltantes

El dataset está limpio para análisis básico

 Paso 4: Exploración inicial de los datos

Objetivo:
Entender cómo se mueve tu dinero a nivel general.

Lo que revisaste:

Ejemplos de descripciones (comercios, transferencias, etc.)

Estadísticas del monto:

count: 53 movimientos
mean:  -29.68
min:  -1299.00
max:   3918.18


 Interpretación clave:

La mayoría son egresos (valores negativos).

Hay ingresos puntuales grandes.

Ya podemos detectar:

gastos frecuentes

gastos fuertes

ingresos

En resumen, hasta ahora:

Ya tienes:
 Datos reales del banco
 Dataset limpio
 Columnas claras
 Primer entendimiento de gastos e ingresos

ef load_data_excel(data):
    data = pd.read_excel(data)
    return data
def load_data_csv(data):
    data = pd.read_csv(data)
    return data

def fechaymontoabs(df,fecha_column_name,monto_column_name,descripcion_column_name)  :
    df[fecha_column_name] = pd.to_datetime(df[fecha_column_name])
    df[descripcion_column_name] = (
        df[descripcion_column_name]
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )
    df["tipo_movimiento"] = df[monto_column_name].apply(lambda x: "GASTO" if x < 0 else "PAGO")
    df["monto_abs"] = df[monto_column_name].abs()
    return df

def gastos(df):
    gasto = df[df["tipo_movimiento"] == "GASTO"]
    return gasto

def aportes(df):
    pago = df[df["tipo_movimiento"] == "PAGO"]
    return pago

def limpieza(df,descripcion_column_name):
    df["Descripcion_base"] = (
        df[descripcion_column_name]
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
def clasificar_descripcion(desc,patrones):
    if pd.isna(desc):
        return "Otros", "Otros"
    
    desc = desc.upper()
    
    for _, row in patrones.iterrows():
        patron = row["patron"]
        
        if re.search(patron, desc, re.IGNORECASE):
            return row["categoria"], row["supercategoria"]
    
    return "Otros", "Otros"
categorias = load_data_csv("../data/references/catergorias2.csv").sort_values("prioridad")
df = load_data_excel("../data/raw/VisaOroBCPQore.xlsx")
df = fechaymontoabs(df,"Fecha","Monto","Descripcion")
gasto = gastos(df)
aportes = aportes(df)
gasto = limpieza(gasto,"Descripcion")
aportes = limpieza(aportes,"Descripcion")
st.dataframe(gasto)
st.dataframe(aportes)



gasto[["Categoria", "Supercategoria"]] = gasto["Descripcion_limpia"] \
    .apply(lambda x: pd.Series(clasificar_descripcion(x,categorias)))
st.subheader("Gastos por categoría")

gasto = (
    gasto
    .groupby("Categoria", as_index=False)["monto_abs"]
    .sum()
    .sort_values("monto_abs", ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(gasto["Categoria"], gasto["monto_abs"])
ax.set_ylabel("Monto gastado")
ax.set_xlabel("Categoría")
ax.set_title("Distribución de gastos por categoría")
plt.xticks(rotation=45, ha="right")

st.pyplot(fig)
