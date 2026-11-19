import streamlit as st
import pandas as pd

from utils import query_filtered_data

COLORES_POSICION = {
    "Delanteros (ATT)": "#ff2882",
    "Centrocampistas (MID)": "#04f5ff",
    "Defensas (DEF)": "#00ff87",
    "Porteros (GK)": "#ffb1c4",
}


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


def calcular_picos(datos):
    picos = {}
    posiciones_orden = [
        "Delanteros (ATT)",
        "Centrocampistas (MID)",
        "Defensas (DEF)",
        "Porteros (GK)",
    ]
    posiciones = [p for p in posiciones_orden if p in datos["POSICION"].values] or sorted(datos["POSICION"].unique())

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
    grupos_orden = ["15-21", "22-26", "27-31", "32-38"]
    grupos = [g for g in grupos_orden if g in datos["GRUPO_ETARIO"].values] or sorted(datos["GRUPO_ETARIO"].unique())

    posiciones_orden = [
        "Delanteros (ATT)",
        "Centrocampistas (MID)",
        "Defensas (DEF)",
        "Porteros (GK)",
    ]
    posiciones = [p for p in posiciones_orden if p in datos["POSICION"].values] or sorted(datos["POSICION"].unique())

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
        "title": {
            "text": "Pico Salarial vs. Pico de Habilidad por Posición",
            "textStyle": {"color": "#fbfaff", "fontSize": 14, "fontWeight": 600},
            "left": "center",
            "top": 0,
        },
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
            "bottom": 55,
            "containLabel": True,
        },
        "xAxis": [
            {
                "type": "category",
                "data": etiquetas_x,
                "name": "Posición y grupo etario del pico",
                "nameLocation": "middle",
                "nameGap": 42,
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


def interpretar(datos, picos):
    if datos.empty or not picos:
        msg = "No hay suficientes datos para interpretar este objetivo."
        return msg, msg

    posiciones_orden = [
        "Delanteros (ATT)",
        "Centrocampistas (MID)",
        "Defensas (DEF)",
        "Porteros (GK)",
    ]
    grupos_orden = ["15-21", "22-26", "27-31", "32-38"]

    trayectorias_pos = []
    for pos in posiciones_orden:
        if pos not in picos:
            continue
        filas_p = datos[datos["POSICION"] == pos].set_index("GRUPO_ETARIO")
        grupos_disp = [g for g in grupos_orden if g in filas_p.index]
        if not grupos_disp:
            continue

        g_ini = grupos_disp[0]
        hab_ini = float(filas_p.loc[g_ini, "HABILIDAD_PROMEDIO"])
        sal_ini = float(filas_p.loc[g_ini, "SALARIO_PROMEDIO"])

        info = picos[pos]
        if info["coinciden"]:
            trayectorias_pos.append(
                f"en **{pos}**, la progresión parte en **{g_ini} años** ({hab_ini} pts y {formatear_eur(sal_ini)}) "
                f"y asciende de forma sostenida hasta converger en **{info['pico_hab']} años** con su máximo tanto de habilidad "
                f"(**{info['val_hab']} pts**) como de salario (**{formatear_eur(info['val_sal'])}**)"
            )
        else:
            trayectorias_pos.append(
                f"en **{pos}**, la curva inicia en **{g_ini} años** ({hab_ini} pts y {formatear_eur(sal_ini)}), "
                f"alcanza su tope deportivo en **{info['pico_hab']} años** (**{info['val_hab']} pts**) "
                f"y registra su techo salarial en **{info['pico_sal']} años** (**{formatear_eur(info['val_sal'])}**)"
            )

    coincidentes = [pos for pos, info in picos.items() if info["coinciden"]]
    desfasadas = [pos for pos, info in picos.items() if not info["coinciden"]]

    mejor_hab_pos = max(picos.items(), key=lambda x: x[1]["val_hab"])
    menor_hab_pos = min(picos.items(), key=lambda x: x[1]["val_hab"])
    mejor_sal_pos = max(picos.items(), key=lambda x: x[1]["val_sal"])
    menor_sal_pos = min(picos.items(), key=lambda x: x[1]["val_sal"])

    brecha_hab = round(mejor_hab_pos[1]["val_hab"] - menor_hab_pos[1]["val_hab"], 1)
    brecha_sal = mejor_sal_pos[1]["val_sal"] - menor_sal_pos[1]["val_sal"]

    if len(coincidentes) == len(picos):
        comparativa_picos = (
            f"Al contrastar los picos máximos entre posiciones, se confirma una convergencia total en el rango de "
            f"**{mejor_hab_pos[1]['pico_hab']} años**: **{mejor_hab_pos[0]}** lidera el techo de habilidad con **{mejor_hab_pos[1]['val_hab']} pts** "
            f"(superando por {brecha_hab} pts el pico de {menor_hab_pos[0]} con {menor_hab_pos[1]['val_hab']} pts), mientras que "
            f"**{mejor_sal_pos[0]}** encabeza el pico salarial con **{formatear_eur(mejor_sal_pos[1]['val_sal'])}** "
            f"(una diferencia de {formatear_eur(brecha_sal)} frente al tope de {menor_sal_pos[0]} con {formatear_eur(menor_sal_pos[1]['val_sal'])}). "
        )
    elif len(desfasadas) == len(picos):
        comparativa_picos = (
            f"Al contrastar los picos máximos entre posiciones, se observa un desfase generalizado entre el mejor momento "
            f"deportivo y el mayor ingreso: **{mejor_hab_pos[0]}** alcanza el mayor pico de habilidad con **{mejor_hab_pos[1]['val_hab']} pts** "
            f"en **{mejor_hab_pos[1]['pico_hab']} años** ({brecha_hab} pts por encima del tope de {menor_hab_pos[0]}), en tanto que "
            f"**{mejor_sal_pos[0]}** registra el pico salarial más alto con **{formatear_eur(mejor_sal_pos[1]['val_sal'])}** en "
            f"**{mejor_sal_pos[1]['pico_sal']} años** ({formatear_eur(brecha_sal)} por encima del techo de {menor_sal_pos[0]}). "
        )
    else:
        comparativa_picos = (
            f"Al contrastar los picos máximos entre posiciones, ambos momentos coinciden en {', '.join(coincidentes)} "
            f"y presentan desfase etario en {', '.join(desfasadas)}: a nivel absoluto, **{mejor_hab_pos[0]}** marca la cima de habilidad "
            f"con **{mejor_hab_pos[1]['val_hab']} pts** en **{mejor_hab_pos[1]['pico_hab']} años** (superando por {brecha_hab} pts a {menor_hab_pos[0]}), "
            f"mientras que **{mejor_sal_pos[0]}** lidera el techo salarial con **{formatear_eur(mejor_sal_pos[1]['val_sal'])}** en "
            f"**{mejor_sal_pos[1]['pico_sal']} años** ({formatear_eur(brecha_sal)} más que el tope de {menor_sal_pos[0]}). "
        )

    texto_a = (
        "**Interpretación:** "
        "Al examinar la progresión conjunta en cada panel de posición a través de los cuatro tramos etarios, se aprecia cómo "
        "cada rol táctico incrementa su rendimiento y remuneración desde la etapa formativa hasta su techo profesional: "
        + "; ".join(trayectorias_pos)
        + "."
    )

    texto_b = (
        "**Interpretación:** "
        + comparativa_picos
        + "Esta concentración de los picos deportivos y financieros en las etapas avanzadas responde tanto a la consolidación contractual "
        "acumulada tras los años de madurez competitiva como al **sesgo de supervivencia** en el tramo de 32 a 38 años, donde solo "
        "continúan activos en la élite los futbolistas de mayor jerarquía y contratos más elevados."
    )

    return texto_a, texto_b


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

    datos = query_filtered_data("""
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
    """)

    if datos.empty:
        chart_a.info("No se encontraron registros para la combinación de filtros seleccionada en la barra lateral.")
        chart_b.info("No se encontraron registros para la combinación de filtros seleccionada en la barra lateral.")
        return

    picos = calcular_picos(datos)
    texto_a, texto_b = interpretar(datos, picos)

    with chart_a:
        st.echarts_chart(opciones_small_multiples(datos), height=540)
    texto_a_slot.markdown(texto_a)

    with chart_b:
        st.echarts_chart(opciones_picos_comparados(picos), height=440)
    texto_b_slot.markdown(texto_b)

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
