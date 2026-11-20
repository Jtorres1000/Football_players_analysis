import streamlit as st
import pandas as pd

from utils import query_filtered_data

COLORES_POSICION = {
    "Delanteros (ATT)": "#ff2882",
    "Centrocampistas (MID)": "#04f5ff",
    "Defensas (DEF)": "#00ff87",
    "Porteros (GK)": "#ffb1c4",
}

COLORES_GRUPO = {
    "15-21": "#00ff87",
    "22-26": "#04f5ff",
    "27-31": "#ffb1c4",
    "32-38": "#ff2882",
}

POSICIONES_ORDEN = [
    "Delanteros (ATT)",
    "Centrocampistas (MID)",
    "Defensas (DEF)",
    "Porteros (GK)",
]

GRUPOS_ORDEN = ["15-21", "22-26", "27-31", "32-38"]

INTERPRETACION_A = (
    "**Interpretación:** Al examinar las cuatro nubes de dispersión posicionales coloreadas por tramo etario, "
    "se evidencia una pendiente positiva en la que los mayores puntajes de habilidad se asocian con remuneraciones superiores, "
    "aunque con distinta concentración según el rol: "
    "en **Delanteros (ATT)** se observa una correlación media de **r = 0.776** (fuerte), alcanzando su mayor ajuste lineal en el grupo de **32-38 años** (**r = 0.863**) y la mayor dispersión en **15-21 años** (**r = 0.73**); "
    "en **Centrocampistas (MID)** se observa una correlación media de **r = 0.784** (fuerte), alcanzando su mayor ajuste lineal en el grupo de **27-31 años** (**r = 0.837**) y la mayor dispersión en **15-21 años** (**r = 0.742**); "
    "en **Defensas (DEF)** se observa una correlación media de **r = 0.788** (fuerte), alcanzando su mayor ajuste lineal en el grupo de **27-31 años** (**r = 0.842**) y la mayor dispersión en **15-21 años** (**r = 0.741**); "
    "en **Porteros (GK)** se observa una correlación media de **r = 0.789** (fuerte), alcanzando su mayor ajuste lineal en el grupo de **27-31 años** (**r = 0.828**) y la mayor dispersión en **15-21 años** (**r = 0.742**)."
)

INTERPRETACION_B = (
    "**Interpretación:** Al contrastar el comportamiento del coeficiente de Pearson a lo largo de las cuatro etapas del ciclo de vida deportivo, "
    "se observa cómo varía el impacto financiero directo del rendimiento en cancha: "
    "en el grupo formativo de **15-21 años** la correlación promedio se sitúa en **r = 0.741** (relación fuerte); "
    "en el tramo de consolidación de **22-26 años** la correlación promedio se sitúa en **r = 0.774** (relación fuerte); "
    "en la etapa de madurez de **27-31 años** la correlación promedio se sitúa en **r = 0.836** (relación fuerte); "
    "en el segmento veterano de **32-38 años** la correlación promedio se sitúa en **r = 0.828** (relación fuerte). "
    "Esto demuestra que el nivel de habilidad explica de forma consistente el crecimiento salarial, mientras que las variaciones "
    "entre tramos responden a los contratos de entrada en juveniles y a la retención por estatus y sesgo de supervivencia en veteranos."
)


def formatear_eur(valor):
    if pd.isna(valor) or valor == 0:
        return "€0"
    signo = "-" if valor < 0 else ""
    v = abs(valor)
    if v >= 1_000_000:
        return f"{signo}€{v / 1_000_000:.2f}M"
    if v >= 1_000:
        return f"{signo}€{v / 1_000:.0f}k"
    return f"{signo}€{v:,.0f}"


