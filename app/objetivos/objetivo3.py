import streamlit as st
import pandas as pd
from utils import query_filtered_data


COLORES_GRUPO = {
    "15-21": "#00ff87", 
    "22-26": "#04f5ff",   
    "27-31": "#ffb1c4", 
    "32-38": "#ff2882",
}


def unir(lista):
    if len(lista) == 1:
        return lista[0]
    return ", ".join(lista[:-1]) + " y " + lista[-1]

def formatear_eur(valor):
    if pd.isna(valor) or valor == 0:
        return "€0"
    if valor >= 1_000_000:
        return f"€{valor / 1_000_000:.2f}M"
    if valor >= 1_000:
        return f"€{valor / 1_000:.0f}k"
    return f"€{valor:,.0f}"

def interpretar_objetivo3(datos):
    temporadas = sorted(datos["TEMPORADA"].unique())
    ultima = datos[datos["TEMPORADA"] == temporadas[-1]]
    

    sal_pos = (
        ultima.groupby("POSICION")
        .apply(lambda g: (g["SALARIO_PROMEDIO"] * g["JUGADORES"]).sum() / g["JUGADORES"].sum())
    )
    sal_grupo = (
        ultima.groupby("GRUPO_ETARIO")
        .apply(lambda g: (g["SALARIO_PROMEDIO"] * g["JUGADORES"]).sum() / g["JUGADORES"].sum())
    )

    mejor_pos = sal_pos.idxmax()
    peor_pos = sal_pos.idxmin()
    pico_grupo = sal_grupo.idxmax()
    menor_grupo = sal_grupo.idxmin()

    texto = ""
    if len(temporadas) > 1:
        texto += f"Temporadas seleccionadas: {unir(temporadas)}. Como referencia se toma la más reciente. "

    if len(sal_pos) == 1:
        texto += (
            f"En {temporadas[-1]}, para la posición {mejor_pos}, el grupo etario con mayor remuneración promedio es "
            f"{pico_grupo} ({formatear_eur(sal_grupo[pico_grupo])}) y el de menor remuneración es {menor_grupo} ({formatear_eur(sal_grupo[menor_grupo])}). "
        )
    else:
        texto += (
            f"En {temporadas[-1]}, la posición con el salario anual promedio más alto es {mejor_pos} "
            f"({formatear_eur(sal_pos[mejor_pos])}) y la de menor remuneración es {peor_pos} ({formatear_eur(sal_pos[peor_pos])}). "
            f"A nivel de grupos etarios, el pico salarial lo alcanza el grupo {pico_grupo} ({formatear_eur(sal_grupo[pico_grupo])}), "
            f"mientras que el grupo {menor_grupo} percibe los salarios base más bajos ({formatear_eur(sal_grupo[menor_grupo])}). "
        )

    if "32-38" in sal_grupo.index and pico_grupo == "32-38":
        texto += (
            "El elevado promedio en el grupo de 32 a 38 años responde al sesgo de supervivencia: "
            "a esa edad solo continúan activos aquellos jugadores de gran jerarquía con contratos de élite. "
        )
    elif "32-38" in sal_grupo.index:
        texto += (
            "A partir de los 32 años, las remuneraciones promedio tienden a decrecer respecto al pico contractual "
            "alcanzado en la madurez deportiva. "
        )

    generadas = [t for t in temporadas if t != "2025/26"]
    if not generadas:
        texto += "Esta temporada corresponde a datos reales."
    else:
        if len(generadas) == 1:
            texto += f"La temporada {generadas[0]} corresponde a datos generados"
        else:
            texto += f"Las temporadas {unir(generadas)} corresponden a datos generados"
        if "2025/26" in temporadas:
            texto += "; solo 2025/26 corresponde a datos reales."
        else:
            texto += ", no reales."
    return texto

def opciones_objetivo3(datos):
    temporadas = sorted(datos["TEMPORADA"].unique())
    ultima_temporada = temporadas[-1]
    df_chart = datos[datos["TEMPORADA"] == ultima_temporada]

    posiciones = sorted(df_chart["POSICION"].unique())


    if len(posiciones) == 1:
        eje_x = temporadas
        nombre_eje = "Temporada"
        df_base = datos
        col_cat = "TEMPORADA"
    else:
        eje_x = posiciones
        nombre_eje = "Posición"
        df_base = df_chart
        col_cat = "POSICION"

    series = []
    for grupo, filas in df_base.groupby("GRUPO_ETARIO"):
        valores = filas.set_index(col_cat).reindex(eje_x)["SALARIO_PROMEDIO"]
        series.append({
            "name": grupo,
            "type": "bar",
            "data": [None if pd.isna(v) else float(v) for v in valores],
            "itemStyle": {"color": COLORES_GRUPO.get(grupo)},
        })

    return {
        "backgroundColor": "transparent",
        "tooltip": {"trigger": "item"},
        "legend": {"top": 0},
        "xAxis": {"type": "category", "data": eje_x, "name": nombre_eje},
        "yAxis": {"type": "value", "name": "Salario promedio"},
        "series": series,
    }

