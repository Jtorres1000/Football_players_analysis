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
            "text": "Small Multiples: Evolución de Habilidad vs. Salario por Posición",
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
            "text": "Mixed Line and Bar: Pico Salarial vs. Pico de Habilidad por Posición",
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
        return "No hay suficientes datos para interpretar este objetivo."

    return (
        "Al examinar la evolución conjunta a través de los cuatro grupos de edad, se puede apreciar el progreso en el rendimiento y la compensación: "
        "en el grupo de 15-21 años, se establece la base de formación con una habilidad media de 375.2 puntos y un salario inicial de €1.04M; "
        "en el rango de edad de 22-26 años, se produce una consolidación deportiva, alcanzando 399.4 puntos y aumentando el ingreso medio a €1.16M; "
        "en la etapa de 27-31 años, se consolida la madurez competitiva y contractual con 445.4 puntos de rendimiento medio y una remuneración de €1.79M; "
        "por último, en el rango de 32-38 años, los registros llegan a 461.9 puntos de habilidad y €2.41M de salario anual, debido a un sesgo de supervivencia, "
        "ya que a esta edad, pues a esta edad solo continúan activos los jugadores de fútbol con más jerarquía y con contratos más altos. "
        "Cuando se comparan los picos por posición, se observa que todos alcanzan su puntaje máximo de habilidad y su salario más alto en el rango de 32 a 38 años, "
        "siendo los Centrocampistas (MID) los que sobresalen en habilidad (470.8 pts) y también en remuneración (€2.56M)."
    )


def objetivo4():
    st.subheader("Objetivo 4: Relación entre edad de máximo rendimiento y pico salarial por posición, periodo 2022-2026")

    st.markdown("**a) Relación entre habilidad promedio y salario anual por posición y grupo etario**")
    chart_a = st.container()

    st.markdown("**b) Comparativa de picos máximos de habilidad y salario anual por posición**")
    chart_b = st.container()

    st.subheader("Interpretación")
    texto_slot = st.container()

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

    with chart_a:
        st.echarts_chart(opciones_small_multiples(datos), height=540)

    with chart_b:
        st.echarts_chart(opciones_picos_comparados(picos), height=440)

    texto_slot.markdown(interpretar(datos, picos))

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
