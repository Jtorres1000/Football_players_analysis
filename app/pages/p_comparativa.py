import streamlit as st

from components import banner

# Data estática para probar el funcionamiento del radar.

MOCK_RADAR_DATA = [
    {
        "name": "Nesto Groen",
        "primary_category": "ATTACKER",
        "sum(psa.goals)": 132,
        "sum(psa.dribbles_made)": 173,
        "sum(psd.tackles_completed)": 143,
        "avg(psg2.save_ratio)": 0.0,
        "sum(psa.chances_created)": 28,
        "sum(psp.passes_completed)": 3307,
    },
    {
        "name": "Malick Thiaw",
        "primary_category": "DEFENDER",
        "sum(psa.goals)": 4,
        "sum(psa.dribbles_made)": 102,
        "sum(psd.tackles_completed)": 273,
        "avg(psg2.save_ratio)": 0.0,
        "sum(psa.chances_created)": 8,
        "sum(psp.passes_completed)": 13471,
    },
    {
        "name": "Moisés Caicedo",
        "primary_category": "MIDFIELDER",
        "sum(psa.goals)": 16,
        "sum(psa.dribbles_made)": 203,
        "sum(psd.tackles_completed)": 430,
        "avg(psg2.save_ratio)": 0.0,
        "sum(psa.chances_created)": 55,
        "sum(psp.passes_completed)": 9392,
    },
    {
        "name": "Sergio Camacho",
        "primary_category": "GOALKEEPER",
        "sum(psa.goals)": 0,
        "sum(psa.dribbles_made)": 0,
        "sum(psd.tackles_completed)": 0,
        "avg(psg2.save_ratio)": 1.0,
        "sum(psa.chances_created)": 0,
        "sum(psp.passes_completed)": 130,
    },
    {
        "name": "Vinícius Júnior",
        "primary_category": "MIDFIELDER",
        "sum(psa.goals)": 82,
        "sum(psa.dribbles_made)": 727,
        "sum(psd.tackles_completed)": 424,
        "avg(psg2.save_ratio)": 0.0,
        "sum(psa.chances_created)": 151,
        "sum(psp.passes_completed)": 5562,
    },
]

# Métricas usadas para normalizar cada uno de los stats, nuevamente para probar la visualización.

METRICS = [
    ("sum(psa.goals)", "Goles", 0, 132),
    ("sum(psa.dribbles_made)", "Regates", 0, 727),
    ("sum(psd.tackles_completed)", "Entradas", 0, 689),
    ("avg(psg2.save_ratio)", "Ratio Paradas", 0, 1.0),
    ("sum(psa.chances_created)", "Ocasiones Creadas", 0, 213),
    ("sum(psp.passes_completed)", "Pases Completados", 50, 13471),
]

# Función para construir el json del gráfico de radar en formato ECharts.

def _build_radar_chart_option(p1_data: dict, p2_data: dict) -> dict:
    indicators = []
    p1_values = []
    p2_values = []

    for key, label, min_val, max_val in METRICS:
        indicators.append({
            "name": label,
            "text": label,
            "min": min_val,
            "max": max_val,
        })

        v1 = p1_data[key]
        v2 = p2_data[key]

        p1_values.append(round(v1, 2) if isinstance(v1, float) else v1)
        p2_values.append(round(v2, 2) if isinstance(v2, float) else v2)

    return {
        "backgroundColor": "rgba(29, 2, 32, 0.9)",
        "tooltip": {
            "trigger": "item",
            "backgroundColor": "rgba(22, 1, 24, 0.95)",
            "borderColor": "rgba(255, 255, 255, 0.15)",
            "borderWidth": 1,
            "textStyle": {
                "color": "#fbfaff",
                "fontFamily": "Plus Jakarta Sans, sans-serif",
                "fontSize": 12,
            },
        },
        "legend": {
            "show": True,
            "bottom": "3%",
            "left": "right",
            "icon": "circle",
            "itemGap": 24,
            "textStyle": {
                "color": "#fbfaff",
                "fontFamily": "Plus Jakarta Sans, sans-serif",
                "fontSize": 13,
            },
            "data": [p1_data["name"], p2_data["name"]],
        },
        "radar": {
            "shape": "polygon",
            "center": ["50%", "50%"],
            "radius": "80%",
            "splitNumber": 4,
            "axisName": {
                "color": "#fbfaff",
                "fontFamily": "Outfit, sans-serif",
                "fontSize": 12,
                "fontWeight": 600,
            },
            "splitArea": {
                "show": True,
                "areaStyle": {
                    "color": ["#160118", "#1c011e", "#160118", "#1c011e"],
                },
            },
            "axisLine": {
                "lineStyle": {
                    "color": "rgba(255, 255, 255, 0.15)",
                },
            },
            "splitLine": {
                "lineStyle": {
                    "color": "rgba(255, 255, 255, 0.12)",
                },
            },
            "indicator": indicators,
        },
        "series": [
            {
                "type": "radar",
                "emphasis": {
                    "lineStyle": {
                        "width": 4,
                    },
                },
                "data": [
                    {
                        "value": p1_values,
                        "name": p1_data["name"],
                        "symbol": "circle",
                        "symbolSize":6,
                        "lineStyle": {
                            "color": "#04f5ff",
                            "width": 3,
                        },
                        "itemStyle": {
                            "color": "#04f5ff",
                        },
                        "areaStyle": {
                            "color": "rgba(4, 245, 255, 0.25)",
                        },
                    },
                    {
                        "value": p2_values,
                        "name": p2_data["name"],
                        "symbol": "circle",
                        "symbolSize": 6,
                        "lineStyle": {
                            "color": "#e4006f",
                            "width": 3,
                        },
                        "itemStyle": {
                            "color": "#e4006f",
                        },
                        "areaStyle": {
                            "color": "rgba(228, 0, 111, 0.25)",
                        },
                    },
                ],
            }
        ],
    }

