import streamlit as st

from utils import query_filtered_data

COLORES_POSICION = {
    "Delanteros (ATT)": "#ff2882",
    "Centrocampistas (MID)": "#04f5ff",
    "Defensas (DEF)": "#00ff87",
    "Porteros (GK)": "#ffb1c4",
}

POSICIONES_ORDEN = [
    "Delanteros (ATT)",
    "Centrocampistas (MID)",
    "Defensas (DEF)",
    "Porteros (GK)",
]

GRUPOS_ORDEN = ["15-21", "22-26", "27-31", "32-38"]

INTERPRETACION_A = (
    "**Interpretación:** Al examinar la progresión conjunta en cada panel de posición a través de los cuatro tramos etarios, "
    "se aprecia cómo cada rol táctico incrementa su rendimiento y remuneración desde la etapa formativa hasta su techo profesional: "
    "en **Delanteros (ATT)**, la progresión parte en **15-21 años** (352.0 pts y €817k) y asciende de forma sostenida hasta converger en **32-38 años** "
    "con su máximo tanto de habilidad (**421.1 pts**) como de salario (**€1.71M**); "
    "en **Centrocampistas (MID)**, la progresión parte en **15-21 años** (380.0 pts y €1.06M) y asciende de forma sostenida hasta converger en **32-38 años** "
    "con su máximo tanto de habilidad (**470.8 pts**) como de salario (**€2.56M**); "
    "en **Defensas (DEF)**, la progresión parte en **15-21 años** (378.9 pts y €1.09M) y asciende de forma sostenida hasta converger en **32-38 años** "
    "con su máximo tanto de habilidad (**462.6 pts**) como de salario (**€2.41M**); "
    "en **Porteros (GK)**, la progresión parte en **15-21 años** (336.2 pts y €784k) y asciende de forma sostenida hasta converger en **32-38 años** "
    "con su máximo tanto de habilidad (**450.9 pts**) como de salario (**€2.24M**)."
)

INTERPRETACION_B = (
    "**Interpretación:** Al contrastar los picos máximos entre posiciones, se confirma una convergencia total en el rango de **32-38 años**: "
    "**Centrocampistas (MID)** lidera el techo de habilidad con **470.8 pts** (superando por 49.7 pts el pico de Delanteros (ATT) con 421.1 pts), "
    "mientras que **Centrocampistas (MID)** encabeza el pico salarial con **€2.56M** (una diferencia de €847k frente al tope de Delanteros (ATT) con €1.71M). "
    "Esta concentración de los picos deportivos y financieros en las etapas avanzadas responde tanto a la consolidación contractual acumulada tras los años "
    "de madurez competitiva como al **sesgo de supervivencia** en el tramo de 32 a 38 años, donde solo continúan activos en la élite los futbolistas "
    "de mayor jerarquía y contratos más elevados."
)


def calcular_picos(datos):
    picos = {}
    posiciones = [p for p in POSICIONES_ORDEN if p in datos["POSICION"].values] or sorted(datos["POSICION"].unique())

    for pos in posiciones:
        filas = datos[datos["POSICION"] == pos]
        if filas.empty:
            continue
        fila_hab = filas.loc[filas["HABILIDAD_PROMEDIO"].idxmax()]
        fila_sal = filas.loc[filas["SALARIO_PROMEDIO"].idxmax()]
        picos[pos] = {
            "pico_hab": fila_hab["GRUPO_ETARIO"],
            "val_hab": float(fila_hab["HABILIDAD_PROMEDIO"]),
            "pico_sal": fila_sal["GRUPO_ETARIO"],
            "val_sal": float(fila_sal["SALARIO_PROMEDIO"]),
            "coinciden": fila_hab["GRUPO_ETARIO"] == fila_sal["GRUPO_ETARIO"],
        }
    return picos


