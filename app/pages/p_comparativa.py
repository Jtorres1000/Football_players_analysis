import pandas as pd
import streamlit as st

from components import banner
from utils import query_base_data

METRICS = [
    ("goals", "Goles"),
    ("dribbles_made", "Regates"),
    ("tackles_completed", "Entradas"),
    ("save_ratio", "Ratio Paradas"),
    ("chances_created", "Ocasiones Creadas"),
    ("passes_completed", "Pases Completados"),
]

POSITION_OPTIONS = ["Todas", "ATTACKER", "MIDFIELDER", "DEFENDER", "GOALKEEPER"]

STATS_SELECT_SQL = """
    SELECT
        NAME AS name,
        PRIMARY_CATEGORY AS primary_category,
        PRIMARY_ROLE_CODE AS primary_role_code,
        PRIMARY_SIDE_CODE AS primary_side_code,
        CAST(SUM(GOALS) AS INT) AS goals,
        CAST(SUM(DRIBBLES_MADE) AS INT) AS dribbles_made,
        CAST(SUM(TACKLES_COMPLETED) AS INT) AS tackles_completed,
        ROUND(AVG(SAVE_RATIO), 4) AS save_ratio,
        CAST(SUM(CHANCES_CREATED) AS INT) AS chances_created,
        CAST(SUM(PASSES_COMPLETED) AS INT) AS passes_completed
"""


def format_position_tag(player: dict) -> str:
    """
    Formatea la etiqueta táctica del jugador combinando su categoría, rol y banda si la posee.
    """
    cat, role, side = player["primary_category"], player["primary_role_code"], player["primary_side_code"]
    return f"{cat} ({role} - {side})" if pd.notna(side) else f"{cat} ({role})"


@st.cache_data(ttl="1h", show_spinner=False)
def get_global_metric_bounds() -> dict[str, tuple[float, float]]:
    """
    Calcula los valores mínimos y máximos globales por jugador para normalizar los 6 ejes del radar.
    """
    df = query_base_data(
        """
        WITH player_totals AS (
            SELECT
                SUM(GOALS) AS goals,
                SUM(DRIBBLES_MADE) AS dribbles_made,
                SUM(TACKLES_COMPLETED) AS tackles_completed,
                AVG(SAVE_RATIO) AS save_ratio,
                SUM(CHANCES_CREATED) AS chances_created,
                SUM(PASSES_COMPLETED) AS passes_completed
            FROM df_base
            GROUP BY PLAYER_ID
        )
        SELECT
            MIN(goals) AS min_goals, MAX(goals) AS max_goals,
            MIN(dribbles_made) AS min_dribbles_made, MAX(dribbles_made) AS max_dribbles_made,
            MIN(tackles_completed) AS min_tackles_completed, MAX(tackles_completed) AS max_tackles_completed,
            MIN(save_ratio) AS min_save_ratio, MAX(save_ratio) AS max_save_ratio,
            MIN(chances_created) AS min_chances_created, MAX(chances_created) AS max_chances_created,
            MIN(passes_completed) AS min_passes_completed, MAX(passes_completed) AS max_passes_completed
        FROM player_totals
        """
    )
    row = df.iloc[0]
    return {key: (float(row[f"min_{key}"]), float(row[f"max_{key}"])) for key, _ in METRICS}


@st.cache_data(ttl="1h", show_spinner=False)
def get_available_divisions() -> list[str]:
    """
    Devuelve la lista ordenada de divisiones activas en la temporada 2025/26.
    """
    df = query_base_data(
        """
        SELECT DISTINCT DIVISION_NAME
        FROM df_base
        WHERE SEASON_LABEL = '2025/26'
          AND DIVISION_NAME IS NOT NULL
        ORDER BY DIVISION_NAME
        """
    )
    return df["DIVISION_NAME"].tolist()


@st.cache_data(ttl="1h", show_spinner=False)
def get_available_roles(category: str) -> list[str]:
    """
    Devuelve los códigos de rol táctico disponibles para la categoría posicional seleccionada.
    """
    df = query_base_data(
        """
        SELECT DISTINCT PRIMARY_ROLE_CODE
        FROM df_base
        WHERE (? = 'Todas' OR PRIMARY_CATEGORY = ?)
        ORDER BY PRIMARY_ROLE_CODE
        """,
        params=[category, category],
    )
    return df["PRIMARY_ROLE_CODE"].tolist()