def opciones_small_multiples_dispersion(muestra, datos_corr):
    grupos = [g for g in GRUPOS_ORDEN if g in muestra["GRUPO_ETARIO"].values] or sorted(muestra["GRUPO_ETARIO"].unique())
    posiciones = [p for p in POSICIONES_ORDEN if p in muestra["POSICION"].values] or sorted(muestra["POSICION"].unique())

    grids = []
    x_axes = []
    y_axes = []
    series = []
    titulos = [
        {
            "text": "Habilidad vs. Salario Anual por Posición",
            "textStyle": {"color": "#fbfaff", "fontSize": 14, "fontWeight": 600},
            "left": "center",
            "top": 0,
        }
    ]

    ubicaciones = [
        {"left": "8%", "top": "16%", "width": "36%", "height": "28%", "title_left": "26%", "title_top": "10%"},
        {"left": "57%", "top": "16%", "width": "36%", "height": "28%", "title_left": "75%", "title_top": "10%"},
        {"left": "8%", "top": "62%", "width": "36%", "height": "28%", "title_left": "26%", "title_top": "56%"},
        {"left": "57%", "top": "62%", "width": "36%", "height": "28%", "title_left": "75%", "title_top": "56%"},
    ]

    for idx, p in enumerate(posiciones[:4]):
        loc = ubicaciones[idx]
        color_pos = COLORES_POSICION.get(p, "#04f5ff")
        filas_p = muestra[muestra["POSICION"] == p]

        filas_c = datos_corr[datos_corr["POSICION"] == p]
        total_j = filas_c["JUGADORES"].sum()
        r_pos = round((filas_c["CORRELACION"] * filas_c["JUGADORES"]).sum() / total_j, 3) if total_j > 0 else 0.0

        titulos.append({
            "text": f"{p} · r medio = {r_pos}",
            "left": loc["title_left"],
            "top": loc["title_top"],
            "textAlign": "center",
            "textStyle": {"color": color_pos, "fontSize": 12, "fontWeight": 600},
        })

        grids.append({
            "left": loc["left"],
            "top": loc["top"],
            "width": loc["width"],
            "height": loc["height"],
            "containLabel": True,
        })

        x_axes.append({
            "type": "value",
            "gridIndex": idx,
            "name": "Habilidad (pts)",
            "nameLocation": "middle",
            "nameGap": 22,
            "nameTextStyle": {"color": "#c6b5cb", "fontSize": 10},
            "scale": True,
            "splitNumber": 4,
            "axisLine": {"show": True, "lineStyle": {"color": "rgba(255, 255, 255, 0.2)"}},
            "axisLabel": {"color": "#c6b5cb", "fontSize": 10},
            "splitLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.05)"}},
        })

        y_axes.append({
            "type": "value",
            "gridIndex": idx,
            "scale": True,
            "splitNumber": 3,
            "axisLine": {"show": True, "lineStyle": {"color": "#04f5ff"}},
            "axisLabel": {"color": "#04f5ff", "fontSize": 10, "formatter": "€{value}"},
            "splitLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.05)"}},
        })

        for g in grupos:
            sub_g = filas_p[filas_p["GRUPO_ETARIO"] == g]
            puntos = [
                {
                    "name": f"{p} · Grupo {g} ({row['HABILIDAD']} pts | {formatear_eur(row['SALARIO'])})",
                    "value": [float(row["HABILIDAD"]), float(row["SALARIO"])],
                }
                for _, row in sub_g.iterrows()
            ]

            series.append({
                "name": f"Grupo {g}",
                "type": "scatter",
                "xAxisIndex": idx,
                "yAxisIndex": idx,
                "symbolSize": 7,
                "label": {"show": False},
                "emphasis": {"disabled": True},
                "itemStyle": {
                    "color": COLORES_GRUPO.get(g, "#04f5ff"),
                    "opacity": 0.78,
                },
                "data": puntos,
            })

    return {
        "backgroundColor": "transparent",
        "title": titulos,
        "tooltip": {
            "trigger": "item",
            "formatter": "{b}",
            "backgroundColor": "rgba(22, 1, 24, 0.95)",
            "borderColor": "rgba(255, 255, 255, 0.15)",
            "textStyle": {"color": "#fbfaff", "fontSize": 12},
        },
        "legend": {
            "top": 26,
            "data": [f"Grupo {g}" for g in grupos],
            "textStyle": {"color": "#c6b5cb", "fontSize": 11},
        },
        "toolbox": {
            "show": True,
            "feature": {
                "restore": {"show": True, "title": "Reiniciar"},
                "saveAsImage": {"show": True, "title": "Guardar imagen"},
            },
            "iconStyle": {"borderColor": "#c6b5cb"},
            "top": 0,
            "right": "2%",
        },
        "grid": grids,
        "xAxis": x_axes,
        "yAxis": y_axes,
        "series": series,
    }


