import streamlit as st
from components import banner
from utils import query_local_duckdb
from preguntas import (
    pregunta_1,
    pregunta_2,
    pregunta_3,
    pregunta_4,
    pregunta_5,
    pregunta_6,
)

def p_cuestionario():
    banner(
        title="Cuestionario SQL",
    )
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        'Pregunta 1',
        'Pregunta 2',
        'Pregunta 3',
        'Pregunta 4',
        'Pregunta 5',
        'Pregunta 6',
    ])

    with tab1:
        pregunta_1()
    with tab2:
        pregunta_2()
    with tab3:
        pregunta_3()
    with tab4:
        pregunta_4()
    with tab5:
        pregunta_5()
    with tab6:
        pregunta_6()

    st.divider()
    st.markdown("### Consulta SQL personalizada")
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