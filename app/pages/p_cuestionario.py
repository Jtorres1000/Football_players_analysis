import streamlit as st
from components import banner
from utils import query_local_duckdb

def p_cuestionario():
    banner(
        title="Cuestionario SQL",
    )
    query = st.text_input("Ingrese su consulta SQL:")

    if st.button("Ejecutar"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
                st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.markdown(f"**Número de filas:** {len(df)}")
            st.dataframe(df)