# Definición de la página de comparativa de jugadores.
def p_comparativa():
    # Banner de la página con título y subtitulo
    banner(
        title="Comparativa Radar de Rendimiento",
        subtitle="Análisis multidimensional de perfiles deportivos y preparación de datos para el Agente Coach.",
    )

    st.markdown(
        """
        ### Propósito del Módulo y Flujo de Trabajo

        Esta herramienta permite comparar perfiles de rendimiento entre dos futbolistas en seis dimensiones esenciales: goles, regates realizados, entradas completadas, ratio de paradas, ocasiones creadas y pases completados. Los ejes emplean una escala normalizada con topes referenciales fijos, garantizando que el perfil geométrico de cada jugador permanezca inmutable al contrastarlo frente a distintos rivales.

        **Pasos para el análisis:**
        1. **Inspección del Radar**: Observa la superposición de polígonos en la tarjeta visual. Al interactuar con cada vértice, el cursor revelará la estadística cuantitativa acumulada real.
        2. **Configuración de Candidatos**: En los selectores situados al pie del gráfico, elige a los dos futbolistas a confrontar para actualizar las dimensiones y etiquetas de rol.
        3. **Asignación del Club Objetivo**: Selecciona el equipo donde se proyecta la evaluación de los perfiles. Este paso es un requisito indispensable para activar la comunicación con el módulo de inteligencia.
        4. **Envío al Agente Coach**: Acciona el botón de envío para empaquetar los datos de los futbolistas y la plantilla del club en la estructura estandarizada que procesará el agente para el reporte final.
        """
    )

    # Extracción de la data de los jugadores escogidos para construir el gráfico.

    player_names = [p["name"] for p in MOCK_RADAR_DATA]

    p1_selected_name = st.session_state.get("comp_player_1", player_names[0])
    p2_selected_name = st.session_state.get("comp_player_2", player_names[1])

    p1_data = next((p for p in MOCK_RADAR_DATA if p["name"] == p1_selected_name), MOCK_RADAR_DATA[0])
    p2_data = next((p for p in MOCK_RADAR_DATA if p["name"] == p2_selected_name), MOCK_RADAR_DATA[1])

    cat1 = p1_data.get("primary_category", "NONE")
    cat2 = p2_data.get("primary_category", "NONE")

    card_header = f"""
    <div style="
        background: linear-gradient(135deg, #26042a 0%, #1d0220 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px 16px 0 0;
        padding: 20px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    ">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background: rgba(228, 0, 111, 0.15);
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid rgba(228, 0, 111, 0.4);
                flex-shrink: 0;
            ">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="9" stroke="#e4006f" stroke-width="2"/>
                    <circle cx="12" cy="12" r="5" stroke="#e4006f" stroke-width="2"/>
                    <circle cx="12" cy="12" r="2" fill="#e4006f"/>
                </svg>
            </div>
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 700; color: #fbfaff; line-height: 1.2;">
                    Radar Comparativo de Jugadores
                </div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #c6b5cb; margin-top: 3px;">
                    Comparando {p1_data['name']} vs {p2_data['name']}
                </div>
            </div>
        </div>
        <div style="
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 6px 14px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.03em;
            display: flex;
            align-items: center;
            white-space: nowrap;
        ">
            <span style="color: #04f5ff;">P1: {cat1}</span>
            <span style="color: rgba(255, 255, 255, 0.25); margin: 0 8px;">|</span>
            <span style="color: #e4006f;">P2: {cat2}</span>
        </div>
    </div>
    """

    # se contruye el gráfico de radar.
    st.markdown(card_header, unsafe_allow_html=True)
    chart_option = _build_radar_chart_option(p1_data, p2_data)

    try:
        st.echarts_chart(chart_option, height=480, use_container_width=True)
    except TypeError:
        try:
            st.echarts_chart(chart_option, height=480)
        except TypeError:
            st.echarts_chart(chart_option)

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox(
            "Jugador 1 (Candidato A)",
            options=player_names,
            index=0,
            key="comp_player_1",
        )

    with col2:
        st.selectbox(
            "Jugador 2 (Candidato B)",
            options=player_names,
            index=1 if len(player_names) > 1 else 0,
            key="comp_player_2",
        )

    selected_team = st.selectbox(
        "Seleccionar Equipo para la Comparativa",
        options=["Real Madrid", "FC Barcelona", "Manchester City", "Juventus", "Liverpool"],
        index=None,
        placeholder="Seleccione un equipo para habilitar el análisis del Coach...",
        key="comp_team",
    )

    send_coach_clicked = st.button(
        "Enviar al Agente Coach",
        type="primary",
        use_container_width=True,
        disabled=not bool(selected_team),
    )

    if send_coach_clicked:
        payload = {
            "target_team": selected_team,
            "candidates": [
                p1_data,
                p2_data,
            ],
            "current_team_roster_stats": [
                {
                    "name": "Jugador Referencia 1",
                    "position": "Delantero",
                    "goals": 18,
                    "assists": 7,
                },
                {
                    "name": "Jugador Referencia 2",
                    "position": "Centrocampista",
                    "goals": 5,
                    "assists": 14,
                },
            ],
        }

        st.success(
            "Payload generado y listo para enviar al Agente Coach."
        )
        with st.expander("Ver JSON que se enviará al Agente Coach"):
            st.json(payload)
