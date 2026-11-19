import streamlit as st
from utils import query_local_duckdb

def pregunta_3():
    st.markdown("##### Pregunta 3: Inflación del Mercado de Traspasos por Categoría")
    st.markdown("""
Se quiere saber si el precio de los traspasos crece de una temporada a otra y qué tan concentrado está el gasto.

Trabajá solo con traspasos definitivos con monto pagado mayor a cero, y descartá los registros que no representan un movimiento real entre dos clubes. Para cada temporada y categoría principal del jugador calculá la cantidad de traspasos, el monto mediano (sin funciones de percentil), el monto medio, la variación porcentual de la mediana respecto de la temporada anterior de la misma categoría, la proporción del gasto total que concentra el 10 % de traspasos más caros y un indicador de asimetría definido como el cociente entre la media y la mediana.

Ordená por categoría y, dentro de ella, cronológicamente.
    """)
    query = """
        -- Consulta SQL pendiente
    """
    st.markdown("##### Consulta SQL empleada:")
    st.code(query, language='sql')
    if st.button("Ejecutar", key="pregunta_3"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.dataframe(df)
