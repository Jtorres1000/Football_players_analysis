import streamlit as st
from utils import query_local_duckdb

def pregunta_4():
    st.markdown("##### Pregunta 4: Agencias de Representación y Movilidad entre Divisiones")
    st.markdown("""
Un traspaso puede llevar al jugador a una liga más fuerte, a una más débil o a una de nivel similar. Se quiere saber qué agencias logran mover a sus representados hacia arriba.

Para cada traspaso real entre dos clubes calculá la diferencia de fuerza entre la división de destino y la de origen, y clasificalo como ascenso (diferencia mayor a 5), descenso (menor a −5) o lateral. Asociá cada traspaso a la agencia que representa al jugador; tené en cuenta que una agencia agrupa a varios agentes y que hay jugadores sin representante.

Para las agencias con al menos 30 traspasos mostrá la cantidad de traspasos, la proporción de ascensos, la proporción de descensos, el saldo neto (ascensos menos descensos), la diferencia de fuerza promedio, el monto medio de los ascensos que fueron traspasos definitivos y la diferencia entre su proporción de ascensos y la del mercado completo, incluidos los jugadores sin representante. Mostrá las diez agencias con mejor saldo neto junto con su puesto en el ranking (los empates comparten puesto).
    """)
    query = """
        -- Consulta SQL pendiente
    """
    st.markdown("##### Consulta SQL empleada:")
    st.code(query, language='sql')
    if st.button("Ejecutar", key="pregunta_4"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.dataframe(df)
