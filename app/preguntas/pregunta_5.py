import streamlit as st
from utils import query_local_duckdb

def pregunta_5():
    st.markdown("##### Pregunta 5: Arqueros Diferenciales según el Nivel de la Liga")
    st.markdown("""
Comparar arqueros de ligas de distinto nivel es injusto: la comparación debe hacerse entre pares.

Dividí las divisiones en cuatro niveles con igual cantidad de divisiones según su fuerza (el corte se hace sobre las divisiones, no sobre los jugadores). Considerá arqueros a quienes tienen el arco entre sus posiciones naturales y jugaron al menos 1800 minutos en la temporada.

Para cada temporada y nivel obtené los tres arqueros con más goles evitados por 90 minutos (desempate por minutos jugados), mostrando su club, el valor, la cantidad de arqueros que compiten en ese nivel, el promedio del nivel y la diferencia con ese promedio. Agregá una columna que indique si el arquero también estuvo entre los tres mejores de su nivel en la temporada cronológicamente anterior ('Sí', 'No' o 'N/A' cuando no existe temporada anterior). Ordená cronológicamente y del nivel más fuerte al más débil.
    """)
    query = """
        -- Consulta SQL pendiente
    """
    st.markdown("##### Consulta SQL empleada:")
    st.code(query, language='sql')
    if st.button("Ejecutar", key="pregunta_5"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.dataframe(df)
