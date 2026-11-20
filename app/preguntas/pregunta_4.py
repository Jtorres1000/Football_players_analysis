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
    WITH traspasos AS (
    SELECT
        t.transfer_id,
        t.player_id,
        t.transfer_type,
        t.transfer_fee_eur,
        d_dest.division_strength - d_orig.division_strength AS dif_fuerza
    FROM transfers t
    JOIN clubs c_orig      ON c_orig.club_id = t.from_club_id
    JOIN clubs c_dest      ON c_dest.club_id = t.to_club_id
    JOIN divisions d_orig  ON d_orig.division_id = c_orig.division_id
    JOIN divisions d_dest  ON d_dest.division_id = c_dest.division_id
    WHERE t.from_club_id <> t.to_club_id
),
clasificados AS (
    SELECT
        tr.*,
        CASE
            WHEN tr.dif_fuerza > 5  THEN 'ascenso'
            WHEN tr.dif_fuerza < -5 THEN 'descenso'
            ELSE 'lateral'
        END AS movimiento,
        a.agency_name AS agencia
    FROM traspasos tr
    JOIN players p     ON p.player_id = tr.player_id
    LEFT JOIN agents a ON a.agent_id = p.agent_id
),
mercado AS (
    SELECT AVG(CASE WHEN movimiento = 'ascenso' THEN 1.0 ELSE 0 END) AS prop_ascensos_mercado
    FROM clasificados
),
por_agencia AS (
    SELECT
        agencia,
        COUNT(*) AS traspasos,
        AVG(CASE WHEN movimiento = 'ascenso'  THEN 1.0 ELSE 0 END) AS prop_ascensos,
        AVG(CASE WHEN movimiento = 'descenso' THEN 1.0 ELSE 0 END) AS prop_descensos,
        SUM(CASE WHEN movimiento = 'ascenso'  THEN 1 ELSE 0 END)
          - SUM(CASE WHEN movimiento = 'descenso' THEN 1 ELSE 0 END) AS saldo_neto,
        AVG(dif_fuerza) AS dif_fuerza_promedio,
        AVG(CASE WHEN movimiento = 'ascenso' AND transfer_type = 'Permanent'
                 THEN transfer_fee_eur END) AS monto_medio_ascensos
    FROM clasificados
    WHERE agencia IS NOT NULL
    GROUP BY agencia
    HAVING COUNT(*) >= 30
),
ranking AS (
    SELECT pa.*, RANK() OVER (ORDER BY saldo_neto DESC) AS puesto
    FROM por_agencia pa
)
SELECT
    r.puesto                                              AS puesto,
    r.agencia                                             AS agencia,
    r.traspasos                                           AS cantidad_traspasos,
    ROUND(r.prop_ascensos, 3)                             AS proporcion_ascensos,
    ROUND(r.prop_descensos, 3)                            AS proporcion_descensos,
    r.saldo_neto                                          AS saldo_neto,
    ROUND(r.dif_fuerza_promedio, 2)                       AS diferencia_fuerza_promedio,
    ROUND(r.monto_medio_ascensos, 0)                      AS monto_medio_ascensos_definitivos,
    ROUND(r.prop_ascensos - m.prop_ascensos_mercado, 3)   AS diferencia_vs_mercado
FROM ranking r
CROSS JOIN mercado m
WHERE r.puesto <= 10
ORDER BY r.puesto, r.agencia;
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