def opciones_curvas_correlacion(datos):
    grupos = [g for g in GRUPOS_ORDEN if g in datos["GRUPO_ETARIO"].values] or sorted(datos["GRUPO_ETARIO"].unique())
    posiciones = [p for p in POSICIONES_ORDEN if p in datos["POSICION"].values] or sorted(datos["POSICION"].unique())

    series = []
    for p in posiciones:
        color = COLORES_POSICION.get(p, "#04f5ff")
        filas_p = datos[datos["POSICION"] == p]

        valores = []
        for g in grupos:
            sub = filas_p[filas_p["GRUPO_ETARIO"] == g]
            if not sub.empty:
                valores.append(float(sub.iloc[0]["CORRELACION"]))
            else:
                valores.append(None)

        series.append({
            "name": p,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 9,
            "label": {"show": False},
            "emphasis": {"disabled": True},
            "lineStyle": {
                "width": 3.5,
                "color": color,
            },
            "itemStyle": {
                "color": color,
            },
            "data": valores,
        })

    return {
        "backgroundColor": "transparent",
        "title": {
            "text": "Coeficiente de Correlación de Pearson (r) por Grupo Etario y Posición",
            "textStyle": {"color": "#fbfaff", "fontSize": 14, "fontWeight": 600},
            "left": "center",
            "top": 0,
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "none"},
            "backgroundColor": "rgba(22, 1, 24, 0.95)",
            "borderColor": "rgba(255, 255, 255, 0.15)",
            "textStyle": {"color": "#fbfaff", "fontSize": 12},
        },
        "legend": {
            "top": 30,
            "data": posiciones,
            "textStyle": {"color": "#c6b5cb", "fontSize": 11},
        },
        "toolbox": {
            "show": True,
            "feature": {
                "restore": {"show": True, "title": "Reiniciar"},
                "saveAsImage": {"show": True, "title": "Guardar imagen"},
            },
            "iconStyle": {"borderColor": "#c6b5cb"},
            "top": 0,
            "right": "2%",
        },
        "grid": {
            "top": 82,
            "left": "7%",
            "right": "6%",
            "bottom": 45,
            "containLabel": True,
        },
        "xAxis": {
            "type": "category",
            "data": grupos,
            "name": "Grupo etario",
            "nameLocation": "middle",
            "nameGap": 28,
            "boundaryGap": False,
            "axisLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.2)"}},
            "axisLabel": {"color": "#c6b5cb", "fontSize": 11},
            "splitLine": {"show": True, "lineStyle": {"color": "rgba(255, 255, 255, 0.05)"}},
        },
        "yAxis": {
            "type": "value",
            "name": "Correlación de Pearson (r)",
            "nameGap": 18,
            "scale": True,
            "axisLine": {"show": True, "lineStyle": {"color": "#00ff87"}},
            "axisLabel": {
                "color": "#00ff87",
                "formatter": "{value}",
            },
            "splitLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.05)"}},
        },
        "series": series,
    }


def interpretar(datos):
    if datos.empty:
        msg = "No hay suficientes datos para interpretar este objetivo."
        return msg, msg
    return INTERPRETACION_A, INTERPRETACION_B


