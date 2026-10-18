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
    