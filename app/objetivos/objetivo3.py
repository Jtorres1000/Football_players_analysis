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


def opciones_grafico(datos):
    grupos_orden = ["15-21", "22-26", "27-31", "32-38"]
    grupos = [g for g in grupos_orden if g in datos["GRUPO_ETARIO"].values] or sorted(datos["GRUPO_ETARIO"].unique())

    posiciones_orden = [
        "Delanteros (ATT)",
        "Centrocampistas (MID)",
        "Defensas (DEF)",
        "Porteros (GK)",
    ]
    posiciones = [p for p in posiciones_orden if p in datos["POSICION"].values] or sorted(datos["POSICION"].unique())

    series = []
    for p in posiciones:
        color = COLORES_POSICION.get(p, "#04f5ff")
        filas_p = datos[datos["POSICION"] == p]

        valores = []
        for g in grupos:
            sub = filas_p[filas_p["GRUPO_ETARIO"] == g]
            if not sub.empty and sub["JUGADORES"].sum() > 0:
                sal = round((sub["SALARIO_PROMEDIO"] * sub["JUGADORES"]).sum() / sub["JUGADORES"].sum())
                valores.append(sal)
            else:
                valores.append(None)

        series.append({
            "name": p,
            "type": "line",
            "smooth": True,
            "symbol": "circle",
            "symbolSize": 8,
            "emphasis": {
                "focus": "series",
            },
            "lineStyle": {
                "width": 3.5,
                "color": color,
            },
            "itemStyle": {
                "color": color,
            },
            "markPoint": {
                "data": [{"type": "max", "name": "Pico"}],
                "itemStyle": {"color": color},
                "label": {
                    "color": "#27042a",
                    "fontWeight": "bold",
                    "fontSize": 10,
                    "formatter": "Tope",
                },
            },
            "data": valores,
        })

    return {
        "backgroundColor": "transparent",
        "title": {
            "text": "Ciclo de Vida Salarial por Posición de Juego",
            "textStyle": {"color": "#fbfaff", "fontSize": 14, "fontWeight": 600},
            "left": "center",
            "top": 0,
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross",
                "label": {
                    "backgroundColor": "#28042a",
                    "color": "#04f5ff",
                },
            },
            "backgroundColor": "rgba(22, 1, 24, 0.95)",
            "borderColor": "rgba(255, 255, 255, 0.15)",
            "textStyle": {"color": "#fbfaff", "fontSize": 12},
        },
        "legend": {
            "top": 28,
            "data": posiciones,
            "textStyle": {"color": "#c6b5cb", "fontSize": 11},
        },
        "toolbox": {
            "show": True,
            "feature": {
                "restore": {"title": "Reiniciar"},
                "saveAsImage": {"title": "Guardar imagen"},
            },
            "iconStyle": {"borderColor": "#c6b5cb"},
            "top": 20,
            "right": "4%",
        },
        "grid": {
            "top": 100,
            "left": "6%",
            "right": "6%",
            "bottom": 40,
            "containLabel": True,
        },
        "xAxis": {
            "type": "category",
            "data": grupos,
            "name": "Grupo etario",
            "boundaryGap": False,
            "axisLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.2)"}},
            "axisLabel": {"color": "#c6b5cb", "fontSize": 11},
            "splitLine": {"show": True, "lineStyle": {"color": "rgba(255, 255, 255, 0.05)"}},
        },
        "yAxis": {
            "type": "value",
            "name": "Salario anual promedio (€)",
            "scale": True,
            "axisLine": {"show": True, "lineStyle": {"color": "#04f5ff"}},
            "axisLabel": {
                "color": "#04f5ff",
                "formatter": "€{value}",
            },
            "splitLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.05)"}},
        },
        "series": series,
    }


def tarjetas(slot, datos):
    temporadas = sorted(datos["TEMPORADA"].unique()) if "TEMPORADA" in datos.columns else []
    if len(temporadas) < 2:
        return

    grupos_orden = ["15-21", "22-26", "27-31", "32-38"]
    grupos = [g for g in grupos_orden if g in datos["GRUPO_ETARIO"].values] or sorted(datos["GRUPO_ETARIO"].unique())

    tarjetas_info = []
    for g in grupos:
        sub_g = datos[datos["GRUPO_ETARIO"] == g]
        temps_g = sorted(sub_g["TEMPORADA"].unique())
        if len(temps_g) < 2:
            continue

        t_ini = temps_g[0]
        t_fin = temps_g[-1]

        sub_ini = sub_g[sub_g["TEMPORADA"] == t_ini]
        sub_fin = sub_g[sub_g["TEMPORADA"] == t_fin]

        if sub_ini["JUGADORES"].sum() == 0 or sub_fin["JUGADORES"].sum() == 0:
            continue

        sal_ini = round((sub_ini["SALARIO_PROMEDIO"] * sub_ini["JUGADORES"]).sum() / sub_ini["JUGADORES"].sum())
        sal_fin = round((sub_fin["SALARIO_PROMEDIO"] * sub_fin["JUGADORES"]).sum() / sub_fin["JUGADORES"].sum())
        diff = sal_fin - sal_ini
        pct = (diff / sal_ini) * 100 if sal_ini > 0 else 0
        signo = "+" if diff > 0 else ""
        delta_str = f"{signo}{formatear_eur(diff)} ({pct:+.1f}%)"

        tarjetas_info.append((g, t_ini, t_fin, sal_fin, delta_str))

    if not tarjetas_info:
        return

    columnas = slot.columns(len(tarjetas_info))
    for col, (g, t_ini, t_fin, sal_fin, delta_str) in zip(columnas, tarjetas_info):
        col.metric(
            label=f"Grupo {g} · {t_fin}",
            value=formatear_eur(sal_fin),
            delta=delta_str,
            help=f"Cambio entre {t_ini} y {t_fin}",
            border=True,
        )