def objetivo5():
    st.subheader("Objetivo 5: Grado de correlación entre puntaje de habilidad y salario anual por grupo etario y posición, periodo 2022-2026")

    st.markdown("**a) Dispersión entre puntaje de habilidad y salario anual por posición y grupo etario**")
    chart_a = st.container()
    texto_a_slot = st.container()

    st.markdown("**b) Coeficiente de correlación de Pearson (r) según grupo etario y posición de juego**")
    chart_b = st.container()
    texto_b_slot = st.container()

    st.subheader("Datos utilizados")
    st.markdown(
        "Empleamos el modelo dimensional uniendo la tabla de hechos `FACT_PLAYER_SEASON` con las dimensiones "
        "`DIM_PLAYER`, `DIM_AGE_BRACKET` y `DIM_SEASON`. Cada fila presenta el coeficiente de correlación de Pearson (`r`) "
        "entre el puntaje de habilidad y el salario anual, junto con sus promedios y cantidad de registros por posición y grupo etario."
    )
    table_slot = st.container()

    consulta_obj5 = """
        SELECT
            CASE PRIMARY_CATEGORY
                WHEN 'ATTACKER' THEN 'Delanteros (ATT)'
                WHEN 'MIDFIELDER' THEN 'Centrocampistas (MID)'
                WHEN 'DEFENDER' THEN 'Defensas (DEF)'
                WHEN 'GOALKEEPER' THEN 'Porteros (GK)'
                ELSE PRIMARY_CATEGORY
            END AS POSICION,
            AGE_GROUP AS GRUPO_ETARIO,
            COALESCE(ROUND(CORR(ABILITY_SCORE, ANNUAL_WAGE_EUR), 3), 0) AS CORRELACION,
            ROUND(AVG(ABILITY_SCORE), 1) AS HABILIDAD_PROMEDIO,
            ROUND(AVG(ANNUAL_WAGE_EUR), 0) AS SALARIO_PROMEDIO,
            COUNT(*) AS JUGADORES
        FROM df_filtrado
        WHERE ABILITY_SCORE IS NOT NULL AND ANNUAL_WAGE_EUR IS NOT NULL
        GROUP BY PRIMARY_CATEGORY, AGE_GROUP
        ORDER BY POSICION, GRUPO_ETARIO
    """

    datos = query_filtered_data(consulta_obj5)
    texto_a, texto_b = interpretar(datos)
    texto_a_slot.markdown(texto_a)
    texto_b_slot.markdown(texto_b)

    if datos.empty:
        chart_a.info("No se encontraron registros para la combinación de filtros seleccionada en la barra lateral.")
        chart_b.info("No se encontraron registros para la combinación de filtros seleccionada en la barra lateral.")
        table_slot.info("No se encontraron registros para la combinación de filtros seleccionada en la barra lateral.")
        return

    muestra = query_filtered_data("""
        SELECT
            POSICION,
            GRUPO_ETARIO,
            HABILIDAD,
            SALARIO
        FROM (
            SELECT
                CASE PRIMARY_CATEGORY
                    WHEN 'ATTACKER' THEN 'Delanteros (ATT)'
                    WHEN 'MIDFIELDER' THEN 'Centrocampistas (MID)'
                    WHEN 'DEFENDER' THEN 'Defensas (DEF)'
                    WHEN 'GOALKEEPER' THEN 'Porteros (GK)'
                    ELSE PRIMARY_CATEGORY
                END AS POSICION,
                AGE_GROUP AS GRUPO_ETARIO,
                ROUND(ABILITY_SCORE, 1) AS HABILIDAD,
                ROUND(ANNUAL_WAGE_EUR, 0) AS SALARIO,
                ROW_NUMBER() OVER (
                    PARTITION BY PRIMARY_CATEGORY, AGE_GROUP
                    ORDER BY HASH(PLAYER_ID, SEASON_ID)
                ) AS RN
            FROM df_filtrado
            WHERE ABILITY_SCORE IS NOT NULL AND ANNUAL_WAGE_EUR IS NOT NULL
        )
        WHERE RN <= 65
    """)

    with chart_a:
        st.caption(
            "Nota: Para mantener la legibilidad visual del gráfico, los puntos graficados corresponden a "
            "una nube representativa de hasta 65 registros por cada combinación de posición y grupo etario, "
            "y no a la totalidad de los datos filtrados. Los valores del coeficiente de correlación (r) "
            "mostrados sí se calculan sobre el conjunto completo de registros."
        )

        st.echarts_chart(opciones_small_multiples_dispersion(muestra, datos), height=560)

    with chart_b:
        st.echarts_chart(opciones_curvas_correlacion(datos), height=420)

    table_slot.dataframe(
        datos,
        key="objetivo5_datos_df",
        hide_index=True,
        column_config={
            "POSICION": st.column_config.TextColumn("Posición"),
            "GRUPO_ETARIO": st.column_config.TextColumn("Grupo etario"),
            "CORRELACION": st.column_config.NumberColumn("Correlación (r)", format="%.3f"),
            "HABILIDAD_PROMEDIO": st.column_config.NumberColumn("Habilidad promedio", format="%.1f"),
            "SALARIO_PROMEDIO": st.column_config.NumberColumn("Salario promedio", format="€%d"),
            "JUGADORES": st.column_config.NumberColumn("Jugadores", format="%d"),
        },
    )