@st.cache_data(ttl="1h", show_spinner=False)
def get_available_sides(category: str, role_code: str) -> list[str]:
    """
    Devuelve los códigos de banda disponibles según la categoría y el rol táctico seleccionados.
    """
    df = query_base_data(
        """
        SELECT DISTINCT PRIMARY_SIDE_CODE
        FROM df_base
        WHERE PRIMARY_SIDE_CODE IS NOT NULL
          AND (? = 'Todas' OR PRIMARY_CATEGORY = ?)
          AND (? = 'Todos' OR PRIMARY_ROLE_CODE = ?)
        ORDER BY PRIMARY_SIDE_CODE
        """,
        params=[category, category, role_code, role_code],
    )
    return df["PRIMARY_SIDE_CODE"].tolist()


@st.cache_data(ttl="1h", show_spinner=False)
def get_clubs_by_division(division_name: str) -> list[str]:
    """
    Devuelve los clubes pertenecientes a la división seleccionada en la temporada 2025/26.
    """
    df = query_base_data(
        """
        SELECT DISTINCT CLUB_NAME
        FROM df_base
        WHERE SEASON_LABEL = '2025/26'
          AND DIVISION_NAME = ?
        ORDER BY CLUB_NAME
        """,
        params=[division_name],
    )
    return df["CLUB_NAME"].tolist()


@st.cache_data(ttl="1h", show_spinner=False)
def search_candidate_options(
    division: str,
    category: str,
    role_code: str,
    side_code: str,
    search_term: str,
    limit: int = 80,
) -> list[dict]:
    """
    Filtra jugadores según los criterios seleccionados y devuelve sus estadísticas acumuladas
    en todas las temporadas, ordenados por mayor habilidad.
    """
    term = f"%{search_term.strip()}%" if search_term else "%"
    df = query_base_data(
        f"""
        {STATS_SELECT_SQL}
        FROM df_base
        WHERE (? = 'Todas' OR PRIMARY_CATEGORY = ?)
          AND (? = 'Todos' OR PRIMARY_ROLE_CODE = ?)
          AND (? = 'Todos' OR PRIMARY_SIDE_CODE = ?)
          AND NAME ILIKE ?
        GROUP BY PLAYER_ID, NAME, PRIMARY_CATEGORY, PRIMARY_ROLE_CODE, PRIMARY_SIDE_CODE
        HAVING BOOL_OR(? = 'Todas' OR DIVISION_NAME = ?)
        ORDER BY MAX(ABILITY_SCORE) DESC, NAME ASC
        LIMIT ?
        """,
        params=[
            category, category,
            role_code, role_code,
            side_code, side_code,
            term,
            division, division,
            limit,
        ],
    )
    return df.to_dict(orient="records")


@st.cache_data(ttl="1h", show_spinner=False)
def get_club_roster_stats(club_name: str) -> list[dict]:
    """
    Obtiene la plantilla 2025/26 del club seleccionado junto con las estadísticas históricas
    acumuladas de cada uno de sus jugadores.
    """
    df = query_base_data(
        f"""
        {STATS_SELECT_SQL}
        FROM df_base
        WHERE PLAYER_ID IN (
            SELECT DISTINCT PLAYER_ID
            FROM df_base
            WHERE SEASON_LABEL = '2025/26'
              AND CLUB_NAME = ?
        )
        GROUP BY PLAYER_ID, NAME, PRIMARY_CATEGORY, PRIMARY_ROLE_CODE, PRIMARY_SIDE_CODE
        ORDER BY PRIMARY_CATEGORY, NAME
        """,
        params=[club_name],
    )
    return df.to_dict(orient="records")


