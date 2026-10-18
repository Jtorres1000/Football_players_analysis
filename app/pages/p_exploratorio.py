import streamlit as st
import plotly.express as px

def p_exploratorio():
    st.title("Análisis Exploratorio")
    st.subheader("Objetivo 1: Habilidad promedio por grupo etario, periodo 2022-2026")
    conn = st.connection("snowflake") #Conexión y query para responder Objetivo 1
    datos = conn.query("""
                select s."season_label" as temporada,
            case when cast(p."age" as int) < 22 then '15-21'
                 when cast(p."age" as int) < 27 then '22-26'
                 when cast(p."age" as int) < 32 then '27-31'
                 else '32-38' end as grupo_etario,
            round(avg(cast(p."ability_score" as float)), 1) as habilidad_promedio,
            count(*) as jugadores
        from TF_COMPU_II.FOOTBALL_ANALYSIS.PLAYER_SEASONS_RAW p
        join TF_COMPU_II.FOOTBALL_ANALYSIS.SEASONS_RAW s on p."season_id" = s."season_id"
        group by 1, 2
        order by 1, 2
    """)

    grafico = px.line(datos, x="TEMPORADA", y="HABILIDAD_PROMEDIO", color="GRUPO_ETARIO", markers=True) #Gráfico de líneas para mostrar la habilidad promedio por grupo etario a lo largo del tiempo.
    st.plotly_chart(grafico)
    
    #Interpretación y bosquejo de datos
    
    st.subheader("Interpretación")
    st.markdown("En las cuatro temporadas la habilidad promedio aumenta con la edad: el grupo de 15-21 años tiene el valor más bajo (371) y el de 32-38 el más alto (508). Pero esto no significa que los jugadores mejoren después de los 32 años, sino que a esa edad solo siguen activos los de mayor nivel (gracias al sesgo de supervivencia), además de ser el grupo más pequeño (271 en 2022/23). A lo largo del periodo, el grupo de 22-26 sube de 386 a 417 y el de 27-31 baja de 482 a 416, de modo que en 2025/26 quedan casi igualados. Un dato a considerar es que las temporadas 2022/23 a 2024/25 son datos generados, es decir fabricados; y que solo 2025/26 corresponde a datos reales.")
    
    st.subheader("Datos utilizados")
    st.markdown("Tablas: PLAYER_SEASONS_RAW (age, ability_score, season_id) y SEASONS_RAW (season_label), unidas en un JOIN por season_id. Cada fila de la tabla siguiente es el promedio de un grupo etario en una temporada.")
    st.dataframe(datos)