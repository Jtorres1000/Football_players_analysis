import streamlit as st
import pandas as pd #Ya no usaré plotly para los gráficos, usaré echarts y para eso necesito pandas}

from components import banner
from utils import query_filtered_data

#Diseño de una especie de diccionario de colores para alimentar futuros echarts con mayor facilidad, use de referencia DESIGN.md

COLORES_GRUPO = {
    "15-21": "#00ff87", #Verde claro
    "22-26": "#04f5ff", #Cian
    "27-31": "#ffb1c4", #Rosa claro
    "32-38": "#ff2882", #Magenta
}

#Función que arma cada interpretación con los números traiga "datos" en ese momento, así cada temporada sale con su propia interpretación y con cualquier combinación de filtros

def interpretar_objetivo1(datos):
    temporadas = sorted(datos["TEMPORADA"].unique())
    ultima = datos[datos["TEMPORADA"] == temporadas[-1]]
    mejor = ultima.loc[ultima["HABILIDAD_PROMEDIO"].idxmax()]
    peor = ultima.loc[ultima["HABILIDAD_PROMEDIO"].idxmin()]
    menos = ultima.loc[ultima["JUGADORES"].idxmin()]
    
    if len(ultima) == 1:
        texto = f"En {temporadas[-1]}, el grupo {mejor['GRUPO_ETARIO']} tiene una habilidad promedio de {mejor['HABILIDAD_PROMEDIO']}. "
    else:
        texto = (
            f"En {temporadas[-1]}, el grupo {mejor['GRUPO_ETARIO']} tiene la habilidad promedio más alta "
            f"({mejor['HABILIDAD_PROMEDIO']}) y el grupo {peor['GRUPO_ETARIO']} la más baja ({peor['HABILIDAD_PROMEDIO']}). "
            f"El grupo con menos jugadores es {menos['GRUPO_ETARIO']} ({menos['JUGADORES']}). "
        )             
    if mejor["GRUPO_ETARIO"] == "32-38" and len(ultima) > 1:
        texto += (
            "Esto no significa que los jugadores mejoren después de los 32 años: a esa edad solo siguen activos "
            "los de mayor nivel (sesgo de supervivencia). "
        )
        
    if temporadas == ["2025/26"]:
        texto += "Esta temporada corresponde a datos reales."
    elif "2025/26" in temporadas:
        texto += "Las temporadas 2022/23 a 2024/25 son datos generados; solo 2025/26 corresponde a datos reales."
    else:
        texto += "Las temporadas seleccionadas son datos generados, no reales."

    return texto

#Como echarts no recibe un Dataframe como plotly sino un diccionario de opciones armaré ese diccionario a partir de "datos" con esta función

def opciones_objetivo1(datos):
    temporadas = sorted(datos["TEMPORADA"].unique())
    tipo = "line" if len(temporadas) > 1 else "bar" #Cuando elegías una sola temporada el gráfico mostraba puntos sueltos en el aire, así que decidí que fueran de barras
    
    series = []
    for grupo, filas in datos.groupby("GRUPO_ETARIO"):
        valores = filas.set_index("TEMPORADA").reindex(temporadas)["HABILIDAD_PROMEDIO"]
        series.append({
            "name": grupo,
            "type": tipo,
            "data": [None if pd.isna(v) else float(v) for v in valores],
            "itemStyle": {"color": COLORES_GRUPO.get(grupo)},
        })
        
    return {
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 0},
        "xAxis": {"type": "category", "data": temporadas, "name": "Temporada"},
        "yAxis": {"type": "value", "name": "Habilidad promedio", "scale": tipo == "line"},
        "series": series,
    }

#Función para hacer los texto más cortos y visuales

def tarjetas_objetivo1(slot, datos):
    temporadas = sorted(datos["TEMPORADA"].unique())
    inicio = datos[datos["TEMPORADA"] == temporadas[0]].set_index("GRUPO_ETARIO")["HABILIDAD_PROMEDIO"]
    fin = datos[datos["TEMPORADA"] == temporadas[-1]].set_index("GRUPO_ETARIO")["HABILIDAD_PROMEDIO"]
    
    columnas = slot.columns(len(fin))
    for columna, (grupo, valor) in zip(columnas, fin.items()):
        delta = None
        if len(temporadas) > 1 and grupo in inicio:
            delta = round(valor - inicio[grupo], 1)
        columna.metric(
            label=f"Grupo {grupo} · {temporadas[-1]}",
            value=valor,
            delta=delta,
            help=f"Cambio entre {temporadas[0]} y {temporadas[-1]}",
            border=True,
        )

def p_exploratorio():
    banner(
        title="Análisis Exploratorio",
        subtitle="Rendimiento, longevidad y salario de los futbolistas según grupo etario y posición, periodo 2022-2026", 
    )
    st.subheader("Objetivo 1: Habilidad promedio por grupo etario, periodo 2022-2026")

    # Reservar contenedores para renderizar la interfaz estática antes de cargar datos
    chart_slot = st.container()

    # Interpretación y bosquejo de datos
    st.subheader("Interpretación")
    metricas_slot = st.container()
    texto_slot = st.container()

    st.subheader("Datos utilizados")
    st.markdown(
        "Empleamos el modelo dimensional para esto, se unió la tabla de hechos `FACT_PLAYER_SEASON` con las dimensiones: `DIM_SEASON`, `DIM_AGE_BRACKET` y `DIM_PLAYER`. Cada fila de la tabla siguiente representa el promedio de un grupo etario en una temporada según los filtros globales seleccionados en la barra lateral."
    )
    table_slot = st.container()

    datos = query_filtered_data("""
        SELECT
            SEASON_LABEL AS TEMPORADA,
            AGE_GROUP AS GRUPO_ETARIO,
            ROUND(AVG(ABILITY_SCORE), 1) AS HABILIDAD_PROMEDIO,
            COUNT(*) AS JUGADORES
        FROM df_filtrado
        GROUP BY SEASON_LABEL, AGE_GROUP
        ORDER BY TEMPORADA, GRUPO_ETARIO
    """)

    if datos.empty:
        chart_slot.info(
            "No se encontraron registros para la combinación de filtros seleccionada en la barra lateral."
        )
        return

    chart_slot.echarts_chart(opciones_objetivo1(datos)) 
    table_slot.dataframe(
        datos,
        key="exploratorio_datos_df",
        hide_index=True,
        column_config={
            "TEMPORADA": st.column_config.TextColumn("Temporada"),
            "GRUPO_ETARIO": st.column_config.TextColumn("Grupo etario"),
            "HABILIDAD_PROMEDIO": st.column_config.NumberColumn("Habilidad promedio", format="%.1f"),
            "JUGADORES": st.column_config.NumberColumn("Jugadores", format="%d"),
        },
    )
    tarjetas_objetivo1(metricas_slot, datos)
    texto_slot.markdown(interpretar_objetivo1(datos))