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
WITH traspasos_validos AS (
    SELECT
        t.transfer_id,
        t.season_id,
        s.season_label,
        s.season_order,
        p.primary_category,
        t.transfer_fee_eur
    FROM transfers t
    INNER JOIN players p
        ON t.player_id = p.player_id
    INNER JOIN seasons s
        ON t.season_id = s.season_id
    WHERE t.transfer_type = 'Permanent'
      AND t.transfer_fee_eur > 0
      AND t.from_club_id IS NOT NULL
      AND t.to_club_id IS NOT NULL
      AND t.from_club_id <> t.to_club_id
),
traspasos_ordenados AS (
    SELECT
        season_id,
        season_label,
        season_order,
        primary_category,
        transfer_fee_eur,
        COUNT(*) OVER (
            PARTITION BY season_id, primary_category
        ) AS total_traspasos,
        ROW_NUMBER() OVER (
            PARTITION BY season_id, primary_category
            ORDER BY transfer_fee_eur ASC, transfer_id ASC
        ) AS fila_asc,
        NTILE(10) OVER (
            PARTITION BY season_id, primary_category
            ORDER BY transfer_fee_eur DESC, transfer_id ASC
        ) AS decil_gasto
    FROM traspasos_validos
),
metricas_temporada AS (
    SELECT
        primary_category,
        season_id,
        season_label,
        season_order,
        COUNT(*) AS cantidad_traspasos,
        AVG(
            CASE
                WHEN fila_asc IN ((total_traspasos + 1) // 2, (total_traspasos + 2) // 2)
                THEN transfer_fee_eur
            END
        ) AS monto_mediano,
        AVG(transfer_fee_eur) AS monto_medio,
        SUM(
            CASE
                WHEN decil_gasto = 1
                THEN transfer_fee_eur
                ELSE 0
            END
        ) * 1.0 / SUM(transfer_fee_eur) AS proporcion_gasto_top_10
    FROM traspasos_ordenados
    GROUP BY
        primary_category,
        season_id,
        season_label,
        season_order
)
SELECT
    primary_category AS categoria_principal,
    season_label AS temporada,
    cantidad_traspasos,
    ROUND(monto_mediano, 2) AS monto_mediano_eur,
    ROUND(monto_medio, 2) AS monto_medio_eur,
    ROUND(
        (monto_mediano - LAG(monto_mediano) OVER (
            PARTITION BY primary_category
            ORDER BY season_order DESC
        )) * 100.0
        / LAG(monto_mediano) OVER (
            PARTITION BY primary_category
            ORDER BY season_order DESC
        ),
        2
    ) AS variacion_porcentual_mediana,
    ROUND(proporcion_gasto_top_10, 4) AS proporcion_gasto_top_10,
    ROUND(monto_medio * 1.0 / monto_mediano, 4) AS indicador_asimetria
FROM metricas_temporada
ORDER BY
    categoria_principal ASC,
    season_order DESC;
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
