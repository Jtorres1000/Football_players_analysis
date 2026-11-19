import streamlit as st
from utils import query_local_duckdb

def pregunta_1():
    st.markdown("##### Pregunta 1: Progresión Sostenida de la Valoración")
    st.markdown("""
La valoración de cada jugador (ability_score) se registra temporada a temporada. Interesa saber qué perfiles mejoran de forma sostenida y a qué edad ocurre.

Considerá solo a los jugadores con registro en las cuatro temporadas. Para cada uno calculá la variación de su valoración entre cada temporada y la anterior en orden cronológico, y marcalo como de progresión sostenida si las tres variaciones son positivas. Clasificalo según su edad en la primera temporada registrada en uno de cuatro tramos: hasta 21, de 22 a 25, de 26 a 29 y 30 o más.

Para cada categoría principal y tramo mostrá la cantidad de jugadores, cuántos progresaron de forma sostenida, la proporción, la mejora total promedio de quienes progresaron y el puesto del tramo dentro de su categoría según esa proporción. Agregá en cada fila el nombre del jugador de la categoría con la mayor mejora total entre los de progresión sostenida. Los tramos deben aparecer en orden de edad, no alfabético.
    """)
    query = """
        -- Consulta SQL pendiente
    """
    st.markdown("##### Consulta SQL empleada:")
    st.code(query, language='sql')
    if st.button("Ejecutar", key="pregunta_1"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.dataframe(df)
