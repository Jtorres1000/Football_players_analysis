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
WITH temporada_actual AS (
    SELECT
        season_id
    FROM seasons
    WHERE season_order = 0
      AND is_fabricated = 0
),
niveles_division AS (
    SELECT
        division_id,
        division_name,
        division_strength,
        NTILE(4) OVER (
            ORDER BY division_strength DESC, division_id ASC
        ) AS nivel_division
    FROM divisions
    WHERE division_strength IS NOT NULL
),
contrato_vigente_por_club AS (
    SELECT
        player_id,
        club_id,
        weekly_wage_eur,
        ROW_NUMBER() OVER (
            PARTITION BY player_id, club_id
            ORDER BY start_date DESC, end_date DESC, contract_id DESC
        ) AS rn_contrato
    FROM contracts
),
escala_salarial_plantel AS (
    SELECT
        ps.player_id,
        ps.club_id,
        cv.weekly_wage_eur AS salario_semanal,
        RANK() OVER (
            PARTITION BY ps.club_id
            ORDER BY cv.weekly_wage_eur DESC
        ) AS puesto_salarial,
        COUNT(*) OVER (
            PARTITION BY ps.club_id
        ) AS tamano_plantel
    FROM player_seasons ps
    INNER JOIN temporada_actual ta
        ON ps.season_id = ta.season_id
    LEFT JOIN contrato_vigente_por_club cv
        ON ps.player_id = cv.player_id
       AND ps.club_id = cv.club_id
       AND cv.rn_contrato = 1
    WHERE ps.club_id IS NOT NULL
),
mediocampistas_elegibles AS (
    SELECT
        ps.player_season_id,
        ps.player_id,
        p.name AS nombre_jugador,
        n.nation_code AS codigo_pais,
        c.club_id,
        c.club_name AS club,
        nd.division_name AS division,
        nd.nivel_division,
        ps.age AS edad,
        ps.ability_score,
        psp.progressive_passes_per_90,
        psp.key_passes_per_90,
        psa.xa_per_90,
        psp.pass_completion_ratio
    FROM player_seasons ps
    INNER JOIN temporada_actual ta
        ON ps.season_id = ta.season_id
    INNER JOIN players p
        ON ps.player_id = p.player_id
    LEFT JOIN nations n
        ON p.nation_id = n.nation_id
    INNER JOIN clubs c
        ON ps.club_id = c.club_id
    INNER JOIN niveles_division nd
        ON c.division_id = nd.division_id
    INNER JOIN player_stats_passing psp
        ON ps.player_season_id = psp.player_season_id
    INNER JOIN player_stats_attacking psa
        ON ps.player_season_id = psa.player_season_id
    WHERE ps.mins >= 1500
      AND EXISTS (
          SELECT 1
          FROM player_positions pp
          INNER JOIN positions pos
              ON pp.position_id = pos.position_id
          WHERE pp.player_id = ps.player_id
            AND pos.role_code IN ('M', 'AM')
            AND pos.side_code = 'C'
      )
),
percentiles_por_nivel AS (
    SELECT
        me.*,
        PERCENT_RANK() OVER (
            PARTITION BY me.nivel_division
            ORDER BY me.progressive_passes_per_90 ASC
        ) AS pct_pases_progresivos,
        PERCENT_RANK() OVER (
            PARTITION BY me.nivel_division
            ORDER BY me.key_passes_per_90 ASC
        ) AS pct_pases_clave,
        PERCENT_RANK() OVER (
            PARTITION BY me.nivel_division
            ORDER BY me.xa_per_90 ASC
        ) AS pct_asistencias_esperadas,
        PERCENT_RANK() OVER (
            PARTITION BY me.nivel_division
            ORDER BY me.pass_completion_ratio ASC
        ) AS pct_precision_pase,
        PERCENT_RANK() OVER (
            PARTITION BY me.nivel_division
            ORDER BY me.ability_score ASC
        ) AS percentil_valoracion
    FROM mediocampistas_elegibles me
),
indice_y_brecha AS (
    SELECT
        ppn.*,
        (
            ppn.pct_pases_progresivos +
            ppn.pct_pases_clave +
            ppn.pct_asistencias_esperadas +
            ppn.pct_precision_pase
        ) / 4.0 AS indice_creativo,
        (
            (
                ppn.pct_pases_progresivos +
                ppn.pct_pases_clave +
                ppn.pct_asistencias_esperadas +
                ppn.pct_precision_pase
            ) / 4.0
        ) - ppn.percentil_valoracion AS brecha
    FROM percentiles_por_nivel ppn
)
SELECT
    ib.nombre_jugador AS jugador,
    ib.codigo_pais AS codigo_pais,
    ib.club AS club,
    ib.division AS division,
    ib.edad AS edad,
    ROUND(ib.indice_creativo, 4) AS indice_creativo,
    ROUND(ib.percentil_valoracion, 4) AS percentil_valoracion,
    ROUND(ib.brecha, 4) AS brecha,
    esp.salario_semanal AS salario_semanal_eur,
    CAST(esp.puesto_salarial AS TEXT) || '/' || CAST(esp.tamano_plantel AS TEXT) AS puesto_escala_salarial
FROM indice_y_brecha ib
LEFT JOIN escala_salarial_plantel esp
    ON ib.player_id = esp.player_id
   AND ib.club_id = esp.club_id
WHERE ib.indice_creativo >= 0.75
ORDER BY ib.brecha DESC
LIMIT 15;
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