def build_radar_chart_option(
    p1_data: dict,
    p2_data: dict,
    bounds: dict[str, tuple[float, float]],
) -> dict:
    """
    Construye el gráfico de radar usando la data de los jugadores seleccionados.
    """
    players_style = [
        (p1_data, "#04f5ff", "rgba(4, 245, 255, 0.25)"),
        (p2_data, "#e4006f", "rgba(228, 0, 111, 0.25)"),
    ]

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
            "left": "center",
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
            "center": ["50%", "48%"],
            "radius": "62%",
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
            "indicator": [
                {"name": label, "min": bounds[key][0], "max": bounds[key][1]}
                for key, label in METRICS
            ],
        },
        "series": [
            {
                "type": "radar",
                "emphasis": {"lineStyle": {"width": 4}},
                "data": [
                    {
                        "value": [p[key] for key, _ in METRICS],
                        "name": p["name"],
                        "symbol": "circle",
                        "symbolSize": 6,
                        "lineStyle": {"color": color, "width": 3},
                        "itemStyle": {"color": color},
                        "areaStyle": {"color": area_color},
                    }
                    for p, color, area_color in players_style
                ],
            }
        ],
    }


def render_candidate_selector(
    slot_key: str,
    title_label: str,
    divisions_options: list[str],
    default_idx: int = 0,
) -> dict | None:
    """
    Renderiza las opciones de filtrado de un jugador candidato y devuelve el diccionario del jugador elegido según los filtros.
    """
    st.markdown(f"**{title_label}**")

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_div = st.selectbox("División", options=divisions_options, key=f"{slot_key}_div")
    with f_col2:
        selected_pos = st.selectbox("Posición", options=POSITION_OPTIONS, key=f"{slot_key}_pos")

    f_col3, f_col4 = st.columns(2)
    with f_col3:
        selected_role = st.selectbox(
            "Rol",
            options=["Todos"] + get_available_roles(selected_pos),
            key=f"{slot_key}_role",
        )
    with f_col4:
        selected_side = st.selectbox(
            "Banda / Lado",
            options=["Todos"] + get_available_sides(selected_pos, selected_role),
            key=f"{slot_key}_side",
        )

    search_term = st.text_input(
        "Buscar por nombre",
        placeholder="Ej. Vinícius, Mbappé...",
        key=f"{slot_key}_search",
    )

    candidates = search_candidate_options(
        selected_div, selected_pos, selected_role, selected_side, search_term
    )
    if not candidates:
        st.info("No se encontraron jugadores con esos filtros.")
        return None

    return st.selectbox(
        "Seleccionar Futbolista",
        options=candidates,
        help="Selecciona un jugador de la lista filtrada para comparar, esta lista tiene al top 80 por puntaje de habilidad",
        index=min(default_idx, len(candidates) - 1),
        format_func=lambda c: f"{c['name']} - {format_position_tag(c)}",
        key=f"{slot_key}_player",
    )