def tarjetas_objetivo3(slot, datos):
    temporadas = sorted(datos["TEMPORADA"].unique())
    ultima = datos[datos["TEMPORADA"] == temporadas[-1]]
    primera = datos[datos["TEMPORADA"] == temporadas[0]]


    fin = (
        ultima.groupby("GRUPO_ETARIO")
        .apply(lambda g: round((g["SALARIO_PROMEDIO"] * g["JUGADORES"]).sum() / g["JUGADORES"].sum()))
    )
    inicio = (
        primera.groupby("GRUPO_ETARIO")
        .apply(lambda g: round((g["SALARIO_PROMEDIO"] * g["JUGADORES"]).sum() / g["JUGADORES"].sum()))
    )

    columnas = slot.columns(len(fin))
    for columna, (grupo, valor) in zip(columnas, fin.items()):
        delta = None
        if len(temporadas) > 1 and grupo in inicio:
            diferencia = valor - inicio[grupo]
            delta = f"{'+' if diferencia >= 0 else ''}{formatear_eur(diferencia)}"
        columna.metric(
            label=f"Grupo {grupo} · {temporadas[-1]}",
            value=formatear_eur(valor),
            delta=delta,
            help=f"Salario anual promedio en {temporadas[-1]} y variación respecto a {temporadas[0]}",
            border=True,
        )

def objetivo3():

    st.subheader("Objetivo 3: Salario anual promedio según grupo etario y posición de juego, periodo 2022-2026")


    chart_slot = st.container()


    st.subheader("Interpretación")
    metricas_slot = st.container()
    texto_slot = st.container()

    st.subheader("Datos utilizados")
    st.markdown(
        "Empleamos el modelo dimensional para esto, se unió la tabla de hechos `FACT_PLAYER_SEASON` con las dimensiones: "
        "`DIM_SEASON`, `DIM_AGE_BRACKET` y `DIM_PLAYER`. Cada fila de la tabla siguiente representa el salario anual promedio "
        "de un grupo etario y posición táctica en una temporada según los filtros globales seleccionados en la barra lateral."
    )
    table_slot = st.container()

    datos = query_filtered_data("""
        SELECT
            SEASON_LABEL AS TEMPORADA,
            CASE PRIMARY_CATEGORY
                WHEN 'ATTACKER' THEN 'Delanteros (ATT)'
                WHEN 'MIDFIELDER' THEN 'Centrocampistas (MID)'
                WHEN 'DEFENDER' THEN 'Defensas (DEF)'
                WHEN 'GOALKEEPER' THEN 'Porteros (GK)'
                ELSE PRIMARY_CATEGORY
            END AS POSICION,
            AGE_GROUP AS GRUPO_ETARIO,
            ROUND(AVG(ANNUAL_WAGE_EUR), 0) AS SALARIO_PROMEDIO,
            COUNT(*) AS JUGADORES
        FROM df_filtrado
        WHERE ANNUAL_WAGE_EUR IS NOT NULL
        GROUP BY SEASON_LABEL, PRIMARY_CATEGORY, AGE_GROUP
        ORDER BY TEMPORADA, POSICION, GRUPO_ETARIO
    """)

    if datos.empty:
        chart_slot.info(
            "No se encontraron registros para la combinación de filtros seleccionada en la barra lateral."
        )
        return

    chart_slot.echarts_chart(opciones_objetivo3(datos))
    table_slot.dataframe(
        datos,
        key="infomd_datos_df",
        hide_index=True,
        column_config={
            "TEMPORADA": st.column_config.TextColumn("Temporada"),
            "POSICION": st.column_config.TextColumn("Posición"),
            "GRUPO_ETARIO": st.column_config.TextColumn("Grupo etario"),
            "SALARIO_PROMEDIO": st.column_config.NumberColumn("Salario promedio", format="€%d"),
            "JUGADORES": st.column_config.NumberColumn("Jugadores", format="%d"),
        },
    )
    tarjetas_objetivo3(metricas_slot, datos)
    texto_slot.markdown(interpretar_objetivo3(datos))