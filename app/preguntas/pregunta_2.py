import streamlit as st
from utils import query_local_duckdb

def pregunta_2():
    st.markdown("##### Pregunta 2: Efecto de las Lesiones sobre la Temporada Siguiente")
    st.markdown("""
Para medir el costo deportivo de una lesión no alcanza con mirar al lesionado: hay que compararlo con lo que les ocurrió a jugadores similares que no se lesionaron.

Clasificá cada lesión por gravedad según los días de baja: leve (menos de 14), moderada (de 14 a 59) y grave (60 o más). Para cada lesión compará la temporada anterior a la de la lesión con la temporada posterior: variación de minutos jugados, variación del rating promedio y si el jugador cambió de club entre la temporada de la lesión y la siguiente. Solo pueden evaluarse las lesiones que tengan temporada anterior y posterior.

Construí una línea de base con los jugadores de la misma categoría principal que no registran lesión en esa misma temporada, medidos con el mismo criterio. Para cada gravedad y categoría mostrá la cantidad de casos, el efecto neto (promedio de los lesionados menos promedio de su línea de base) sobre minutos, sobre rating y sobre la tasa de cambio de club, y el ranking de las categorías dentro de cada gravedad según el efecto neto en minutos, de más a menos perjudicial. Ordená por gravedad de menor a mayor.
    """)
    query = """
         WITH trayectoria_jugador AS (
    SELECT
        ps.player_id,
        p.primary_category,
        ps.season_id,
        s.season_order,
        ps.club_id AS club_actual,
        LAG(s.season_order) OVER (
            PARTITION BY ps.player_id
            ORDER BY s.season_order DESC
        ) AS orden_temporada_anterior,
        LEAD(s.season_order) OVER (
            PARTITION BY ps.player_id
            ORDER BY s.season_order DESC
        ) AS orden_temporada_posterior,
        LAG(ps.mins) OVER (
            PARTITION BY ps.player_id
            ORDER BY s.season_order DESC
        ) AS mins_anterior,
        LEAD(ps.mins) OVER (
            PARTITION BY ps.player_id
            ORDER BY s.season_order DESC
        ) AS mins_posterior,
        LAG(psg.average_rating) OVER (
            PARTITION BY ps.player_id
            ORDER BY s.season_order DESC
        ) AS rating_anterior,
        LEAD(psg.average_rating) OVER (
            PARTITION BY ps.player_id
            ORDER BY s.season_order DESC
        ) AS rating_posterior,
        LEAD(ps.club_id) OVER (
            PARTITION BY ps.player_id
            ORDER BY s.season_order DESC
        ) AS club_posterior
    FROM player_seasons ps
    INNER JOIN players p
        ON ps.player_id = p.player_id
    INNER JOIN seasons s
        ON ps.season_id = s.season_id
    INNER JOIN player_stats_general psg
        ON ps.player_season_id = psg.player_season_id
),
casos_evaluables AS (
    SELECT
        t.player_id,
        t.primary_category,
        t.season_id,
        (t.mins_posterior - t.mins_anterior) * 1.0 AS variacion_minutos,
        (t.rating_posterior - t.rating_anterior) * 1.0 AS variacion_rating,
        CASE
            WHEN t.club_posterior <> t.club_actual THEN 1.0
            ELSE 0.0
        END AS cambio_club,
        i.injury_id,
        CAST(i.end_date AS DATE) - CAST(i.start_date AS DATE) AS dias_baja
    FROM trayectoria_jugador t
    LEFT JOIN injuries i
        ON t.player_id = i.player_id
       AND t.season_id = i.season_id
    WHERE t.orden_temporada_anterior = t.season_order + 1
      AND t.orden_temporada_posterior = t.season_order - 1
),
linea_base AS (
    SELECT
        c.season_id,
        c.primary_category,
        AVG(c.variacion_minutos) AS base_variacion_minutos,
        AVG(c.variacion_rating) AS base_variacion_rating,
        AVG(c.cambio_club) AS base_tasa_cambio_club
    FROM casos_evaluables c
    WHERE c.injury_id IS NULL
    GROUP BY
        c.season_id,
        c.primary_category
),
lesiones_clasificadas AS (
    SELECT
        c.injury_id,
        c.season_id,
        c.primary_category,
        c.variacion_minutos,
        c.variacion_rating,
        c.cambio_club,
        CASE
            WHEN c.dias_baja < 14 THEN 'Leve'
            WHEN c.dias_baja <= 59 THEN 'Moderada'
            ELSE 'Grave'
        END AS gravedad_lesion,
        CASE
            WHEN c.dias_baja < 14 THEN 1
            WHEN c.dias_baja <= 59 THEN 2
            ELSE 3
        END AS orden_gravedad
    FROM casos_evaluables c
    WHERE c.injury_id IS NOT NULL
),
efectos_agrupados AS (
    SELECT
        l.gravedad_lesion,
        l.orden_gravedad,
        l.primary_category AS categoria_principal,
        COUNT(*) AS cantidad_casos,
        AVG(l.variacion_minutos - b.base_variacion_minutos) AS efecto_neto_minutos,
        AVG(l.variacion_rating - b.base_variacion_rating) AS efecto_neto_rating,
        AVG(l.cambio_club - b.base_tasa_cambio_club) AS efecto_neto_tasa_cambio_club
    FROM lesiones_clasificadas l
    INNER JOIN linea_base b
        ON l.season_id = b.season_id
       AND l.primary_category = b.primary_category
    GROUP BY
        l.gravedad_lesion,
        l.orden_gravedad,
        l.primary_category
)
SELECT
    gravedad_lesion,
    categoria_principal,
    cantidad_casos,
    ROUND(efecto_neto_minutos, 2) AS efecto_neto_minutos,
    ROUND(efecto_neto_rating, 4) AS efecto_neto_rating,
    ROUND(efecto_neto_tasa_cambio_club, 4) AS efecto_neto_tasa_cambio_club,
    RANK() OVER (
        PARTITION BY gravedad_lesion
        ORDER BY efecto_neto_minutos ASC
    ) AS ranking_perjuicio_minutos
FROM efectos_agrupados
ORDER BY
    orden_gravedad ASC,
    ranking_perjuicio_minutos ASC;
    """
    st.markdown("##### Consulta SQL empleada:")
    st.code(query, language='sql')
    if st.button("Ejecutar", key="pregunta_2"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.dataframe(df)
