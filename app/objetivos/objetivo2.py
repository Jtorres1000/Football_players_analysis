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

#funcion auxiliar

def nombre(posicion):
    return NOMBRES_POSICION.get(posicion, posicion).lower()[0:-1]

#funcion auxiliar

def datos_a_validos(datos):
    return (
        not datos.empty
        and datos["VETERANOS"].sum() > 0
        and not (datos["VETERANOS"] == datos["REGISTROS"]).all()
    )

def opciones_veteranos(datos):
    return {
        "tooltip": {"trigger": "item"},
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

def interpretar_objetivo2(datos, cambios):
    texto = ""
    pos_a = None
    pos_b = None
    
    if datos_a_validos(datos):
        mayor = datos.loc[datos["PCT_VETERANOS"].idxmax()]
        if len(datos) == 1:
            texto += (
                f"En la posición de {nombre(mayor['POSICION'])}, el {mayor['PCT_VETERANOS']}% "
                f"de los registros corresponde a jugadores de 32 a 38 años."
            )
        else:
            pos_a = mayor["POSICION"]
            texto += (
                f"La posición con mayor proporción de jugadores de 32 a 38 años es la de "
                f"{nombre(pos_a)} con ({mayor['PCT_VETERANOS']}%). "
            )

    veteranos = cambios[cambios["GRUPO_ETARIO"] == "32-38"]
    if not veteranos.empty:
        mejor = veteranos.loc[veteranos["CAMBIO_PROMEDIO"].idxmax()]
        if len(veteranos) == 1:
            texto += (
                f"Entre los 32 y 38 años, los {nombre(mejor['POSICION'])}s cambian en promedio "
                f"{mejor['CAMBIO_PROMEDIO']} puntos de habilidad por temporada. "
            )
        else:
            pos_b = mejor["POSICION"]
            peor = veteranos.loc[veteranos["CAMBIO_PROMEDIO"].idxmin()]
            diferencia = round(mejor["CAMBIO_PROMEDIO"] - peor["CAMBIO_PROMEDIO"], 1)
            texto += (
                f"Entre los 32 y 38 años, la posición que mejor conserva su habilidad es la de "
                f"{nombre(pos_b)} que cambia ({mejor['CAMBIO_PROMEDIO']}) puntos por temporada y la que más pierde puntos es la de "
                f"{nombre(peor['POSICION'])} con ({peor['CAMBIO_PROMEDIO']}) puntos; la diferencia entre ambas es de {diferencia} puntos. "
            )
            if diferencia < 5:
                texto += "Es una diferencia pequeña: la pérdida de habilidad con la edad es parecida en todas las posiciones. "
                
    if pos_a and pos_b:
        if pos_a == pos_b:
            texto += f"La posición de {nombre(pos_a)} resulta ser la más longeva según ambos criterios."
        else:
            texto += (
                f"Los dos criterios no coinciden: los {nombre(pos_a)}s son los que más tiempo permanecen activos "
                f"y los {nombre(pos_b)}s los que mejor conservan su habilidad."
            )
    if datos_a_validos(datos):
        texto += (
            "La proporción de veteranos varía mucho entre temporadas, porque las temporadas generadas entre "
            "2022/23 a 2024/25, tienen muchos menos jugadores de 32 a 38 años que la temporada real 2025/26."
        )
    if not texto:
        texto = "Con los filtros actuales no hay datos suficientes para interpretar la longevidad."
    return texto

def tarjetas_objetivo2(slot, datos, cambios):
    tarjetas = []
    if datos_a_validos(datos):
        mayor = datos.loc[datos["PCT_VETERANOS"].idxmax()]
        tarjetas.append(("Mayor proporción de veteranos", mayor["POSICION"], f"{mayor['PCT_VETERANOS']}% con 32-38 años"))
    veteranos = cambios[cambios["GRUPO_ETARIO"] == "32-38"]
    if not veteranos.empty:
        mejor = veteranos.loc[veteranos["CAMBIO_PROMEDIO"].idxmax()]
        tarjetas.append(("Menor pérdida de habilidad a los 32-38", mejor["POSICION"], f"{mejor['CAMBIO_PROMEDIO']} por temporada"))

    if not tarjetas:
        return
    columnas = slot.columns(len(tarjetas))
    for columna, (titulo, posicion, detalle) in zip(columnas, tarjetas):
        columna.metric(
            label=titulo,
            value=NOMBRES_POSICION.get(posicion, posicion),
            delta=detalle,
            delta_color="off",
            delta_arrow="off",
            border=True,
        )

def objetivo2():
    st.subheader("Objetivo 2: Longevidad por posición de juego, periodo 2022-2026")
    st.markdown("**a) Proporción de jugadores veteranos (32-38 años) en cada posición**")
    chart_a = st.container()
    st.markdown("**b) Cambio promedio de habilidad de cada jugador respecto de su temporada anterior, por grupo etario**")
    chart_b = st.container()
    st.subheader("Interpretación")
    tarjetas_slot = st.container()
    texto_slot = st.container()
    st.subheader("Datos utilizados")

    st.markdown("**Parte a**: Se usa el modelo dimensional:`FACT_PLAYER_SEASON` con `DIM_PLAYER` y `DIM_AGE_BRACKET`. Los conteos son registros jugador-temporada: un jugador que aparece en varias temporadas cuenta una vez por cada una")
    tabla_a = st.container()
    st.markdown(
        "**Parte b**: se usa `ABILITY_SCORE_DELTA`, la diferencia entre la habilidad de cada jugador "
        "y la suya en la temporada anterior. La primera temporada de cada jugador no tiene con qué compararse y se excluye."
    )
    tabla_b = st.container()
    
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
        chart_a.info("No se encontraron registros para la combinación de filtros seleccionada.")
        tabla_a.info("No se encontraron registros para la combinación de filtros seleccionada.")
    elif datos["VETERANOS"].sum() == 0:
        chart_a.info("Los filtros actuales no incluyen jugadores de 32 a 38 años, así que no se puede calcular esta proporción")
        tabla_a.info("Los filtros actuales no incluyen jugadores de 32 a 38 años, así que no se puede calcular esta proporción")
    elif (datos["VETERANOS"] == datos["REGISTROS"]).all():
        chart_a.info("Los filtros solo incluyen jugadores de 32 a 38 años, así que todas las posiciones dan 100%. Incluye otros grupos de edad para poder comparar.")
        tabla_a.info("Los filtros solo incluyen jugadores de 32 a 38 años, así que todas las posiciones dan 100%. Incluye otros grupos de edad para poder comparar.")
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
        chart_b.info("No se encontraron registros para la combinación de filtros seleccionada.")
        tabla_b.info("No se encontraron registros para la combinación de filtros seleccionada.")
    else:
        chart_b.echarts_chart(opciones_cambio(cambios))
        tabla_b.dataframe(
            cambios.assign(POSICION=cambios["POSICION"].map(NOMBRES_POSICION)),
            key="objetivo2_tabla_b",
            hide_index=True,
            column_config={
                "POSICION": st.column_config.TextColumn("Posición"),
                "GRUPO_ETARIO": st.column_config.TextColumn("Grupo etario"),
                "CAMBIO_PROMEDIO": st.column_config.NumberColumn("Cambio promedio por temporada", format="%.1f"),
                "REGISTROS": st.column_config.NumberColumn("Registros", format="%d"),
            },
        )
    
    tarjetas_objetivo2(tarjetas_slot, datos, cambios)
    texto_slot.markdown(interpretar_objetivo2(datos, cambios))