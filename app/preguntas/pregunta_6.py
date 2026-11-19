import streamlit as st
from utils import query_local_duckdb

def pregunta_6():
    st.markdown("##### Pregunta 6: Mediocampistas Creativos Infravalorados")
    st.markdown("""
En la temporada más reciente —la única no reconstruida— se buscan mediocampistas cuya producción creativa supere lo que refleja su valoración.

Considerá a los jugadores con al menos 1500 minutos que tengan entre sus posiciones naturales la de mediocampista o mediapunta por el centro. Dividí las divisiones en cuatro niveles con igual cantidad de divisiones según su fuerza y, dentro de cada nivel, calculá el rango percentil de cada jugador en pases progresivos por 90, pases clave por 90, asistencias esperadas por 90 y precisión de pase. El índice creativo es el promedio de esos cuatro percentiles. Calculá también, dentro del mismo nivel, el rango percentil de su valoración.

La brecha es la diferencia entre el índice creativo y el percentil de valoración. Entre los jugadores con índice de al menos 0,75 mostrá los quince de mayor brecha con su código de país, club, división, edad, índice, percentil de valoración, brecha, salario semanal del contrato que lo vincula con su club actual (el más reciente si hay más de uno) y su puesto en la escala salarial del plantel con el formato 'puesto/tamaño del plantel'.
    """)
    query = """
        -- Consulta SQL pendiente
    """
    st.markdown("##### Consulta SQL empleada:")
    st.code(query, language='sql')
    if st.button("Ejecutar", key="pregunta_6"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.dataframe(df)