def p_comparativa():
    banner(
        title="Comparativa Radar de Rendimiento",
        subtitle="Análisis multidimensional de perfiles de jugadores y selección de los mismos con apoyo de nuestro agente director deportivo de IA.",
    )

    st.markdown(
        """
        ### Uso del comparador

        Esta sección permite contrastar el rendimiento acumulado de dos futbolistas en seis métricas clave: goles, regates, entradas completadas, ratio de paradas, ocasiones creadas y pases completados. Los ejes del radar utilizan los valores máximos y mínimos globales de la base de datos para normalizar los rangos.

        **Pasos:**
        1. **Filtrar y elegir candidatos**: Usa los selectores debajo del gráfico para buscar por liga, posición, rol, banda o nombre a los dos jugadores que quieras comparar.
        2. **Elegir el club destino**: Selecciona la división y el club donde se evaluaría su incorporación, se incluirá el roester actual del club temporada 2025-2026.
        3. **Enviar al Agente Coach**: Cuando esté listo, haz click en enviar para hacer la solicitud a nuestro agente de IA con las estadísticas de ambos candidatos y la plantilla actual del club seleccionado.
        """
    )

    bounds = get_global_metric_bounds()
    divisions = get_available_divisions()
    divisions_filter_options = ["Todas"] + divisions

    radar_container = st.container()
    controls_container = st.container(border=True)

    with controls_container:
        col1, col2 = st.columns(2)
        with col1:
            p1_data = render_candidate_selector("comp_p1", "Jugador 1 (Candidato A)", divisions_filter_options, 0)
        with col2:
            p2_data = render_candidate_selector("comp_p2", "Jugador 2 (Candidato B)", divisions_filter_options, 1)

        st.markdown("#### Selección de Club Objetivo (Temporada 2025/26)")
        team_col1, team_col2 = st.columns(2)
        with team_col1:
            selected_team_div = st.selectbox(
                "División",
                options=divisions,
                index=None,
                placeholder="Selecciona una división...",
                key="comp_team_div",
            )
        with team_col2:
            selected_team = st.selectbox(
                "Equipo para la comparativa",
                options=get_clubs_by_division(selected_team_div) if selected_team_div else [],
                index=None,
                placeholder="Selecciona un equipo...",
                disabled=not selected_team_div,
                key="comp_team",
            )

        send_coach_clicked = st.button(
            "Enviar al Agente Coach",
            type="primary",
            use_container_width=True,
            disabled=not (selected_team and p1_data and p2_data),
        )

    if not (p1_data and p2_data):
        radar_container.info("Selecciona dos jugadores válidos para visualizar el radar comparativo.")
        return

    with radar_container:
        card_header = f"""
        <div style="background:linear-gradient(135deg,#26042a 0%,#1d0220 100%);border:1px solid rgba(255,255,255,0.08);border-radius:16px 16px 0 0;padding:20px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
            <div style="display:flex;align-items:center;gap:14px;">
                <div style="width:40px;height:40px;border-radius:50%;background:rgba(4,245,255,0.12);border:1px solid rgba(4,245,255,0.35);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" height="24px" width="24px" fill="#04f5ff"><path d="M8.1,21.21q-1.82-0.79-3.17-2.14Q3.58,17.73 2.79,15.9T2,12Q2,9.92 2.79,8.1Q3.58,6.27 4.93,4.93Q6.28,3.57 8.1,2.79Q9.93,2 12,2t3.9,0.79t3.17,2.14q1.35,1.35 2.14,3.17Q22,9.92 22,12t-0.79,3.9t-2.14,3.17q-1.35,1.35-3.17,2.14T12,22q-2.07,0-3.9-0.79ZM12,20q1.4,0 2.64-0.44t2.26-1.24L15.48,16.9q-0.73,0.53-1.61,0.81T12,18q-2.5,0-4.25-1.75T6,12T7.75,7.75T12,6t4.25,1.75T18,12q0,0.97-0.3,1.88T16.88,15.5l1.43,1.43q0.8-1.03 1.25-2.28T20,12q0-3.35-2.32-5.68T12,4T6.33,6.32T4,12t2.33,5.68T12,20Zm0-4q0.55,0 1.06-0.14q0.51-0.14 0.96-0.41L12.5,13.93q-0.13,0.05-0.25,0.06T12,14q-0.82,0-1.41-0.59T10,12t0.59-1.41T12,10t1.41,0.59Q14,11.18 14,12q0,0.15-0.01,0.29t-0.06,0.26l1.5,1.5q0.28-0.45 0.43-0.96Q16,12.58 16,12q0-1.65-1.17-2.83T12,8T9.18,9.17T8,12t1.18,2.82T12,16Z"/></svg>
                </div>
                <div>
                    <div style="font-family:'Outfit',sans-serif;font-size:20px;font-weight:700;color:#fbfaff;">
                        Radar Comparativo de Jugadores
                    </div>
                    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;color:#c6b5cb;margin-top:3px;">
                        Comparando {p1_data['name']} vs {p2_data['name']}
                    </div>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:6px 14px;font-family:'Plus Jakarta Sans',sans-serif;font-size:12px;font-weight:600;">
                <span style="color:#04f5ff;">P1: {format_position_tag(p1_data)}</span>
                <span style="color:rgba(255,255,255,0.25);margin:0 8px;">|</span>
                <span style="color:#e4006f;">P2: {format_position_tag(p2_data)}</span>
            </div>
        </div>
        """

        st.markdown(card_header, unsafe_allow_html=True)
        st.echarts_chart(build_radar_chart_option(p1_data, p2_data, bounds), height=480)

    if send_coach_clicked and selected_team:
        with controls_container:
            payload = {
                "target_team": selected_team,
                "candidates": [p1_data, p2_data],
                "current_team_roster_stats": get_club_roster_stats(selected_team),
            }
            st.success("Datos listos para enviar al Agente Coach.")
            with st.expander("Ver JSON generado"):
                st.json(payload)