def interpretar(datos):
    if datos.empty:
        return "No hay suficientes datos para interpretar este objetivo."

    sal_grupo = (
        datos.groupby("GRUPO_ETARIO")
        .apply(lambda g: (g["SALARIO_PROMEDIO"] * g["JUGADORES"]).sum() / g["JUGADORES"].sum())
    )
    sal_pos = (
        datos.groupby("POSICION")
        .apply(lambda g: (g["SALARIO_PROMEDIO"] * g["JUGADORES"]).sum() / g["JUGADORES"].sum())
    )

    pico_grupo = sal_grupo.idxmax()
    menor_grupo = sal_grupo.idxmin()
    mejor_pos = sal_pos.idxmax()
    peor_pos = sal_pos.idxmin()

    texto = (
        f"De forma general, la estructura salarial en el fútbol profesional presenta una marcada disparidad tanto "
        f"por etapa etaria como por rol táctico en el campo. A lo largo del ciclo de vida, las remuneraciones promedio "
        f"experimentan un crecimiento sostenido desde el grupo de menor compensación ({menor_grupo}, con una media de "
        f"{formatear_eur(sal_grupo[menor_grupo])}) hasta alcanzar el **pico salarial en el grupo de {pico_grupo} años** "
        f"({formatear_eur(sal_grupo[pico_grupo])}). En el segmento de veteranos (32 a 38 años), los ingresos promedio "
        f"se mantienen en niveles altos debido al **sesgo de supervivencia**, ya que en esta fase de la carrera únicamente "
        f"permanecen activos aquellos futbolistas consagrados que sostienen contratos de alta jerarquía. "
    )

    if len(sal_pos) > 1:
        texto += (
            f"Por posición en el campo, **{mejor_pos}** registra las compensaciones salariales más altas del mercado "
            f"({formatear_eur(sal_pos[mejor_pos])}), mientras que **{peor_pos}** percibe las remuneraciones promedio más moderadas "
            f"({formatear_eur(sal_pos[peor_pos])}). "
        )

    texto += (
        "El gráfico de curvas evidencia con claridad la interacción de estas dimensiones: las posiciones de ataque y creación "
        "alcanzan remuneraciones estelares en el tramo de madurez competitiva (27-31 años), mientras que las posiciones defensivas "
        "y de portería presentan curvas más contenidas y con una menor dispersión salarial a lo largo de todas las etapas etarias."
    )

    return texto


def objetivo3():
    st.subheader("Objetivo 3: Salario anual promedio según grupo etario y posición de juego, periodo 2022-2026")

    chart_slot = st.container()

    st.subheader("Interpretación")
    metricas_slot = st.container()
    texto_slot = st.container()

    st.subheader("Datos utilizados")
    st.markdown(
        "Empleamos el modelo dimensional uniendo la tabla de hechos `FACT_PLAYER_SEASON` con las dimensiones "
        "`DIM_SEASON`, `DIM_AGE_BRACKET` y `DIM_PLAYER`. Cada fila representa el salario anual promedio y conteo de jugadores "
        "para una posición, grupo etario y temporada según los filtros aplicados en la barra lateral."
    )
    table_slot = st.container()

    datos = query_filtered_data("""
        SELECT
            SEASON_LABEL AS TEMPORADA,
            CASE PRIMARY_CATEGORY
                WHEN 'ATTACKER' THEN 'Delanteros (ATT)'
                WHEN 'MIDFIELDER' THEN 'Centrocampistas (MID)'
                WHEN 'DEFENDER' THEN 'Defensas (DEF)'
                WHEN 'GOALKEEPER' THEN 'Porteros (GK)'
                ELSE PRIMARY_CATEGORY
            END AS POSICION,
            AGE_GROUP AS GRUPO_ETARIO,
            ROUND(AVG(ANNUAL_WAGE_EUR), 0) AS SALARIO_PROMEDIO,
            COUNT(*) AS JUGADORES
        FROM df_filtrado
        WHERE ANNUAL_WAGE_EUR IS NOT NULL
        GROUP BY SEASON_LABEL, PRIMARY_CATEGORY, AGE_GROUP
        ORDER BY TEMPORADA, POSICION, GRUPO_ETARIO
    """)

    if datos.empty:
        chart_slot.info(
            "No se encontraron registros para la combinación de filtros seleccionada en la barra lateral."
        )
        return

    with chart_slot:
        st.echarts_chart(opciones_grafico(datos), height=600)

    tarjetas(metricas_slot, datos)
    texto_slot.markdown(interpretar(datos))

    table_slot.dataframe(
        datos,
        key="objetivo3_datos_df",
        hide_index=True,
        column_config={
            "TEMPORADA": st.column_config.TextColumn("Temporada"),
            "POSICION": st.column_config.TextColumn("Posición"),
            "GRUPO_ETARIO": st.column_config.TextColumn("Grupo etario"),
            "SALARIO_PROMEDIO": st.column_config.NumberColumn("Salario promedio", format="€%d"),
            "JUGADORES": st.column_config.NumberColumn("Jugadores", format="%d"),
        },
    )
