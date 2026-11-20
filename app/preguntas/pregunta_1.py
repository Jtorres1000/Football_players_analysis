import streamlit as st
from utils import query_local_duckdb

def pregunta_1():
    st.markdown("##### Pregunta 1: Progresión Sostenida de la Valoración")
    st.markdown("""
La valoración de cada jugador (ability_score) se registra temporada a temporada. Interesa saber qué perfiles mejoran de forma sostenida y a qué edad ocurre.

Considerá solo a los jugadores con registro en las cuatro temporadas. Para cada uno calculá la variación de su valoración entre cada temporada y la anterior en orden cronológico, y marcalo como de progresión sostenida si las tres variaciones son positivas. Clasificalo según su edad en la primera temporada registrada en uno de cuatro tramos: hasta 21, de 22 a 25, de 26 a 29 y 30 o más.

Para cada categoría principal y tramo mostrá la cantidad de jugadores, cuántos progresaron de forma sostenida, la proporción, la mejora total promedio de quienes progresaron y el puesto del tramo dentro de su categoría según esa proporción. Agregá en cada fila el nombre del jugador de la categoría con la mayor mejora total entre los de progresión sostenida. Los tramos deben aparecer en orden de edad, no alfabético.
    """)
    query = """
        WITH temporadas_completas AS (
    SELECT 
        ps.player_id
    FROM player_seasons ps
    GROUP BY ps.player_id
    HAVING COUNT(DISTINCT ps.season_id) = (SELECT COUNT(*) FROM seasons)
),
historial_jugador AS (
    SELECT 
        ps.player_id,
        p.name AS nombre_jugador,
        p.primary_category,
        ps.age,
        ps.ability_score,
        s.season_order,
        ROW_NUMBER() OVER (
            PARTITION BY ps.player_id 
            ORDER BY s.season_order DESC
        ) AS orden_temporada,
        LAG(ps.ability_score) OVER (
            PARTITION BY ps.player_id 
            ORDER BY s.season_order DESC
        ) AS valoracion_anterior
    FROM player_seasons ps
    INNER JOIN seasons s 
        ON ps.season_id = s.season_id
    INNER JOIN players p 
        ON ps.player_id = p.player_id
    INNER JOIN temporadas_completas tc 
        ON ps.player_id = tc.player_id
),
jugadores_metricas AS (
    SELECT 
        player_id,
        nombre_jugador,
        primary_category,
        MIN(CASE WHEN orden_temporada = 1 THEN age END) AS edad_inicial,
        MIN(CASE WHEN orden_temporada = 4 THEN ability_score END) 
            - MIN(CASE WHEN orden_temporada = 1 THEN ability_score END) AS mejora_total,
        CASE 
            WHEN COUNT(CASE WHEN orden_temporada > 1 AND ability_score > valoracion_anterior THEN 1 END) = 3 
            THEN 1 
            ELSE 0 
        END AS es_progresion_sostenida
    FROM historial_jugador
    GROUP BY player_id, nombre_jugador, primary_category
),
jugadores_clasificados AS (
    SELECT 
        jm.*,
        CASE 
            WHEN jm.edad_inicial <= 21 THEN 'Hasta 21'
            WHEN jm.edad_inicial BETWEEN 22 AND 25 THEN 'De 22 a 25'
            WHEN jm.edad_inicial BETWEEN 26 AND 29 THEN 'De 26 a 29'
            ELSE '30 o más'
        END AS tramo_edad,
        CASE 
            WHEN jm.edad_inicial <= 21 THEN 1
            WHEN jm.edad_inicial BETWEEN 22 AND 25 THEN 2
            WHEN jm.edad_inicial BETWEEN 26 AND 29 THEN 3
            ELSE 4
        END AS orden_tramo
    FROM jugadores_metricas jm
),
mejor_por_categoria AS (
    SELECT 
        primary_category,
        nombre_jugador AS mejor_jugador_categoria
    FROM (
        SELECT 
            primary_category,
            nombre_jugador,
            ROW_NUMBER() OVER (
                PARTITION BY primary_category 
                ORDER BY mejora_total DESC, player_id ASC
            ) AS rn
        FROM jugadores_clasificados
        WHERE es_progresion_sostenida = 1
    )
    WHERE rn = 1
),
resumen_categoria_tramo AS (
    SELECT 
        jc.primary_category,
        jc.tramo_edad,
        jc.orden_tramo,
        COUNT(*) AS cantidad_jugadores,
        SUM(jc.es_progresion_sostenida) AS cantidad_progresion_sostenida,
        1.0 * SUM(jc.es_progresion_sostenida) / COUNT(*) AS proporcion_progresion,
        AVG(CASE WHEN jc.es_progresion_sostenida = 1 THEN jc.mejora_total END) AS mejora_promedio_progresaron
    FROM jugadores_clasificados jc
    GROUP BY jc.primary_category, jc.tramo_edad, jc.orden_tramo
)
SELECT 
    rct.primary_category AS "Categoría Principal",
    rct.tramo_edad AS "Tramo de Edad",
    rct.cantidad_jugadores AS "Cantidad de Jugadores",
    rct.cantidad_progresion_sostenida AS "Jugadores con Progresión Sostenida",
    ROUND(rct.proporcion_progresion, 4) AS "Proporción",
    ROUND(rct.mejora_promedio_progresaron, 4) AS "Mejora Total Promedio",
    DENSE_RANK() OVER (
        PARTITION BY rct.primary_category 
        ORDER BY rct.proporcion_progresion DESC
    ) AS "Puesto del Tramo en Categoría",
    mpc.mejor_jugador_categoria AS "Mejor Jugador de la Categoría"
FROM resumen_categoria_tramo rct
LEFT JOIN mejor_por_categoria mpc 
    ON rct.primary_category = mpc.primary_category
ORDER BY 
    rct.primary_category ASC,
    rct.orden_tramo ASC;
    """
    st.markdown("##### Consulta SQL empleada:")
    st.code(query, language='sql')
    if st.button("Ejecutar", key="pregunta_1"):
        try:
            df = query_local_duckdb(query)
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
        else:
            st.markdown("### Resultados de la consulta:")
            st.dataframe(df)
