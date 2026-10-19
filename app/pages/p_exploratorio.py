import streamlit as st
import plotly.express as px

from utils import query_filtered_data


def p_exploratorio():
    st.title("Análisis Exploratorio")
    st.subheader("Objetivo 1: Habilidad promedio por grupo etario, periodo 2022-2026")

    # Reservar contenedores para renderizar la interfaz estática antes de cargar datos
    chart_slot = st.container()

    # Interpretación y bosquejo de datos
    st.subheader("Interpretación")
    st.markdown(
        "En las cuatro temporadas la habilidad promedio aumenta con la edad: el grupo de 15-21 años tiene el valor más bajo (371) y el de 32-38 el más alto (508). Pero esto no significa que los jugadores mejoren después de los 32 años, sino que a esa edad solo siguen activos los de mayor nivel (gracias al sesgo de supervivencia), además de ser el grupo más pequeño (271 en 2022/23). A lo largo del periodo, el grupo de 22-26 sube de 386 a 417 y el de 27-31 baja de 482 a 416, de modo que en 2025/26 quedan casi igualados. Un dato a considerar es que las temporadas 2022/23 a 2024/25 son datos generados, es decir fabricados; y que solo 2025/26 corresponde a datos reales."
    )

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

    grafico = px.line(
        datos,
        x="TEMPORADA",
        y="HABILIDAD_PROMEDIO",
        color="GRUPO_ETARIO",
        markers=True,
    )
    chart_slot.plotly_chart(grafico)
    table_slot.dataframe(datos, key="exploratorio_datos_df")