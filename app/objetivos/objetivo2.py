import streamlit as st
import pandas as pd

from utils import query_filtered_data

NOMBRES_POSICION = {
    "GOALKEEPER": "Porteros",
    "DEFENDER": "Defensas",
    "MIDFIELDER": "Centrocampistas",
    "ATTACKER": "Delanteros",
}

COLORES_POSICION = {
    "GOALKEEPER": "#ffb1c4",
    "DEFENDER": "#00ff87",
    "MIDFIELDER": "#04f5ff",
    "ATTACKER": "#ff2882",
}

def opciones_veteranos(datos):
    return {
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": [NOMBRES_POSICION.get(p, p) for p in datos["POSICION"]],
        },
        "yAxis": {
            "type": "value",
            "name": "% con 32-38 años",
            "axisLabel": {"formatter": "{value}%"},
        },
        "series": [{
            "type": "bar",
            "data": [
                {"value": float(v), "itemStyle": {"color": COLORES_POSICION.get(p)}}
                for p, v in zip(datos["POSICION"], datos["PCT_VETERANOS"])
            ],
            "label": {"show": True, "position": "top", "formatter": "{c} %"},
        }],
    }

def opciones_cambio(datos):
    grupos = sorted(datos["GRUPO_ETARIO"].unique())
    tipo = "line" if len(grupos) > 1 else "bar"
    
    series = []
    for posicion, filas in datos.groupby("POSICION"):
        valores = filas.set_index("GRUPO_ETARIO").reindex(grupos)["CAMBIO_PROMEDIO"]
        series.append({
            "name": NOMBRES_POSICION.get(posicion, posicion),
            "type": tipo,
            "data": [None if pd.isna(v) else float(v) for v in valores],
            "itemStyle": {"color": COLORES_POSICION.get(posicion)},
        })
    return {
       "tooltip": {"trigger": "axis"},
       "legend": {"top": 0},
       "xAxis": {"type": "category", "data": grupos, "name": "Grupo etario"},
       "yAxis": {"type": "value", "name": "Cambio por temporada"},
       "series": series,
    }

def objetivo2():
    st.subheader("Objetivo 2: Longevidad por posición de juego, periodo 2022-2026")
    st.markdown("**a) Proporción de jugadores veteranos (32-38 años) en cada posición**")
    chart_a = st.container()
    st.markdown("**b) Cambio promedio de habilidad de cada jugador respecto de su temporada anterior, por grupo etario**")
    chart_b = st.container()
    st.subheader("Datos utilizados")
    st.markdown(
        "Se usa el modelo dimensional:`FACT_PLAYER_SEASON` con `DIM_PLAYER` y `DIM_AGE_BRACKET`. "
        "Los conteos son registros jugador-temporada: un jugador que aparece en varias temporadas cuenta una vez por cada una."
    )
    tabla_a = st.container()
    
    datos = query_filtered_data("""
        SELECT
            PRIMARY_CATEGORY AS POSICION,
            COUNT(*) AS REGISTROS,
            SUM(CASE WHEN AGE_GROUP = '32-38' THEN 1 ELSE 0 END) AS VETERANOS,
            ROUND(100.0 * SUM(CASE WHEN AGE_GROUP = '32-38' THEN 1 ELSE 0 END) / COUNT(*), 1) AS PCT_VETERANOS
            FROM df_filtrado
            GROUP BY PRIMARY_CATEGORY
            ORDER BY PCT_VETERANOS DESC                          
    """)
    
    if datos.empty:
        chart_a.info("No se encontraron registros para la comninación de filtros seleccionada.")
    elif datos["VETERANOS"].sum() == 0:
        chart_a.info("Los filtros actuales no incluyen jugadores de 32 a 38 años, así que no se puede calcular esta proporción")
    elif (datos["VETERANOS"] == datos["REGISTROS"]).all():
        chart_a.info("Los filtros solo incluyen jugadores de 32 a 38 años, así que todas las posiciones dan 100%. Incluye otros grupos de edad para poder comparar.")
    else:
        chart_a.echarts_chart(opciones_veteranos(datos))
        tabla_a.dataframe(
            datos.assign(POSICION=datos["POSICION"].map(NOMBRES_POSICION)),
            key="objetivo2_tabla_a",
            hide_index=True,
            column_config={
                "POSICION": st.column_config.TextColumn("Posición"),
                "REGISTROS": st.column_config.NumberColumn("Registros", format="%d"),
                "VETERANOS": st.column_config.NumberColumn("Registros de 32-38 años", format="%d"),
                "PCT_VETERANOS": st.column_config.NumberColumn("% veteranos", format="%.1f%%"),
            },
        )

    cambios = query_filtered_data("""
        SELECT
            PRIMARY_CATEGORY AS POSICION,
            AGE_GROUP AS GRUPO_ETARIO,
            ROUND(AVG(ABILITY_SCORE_DELTA), 1) AS CAMBIO_PROMEDIO,
            COUNT(*) AS REGISTROS
        FROM df_filtrado
        WHERE ABILITY_SCORE_DELTA IS NOT NULL
        GROUP BY PRIMARY_CATEGORY, AGE_GROUP
        ORDER BY POSICION, GRUPO_ETARIO
    """)

    if cambios.empty:
        chart_b.info("No hay cambios que mostrar con estos filtros. La temporada 2022/23 no tiene una temporada anterior con la cual comparar.")
    else:
        chart_b.echarts_chart(opciones_cambio(cambios))