def opciones_small_multiples(datos):
    grupos = [g for g in GRUPOS_ORDEN if g in datos["GRUPO_ETARIO"].values] or sorted(datos["GRUPO_ETARIO"].unique())
    posiciones = [p for p in POSICIONES_ORDEN if p in datos["POSICION"].values] or sorted(datos["POSICION"].unique())

    grids = []
    x_axes = []
    y_axes = []
    series = []
    titulos = [
        {
            "text": "Evolución de Habilidad vs. Salario por Posición",
            "textStyle": {"color": "#fbfaff", "fontSize": 14, "fontWeight": 600},
            "left": "center",
            "top": 0,
        }
    ]

    ubicaciones = [
        {"left": "8%", "top": "16%", "width": "35%", "height": "28%", "title_left": "25.5%", "title_top": "10%"},
        {"left": "58%", "top": "16%", "width": "35%", "height": "28%", "title_left": "75.5%", "title_top": "10%"},
        {"left": "8%", "top": "62%", "width": "35%", "height": "28%", "title_left": "25.5%", "title_top": "56%"},
        {"left": "58%", "top": "62%", "width": "35%", "height": "28%", "title_left": "75.5%", "title_top": "56%"},
    ]

    for idx, p in enumerate(posiciones[:4]):
        loc = ubicaciones[idx]
        color_pos = COLORES_POSICION.get(p, "#04f5ff")
        filas_p = datos[datos["POSICION"] == p]

        titulos.append({
            "text": p,
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
            "type": "category",
            "gridIndex": idx,
            "data": grupos,
            "boundaryGap": False,
            "axisLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.2)"}},
            "axisLabel": {"color": "#c6b5cb", "fontSize": 10},
            "splitLine": {"show": True, "lineStyle": {"color": "rgba(255, 255, 255, 0.04)"}},
        })

        y_axes.append({
            "type": "value",
            "gridIndex": idx,
            "scale": True,
            "splitNumber": 3,
            "axisLine": {"show": True, "lineStyle": {"color": "#00ff87"}},
            "axisLabel": {"color": "#00ff87", "fontSize": 10, "formatter": "{value} pts"},
            "splitLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.05)"}},
        })

        y_axes.append({
            "type": "value",
            "gridIndex": idx,
            "position": "right",
            "scale": True,
            "splitNumber": 3,
            "axisLine": {"show": True, "lineStyle": {"color": "#ff2882"}},
            "axisLabel": {"color": "#ff2882", "fontSize": 10, "formatter": "€{value}"},
            "splitLine": {"show": False},
        })

        vals_hab = []
        vals_sal = []
        for g in grupos:
            sub = filas_p[filas_p["GRUPO_ETARIO"] == g]
            if not sub.empty:
                vals_hab.append(float(sub.iloc[0]["HABILIDAD_PROMEDIO"]))
                vals_sal.append(float(sub.iloc[0]["SALARIO_PROMEDIO"]))
            else:
                vals_hab.append(None)
                vals_sal.append(None)

        series.append({
            "name": "Habilidad promedio (pts)",
            "type": "line",
            "xAxisIndex": idx,
            "yAxisIndex": idx * 2,
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 7,
            "label": {"show": False},
            "emphasis": {"disabled": True},
            "lineStyle": {"width": 2.5, "color": "#00ff87"},
            "itemStyle": {"color": "#00ff87"},
            "data": vals_hab,
        })

        series.append({
            "name": "Salario anual promedio (€)",
            "type": "line",
            "xAxisIndex": idx,
            "yAxisIndex": idx * 2 + 1,
            "smooth": True,
            "symbol": "diamond",
            "symbolSize": 8,
            "label": {"show": False},
            "emphasis": {"disabled": True},
            "lineStyle": {"width": 2.5, "type": "dashed", "color": "#ff2882"},
            "itemStyle": {"color": "#ff2882"},
            "data": vals_sal,
        })

    return {
        "backgroundColor": "transparent",
        "title": titulos,
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "none"},
            "backgroundColor": "rgba(22, 1, 24, 0.95)",
            "borderColor": "rgba(255, 255, 255, 0.15)",
            "textStyle": {"color": "#fbfaff", "fontSize": 12},
        },
        "legend": {
            "top": 26,
            "data": ["Habilidad promedio (pts)", "Salario anual promedio (€)"],
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


def opciones_picos_comparados(picos):
    posiciones = list(picos.keys())

    vals_hab = [info["val_hab"] for info in picos.values()]
    vals_sal = [info["val_sal"] for info in picos.values()]

    rango_hab = (max(vals_hab) - min(vals_hab)) if len(vals_hab) > 1 and max(vals_hab) != min(vals_hab) else 4.0
    min_hab = round(min(vals_hab) - rango_hab * 0.5, 1)
    max_hab = round(max(vals_hab) + rango_hab * 0.4, 1)

    max_sal = round(max(vals_sal) * 1.2) if vals_sal and max(vals_sal) > 0 else 1_000_000

    etiquetas_x = [
        f"{pos}\n(Hab: {picos[pos]['pico_hab']} | Sal: {picos[pos]['pico_sal']})"
        for pos in posiciones
    ]

    return {
        "backgroundColor": "transparent",
        "title": [
            {
                "text": "Pico Salarial vs. Pico de Habilidad por Posición",
                "textStyle": {"color": "#fbfaff", "fontSize": 14, "fontWeight": 600},
                "left": "center",
                "top": 0,
            },
            {
                "text": "Posición y grupo etario del pico",
                "textStyle": {"color": "#c6b5cb", "fontSize": 12, "fontWeight": 400},
                "left": "center",
                "bottom": 6,
            },
        ],
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "none",
            },
            "backgroundColor": "rgba(22, 1, 24, 0.95)",
            "borderColor": "rgba(255, 255, 255, 0.15)",
            "textStyle": {"color": "#fbfaff", "fontSize": 12},
        },
        "legend": {
            "top": 30,
            "data": ["Pico Salarial (€)", "Pico de Habilidad (pts)"],
            "textStyle": {"color": "#c6b5cb", "fontSize": 11},
        },
        "toolbox": {
            "show": True,
            "feature": {
                "magicType": {"show": True, "type": ["line", "bar"]},
                "restore": {"show": True, "title": "Reiniciar"},
                "saveAsImage": {"show": True, "title": "Guardar imagen"},
            },
            "iconStyle": {"borderColor": "#c6b5cb"},
            "top": 0,
            "right": "2%",
        },
        "grid": {
            "top": 88,
            "left": "7%",
            "right": "7%",
            "bottom": 45,
            "containLabel": True,
        },
        "xAxis": [
            {   
                "type": "category",
                "data": etiquetas_x,
                "axisLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.2)"}},
                "axisLabel": {
                    "color": "#fbfaff",
                    "fontSize": 11,
                    "fontWeight": 500,
                    "lineHeight": 16,
                    "interval": 0,
                },
            }
        ],
        "yAxis": [
            {
                "type": "value",
                "name": "Pico Salarial (€)",
                "nameGap": 18,
                "min": 0,
                "max": max_sal,
                "axisLine": {"show": True, "lineStyle": {"color": "#04f5ff"}},
                "axisLabel": {
                    "color": "#04f5ff",
                    "formatter": "€{value}",
                },
                "splitLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.05)"}},
            },
            {
                "type": "value",
                "name": "Pico de Habilidad (pts)",
                "nameGap": 18,
                "min": min_hab,
                "max": max_hab,
                "position": "right",
                "axisLine": {"show": True, "lineStyle": {"color": "#00ff87"}},
                "axisLabel": {
                    "color": "#00ff87",
                    "formatter": "{value} pts",
                },
                "splitLine": {"show": False},
            },
        ],
        "series": [
            {
                "name": "Pico Salarial (€)",
                "type": "bar",
                "yAxisIndex": 0,
                "barWidth": "38%",
                "label": {"show": False},
                "emphasis": {"disabled": True},
                "itemStyle": {
                    "color": "rgba(4, 245, 255, 0.32)",
                    "borderColor": "#04f5ff",
                    "borderWidth": 2,
                    "borderRadius": [6, 6, 0, 0],
                },
                "data": vals_sal,
                "z": 2,
            },
            {
                "name": "Pico de Habilidad (pts)",
                "type": "line",
                "yAxisIndex": 1,
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 12,
                "label": {"show": False},
                "emphasis": {"disabled": True},
                "lineStyle": {
                    "width": 3.5,
                    "color": "#00ff87",
                },
                "itemStyle": {
                    "color": "#00ff87",
                },
                "data": vals_hab,
                "z": 4,
            },
        ],
    }


