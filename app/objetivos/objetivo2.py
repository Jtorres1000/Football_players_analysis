import streamlit as st

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

def objetivo2():
    st.subheader("Objetivo 2: Longevidad por posición de juego, periodo 2022-2026")
    st.markdown("**a) Proporción de jugadores veteranos (32-38 años) en cada posición**")
    chart_a = st.container()
    st.subheader("Datos utilizados")
    st.markdown(
        "Se usa el modelo dimensional:`FACT_PLAYER_SEASON` con `DIM_PLAYER` y `DIM_AGE_BRACKET`. "
        "Los conteos son registros jugador-temporada: un jugador que aparece en varias temporadas cuenta una ve por cada una."
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
        chart_a.info("Los filtros solo incluyen jugadores de 32 a 38 años, así que todas la posiciones dan 100%. Incluye otros grupos de edad para poder comparar.")
    else:
        chart_a.echarts_chart(opciones_veteranos(datos))
        tabla_a.dataframe(
            datos.assign(POSICION=datos["POSICION"].map(NOMBRES_POSICION)),
            key="objetivo2_tabla_a",
            hide_index=True,
            column_config={
                "POSICION": st.column_config.TextColumn("Posición"),
                "REGISTROS": st.column_config.NumberColumn("Registros", format="%d"),
                "VETERANOS": st.column_config.NumberColumn("% veteranos", format="%.1f%%"), 
            },
        )