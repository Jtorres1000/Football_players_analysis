import streamlit as st
from utils import query_local_duckdb

def pregunta_2():
    st.markdown("##### Pregunta 2: Efecto de las Lesiones sobre la Temporada Siguiente")
    st.markdown("""
Para medir el costo deportivo de una lesión no alcanza con mirar al lesionado: hay que compararlo con lo que les ocurrió a jugadores similares que no se lesionaron.

Clasificá cada lesión por gravedad según los días de baja: leve (menos de 14), moderada (de 14 a 59) y grave (60 o más). Para cada lesión compará la temporada anterior a la de la lesión con la temporada posterior: variación de minutos jugados, variación del rating promedio y si el jugador cambió de club entre la temporada de la lesión y la siguiente. Solo pueden evaluarse las lesiones que tengan temporada anterior y posterior.

Construí una línea de base con los jugadores de la misma categoría principal que no registran lesión en esa misma temporada, medidos con el mismo criterio. Para cada gravedad y categoría mostrá la cantidad de casos, el efecto neto (promedio de los lesionados menos promedio de su línea de base) sobre minutos, sobre rating y sobre la tasa de cambio de club, y el ranking de las categorías dentro de cada gravedad según el efecto neto en minutos, de más a menos perjudicial. Ordená por gravedad de menor a mayor.
    """)
    query = """
        -- Consulta SQL pendiente
    """
    st.markdown("##### Consulta SQL empleada:")
    st.code(query, language='sql')
    if st.button("Ejecutar", key="pregunta_2"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.dataframe(df)