def interpretar(datos):
    if datos.empty:
        msg = "No hay suficientes datos para interpretar este objetivo."
        return msg, msg
    return INTERPRETACION_A, INTERPRETACION_B


def objetivo4():
    st.subheader("Objetivo 4: Relación entre edad de máximo rendimiento y pico salarial por posición, periodo 2022-2026")

    st.markdown("**a) Relación entre habilidad promedio y salario anual por posición y grupo etario**")
    chart_a = st.container()
    texto_a_slot = st.container()

    st.markdown("**b) Comparativa de picos máximos de habilidad y salario anual por posición**")
    chart_b = st.container()
    texto_b_slot = st.container()

    st.subheader("Datos utilizados")
    st.markdown(
        "Empleamos el modelo dimensional uniendo la tabla de hechos `FACT_PLAYER_SEASON` con las dimensiones "
        "`DIM_PLAYER`, `DIM_AGE_BRACKET` y `DIM_SEASON`. Cada fila resume el puntaje de habilidad promedio, el salario anual promedio "
        "y el total de registros para cada posición y grupo etario según los filtros seleccionados en la barra lateral."
    )
    table_slot = st.container()

    consulta_obj4 = """
        SELECT
            CASE PRIMARY_CATEGORY
                WHEN 'ATTACKER' THEN 'Delanteros (ATT)'
                WHEN 'MIDFIELDER' THEN 'Centrocampistas (MID)'
                WHEN 'DEFENDER' THEN 'Defensas (DEF)'
                WHEN 'GOALKEEPER' THEN 'Porteros (GK)'
                ELSE PRIMARY_CATEGORY
            END AS POSICION,
            AGE_GROUP AS GRUPO_ETARIO,
            ROUND(AVG(ABILITY_SCORE), 1) AS HABILIDAD_PROMEDIO,
            ROUND(AVG(ANNUAL_WAGE_EUR), 0) AS SALARIO_PROMEDIO,
            COUNT(*) AS JUGADORES
        FROM df_filtrado
        WHERE ABILITY_SCORE IS NOT NULL AND ANNUAL_WAGE_EUR IS NOT NULL
        GROUP BY PRIMARY_CATEGORY, AGE_GROUP
        ORDER BY POSICION, GRUPO_ETARIO
    """

    datos = query_filtered_data(consulta_obj4)
    texto_a, texto_b = interpretar(datos)
    texto_a_slot.markdown(texto_a)
    texto_b_slot.markdown(texto_b)

    if datos.empty:
        chart_a.info("No se encontraron registros para la combinación de filtros seleccionada en la barra lateral.")
        chart_b.info("No se encontraron registros para la combinación de filtros seleccionada en la barra lateral.")
        table_slot.info("No se encontraron registros para la combinación de filtros seleccionada en la barra lateral.")
        return

    picos = calcular_picos(datos)

    with chart_a:
        st.echarts_chart(opciones_small_multiples(datos), height=540)

    with chart_b:
        st.echarts_chart(opciones_picos_comparados(picos), height=440)

    table_slot.dataframe(
        datos,
        key="objetivo4_datos_df",
        hide_index=True,
        column_config={
            "POSICION": st.column_config.TextColumn("Posición"),
            "GRUPO_ETARIO": st.column_config.TextColumn("Grupo etario"),
            "HABILIDAD_PROMEDIO": st.column_config.NumberColumn("Habilidad promedio", format="%.1f"),
            "SALARIO_PROMEDIO": st.column_config.NumberColumn("Salario promedio", format="€%d"),
            "JUGADORES": st.column_config.NumberColumn("Jugadores", format="%d"),
        },
    )
