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
WITH arqueros_naturales AS (
    SELECT DISTINCT
        pp.player_id
    FROM player_positions pp
    INNER JOIN positions pos
        ON pp.position_id = pos.position_id
    WHERE UPPER(pos.role_code) = 'GK'
),
temporadas_ordenadas AS (
    SELECT
        s.season_id,
        s.season_label,
        s.season_order,
        LAG(s.season_id) OVER (ORDER BY s.season_order DESC) AS temporada_anterior_id
    FROM seasons s
),
divisiones_niveles AS (
    SELECT
        d.division_id,
        d.division_name,
        d.division_strength,
        NTILE(4) OVER (
            ORDER BY d.division_strength DESC, d.division_name ASC
        ) AS nivel_liga
    FROM divisions d
    WHERE d.division_strength IS NOT NULL
),
arqueros_temporada AS (
    SELECT
        ps.player_season_id,
        ps.player_id,
        ps.season_id,
        p.name AS nombre_arquero,
        c.club_name AS nombre_club,
        dn.nivel_liga,
        ps.mins AS minutes_played,
        COALESCE(
            sg.expected_goals_prevented_per_90,
            (1.0 * COALESCE(sg.expected_goals_prevented, 0) / NULLIF(ps.mins, 0)) * 90.0,
            0.0
        ) AS goles_evitados_por_90
    FROM player_seasons ps
    INNER JOIN players p
        ON ps.player_id = p.player_id
    INNER JOIN arqueros_naturales an
        ON p.player_id = an.player_id
    INNER JOIN clubs c
        ON ps.club_id = c.club_id
    INNER JOIN divisiones_niveles dn
        ON c.division_id = dn.division_id
    LEFT JOIN player_stats_goalkeeping sg
        ON ps.player_season_id = sg.player_season_id
    WHERE ps.mins >= 1800
),
arqueros_rankeados AS (
    SELECT
        to_ord.season_id,
        to_ord.season_label,
        to_ord.season_order,
        to_ord.temporada_anterior_id,
        arq_temp.nivel_liga,
        arq_temp.player_id,
        arq_temp.nombre_arquero,
        arq_temp.nombre_club,
        arq_temp.minutes_played,
        arq_temp.goles_evitados_por_90,
        COUNT(*) OVER (
            PARTITION BY to_ord.season_id, arq_temp.nivel_liga
        ) AS cantidad_arqueros_nivel,
        AVG(arq_temp.goles_evitados_por_90) OVER (
            PARTITION BY to_ord.season_id, arq_temp.nivel_liga
        ) AS promedio_nivel,
        arq_temp.goles_evitados_por_90 - AVG(arq_temp.goles_evitados_por_90) OVER (
            PARTITION BY to_ord.season_id, arq_temp.nivel_liga
        ) AS diferencia_promedio,
        ROW_NUMBER() OVER (
            PARTITION BY to_ord.season_id, arq_temp.nivel_liga
            ORDER BY arq_temp.goles_evitados_por_90 DESC, arq_temp.minutes_played DESC, arq_temp.player_id ASC
        ) AS posicion_ranking
    FROM arqueros_temporada arq_temp
    INNER JOIN temporadas_ordenadas to_ord
        ON arq_temp.season_id = to_ord.season_id
),
top_3_nivel AS (
    SELECT DISTINCT
        season_id,
        nivel_liga,
        player_id
    FROM arqueros_rankeados
    WHERE posicion_ranking <= 3
)
SELECT
    ar.season_label AS "Temporada",
    ar.nivel_liga AS "Nivel de Liga",
    ar.nombre_arquero AS "Arquero",
    ar.nombre_club AS "Club",
    ROUND(ar.goles_evitados_por_90, 4) AS "Goles Evitados por 90 Min",
    ar.cantidad_arqueros_nivel AS "Arqueros en el Nivel",
    ROUND(ar.promedio_nivel, 4) AS "Promedio del Nivel",
    ROUND(ar.diferencia_promedio, 4) AS "Diferencia con el Promedio",
    CASE
        WHEN ar.temporada_anterior_id IS NULL THEN 'N/A'
        WHEN EXISTS (
            SELECT 1
            FROM top_3_nivel t3_prev
            WHERE t3_prev.season_id = ar.temporada_anterior_id
              AND t3_prev.nivel_liga = ar.nivel_liga
              AND t3_prev.player_id = ar.player_id
        ) THEN 'Sí'
        ELSE 'No'
    END AS "Top 3 Temporada Anterior"
FROM arqueros_rankeados ar
WHERE ar.posicion_ranking <= 3
ORDER BY
    ar.season_order DESC,
    ar.nivel_liga ASC,
    ar.posicion_ranking ASC;
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
