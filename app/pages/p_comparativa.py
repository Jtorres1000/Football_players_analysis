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

POSITION_OPTIONS = [
    "Todas",
    "ATTACKER",
    "MIDFIELDER",
    "DEFENDER",
    "GOALKEEPER",
]


def _clean_code(val) -> str | None:
    if val is None or pd.isna(val):
        return None
    s = str(val).strip()
    return s if s else None


def _format_position_tag(
    category: str | None,
    role_code: str | None,
    side_code: str | None,
) -> str:
    cat = _clean_code(category) or "N/A"
    role = _clean_code(role_code)
    side = _clean_code(side_code)

    if role and side:
        return f"{cat}({role} - {side})"
    if role:
        return f"{cat}({role})"
    if side:
        return f"{cat}({side})"
    return cat


@st.cache_data(ttl="1h", show_spinner=False)
def _get_global_metric_bounds() -> dict[str, tuple[float, float]]:
    df = query_base_data(
        """
        WITH player_totals AS (
            SELECT
                PLAYER_ID,
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
    if df.empty:
        return {key: (0.0, 1.0) for key, _ in METRICS}

    row = df.iloc[0]
    bounds = {}
    for key, _ in METRICS:
        min_v = float(row[f"min_{key}"]) if row[f"min_{key}"] is not None else 0.0
        max_v = float(row[f"max_{key}"]) if row[f"max_{key}"] is not None else 1.0
        if max_v <= min_v:
            max_v = min_v + 1.0
        bounds[key] = (min_v, max_v)
    return bounds


@st.cache_data(ttl="1h", show_spinner=False)
def _get_available_divisions() -> list[str]:
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
def _get_available_roles(category: str) -> list[str]:
    conditions = ["PRIMARY_ROLE_CODE IS NOT NULL"]
    params: list = []
    if category and category != "Todas":
        conditions.append("PRIMARY_CATEGORY = ?")
        params.append(category)

    where_clause = " AND ".join(conditions)
    df = query_base_data(
        f"""
        SELECT DISTINCT PRIMARY_ROLE_CODE
        FROM df_base
        WHERE {where_clause}
        ORDER BY PRIMARY_ROLE_CODE
        """,
        params=params,
    )
    return df["PRIMARY_ROLE_CODE"].tolist()


@st.cache_data(ttl="1h", show_spinner=False)
def _get_available_sides(category: str, role_code: str) -> list[str]:
    conditions = ["PRIMARY_SIDE_CODE IS NOT NULL"]
    params: list = []
    if category and category != "Todas":
        conditions.append("PRIMARY_CATEGORY = ?")
        params.append(category)
    if role_code and role_code != "Todos":
        conditions.append("PRIMARY_ROLE_CODE = ?")
        params.append(role_code)

    where_clause = " AND ".join(conditions)
    df = query_base_data(
        f"""
        SELECT DISTINCT PRIMARY_SIDE_CODE
        FROM df_base
        WHERE {where_clause}
        ORDER BY PRIMARY_SIDE_CODE
        """,
        params=params,
    )
    return df["PRIMARY_SIDE_CODE"].tolist()


@st.cache_data(ttl="1h", show_spinner=False)
def _get_clubs_by_division(division_name: str) -> list[str]:
    df = query_base_data(
        """
        SELECT DISTINCT CLUB_NAME
        FROM df_base
        WHERE SEASON_LABEL = '2025/26'
          AND DIVISION_NAME = ?
          AND CLUB_NAME IS NOT NULL
        ORDER BY CLUB_NAME
        """,
        params=[division_name],
    )
    return df["CLUB_NAME"].tolist()


@st.cache_data(ttl="1h", show_spinner=False)
def _search_candidate_options(
    division: str,
    category: str,
    role_code: str,
    side_code: str,
    search_term: str,
    default_name: str | None = None,
    limit: int = 80,
) -> list[dict]:
    conditions = ["1=1"]
    params: list = []

    if division and division != "Todas":
        conditions.append("DIVISION_NAME = ?")
        params.append(division)

    if category and category != "Todas":
        conditions.append("PRIMARY_CATEGORY = ?")
        params.append(category)

    if role_code and role_code != "Todos":
        conditions.append("PRIMARY_ROLE_CODE = ?")
        params.append(role_code)

    if side_code and side_code != "Todos":
        conditions.append("PRIMARY_SIDE_CODE = ?")
        params.append(side_code)

    cleaned_search = search_term.strip() if search_term else ""
    if cleaned_search:
        conditions.append("NAME ILIKE ?")
        params.append(f"%{cleaned_search}%")

    where_clause = " AND ".join(conditions)
    params.append(limit)

    df = query_base_data(
        f"""
        SELECT
            CAST(PLAYER_ID AS INT) AS player_id,
            NAME AS name,
            PRIMARY_CATEGORY AS primary_category,
            PRIMARY_ROLE_CODE AS primary_role_code,
            PRIMARY_SIDE_CODE AS primary_side_code,
            MAX(ABILITY_SCORE) AS max_ability
        FROM df_base
        WHERE {where_clause}
        GROUP BY
            PLAYER_ID,
            NAME,
            PRIMARY_CATEGORY,
            PRIMARY_ROLE_CODE,
            PRIMARY_SIDE_CODE
        ORDER BY max_ability DESC NULLS LAST, NAME ASC
        LIMIT ?
        """,
        params=params,
    )
    records = df.to_dict(orient="records")

    if (
        default_name
        and division == "Todas"
        and category == "Todas"
        and role_code == "Todos"
        and side_code == "Todos"
        and not cleaned_search
        and not any(r["name"] == default_name for r in records)
    ):
        default_df = query_base_data(
            """
            SELECT
                CAST(PLAYER_ID AS INT) AS player_id,
                NAME AS name,
                PRIMARY_CATEGORY AS primary_category,
                PRIMARY_ROLE_CODE AS primary_role_code,
                PRIMARY_SIDE_CODE AS primary_side_code,
                MAX(ABILITY_SCORE) AS max_ability
            FROM df_base
            WHERE NAME = ?
            GROUP BY
                PLAYER_ID,
                NAME,
                PRIMARY_CATEGORY,
                PRIMARY_ROLE_CODE,
                PRIMARY_SIDE_CODE
            LIMIT 1
            """,
            params=[default_name],
        )
        if not default_df.empty:
            records.insert(0, default_df.iloc[0].to_dict())

    return records


@st.cache_data(ttl="1h", show_spinner=False)
def _get_player_stats_by_id(player_id: int) -> dict:
    df = query_base_data(
        """
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
        FROM df_base
        WHERE PLAYER_ID = ?
        GROUP BY
            PLAYER_ID,
            NAME,
            PRIMARY_CATEGORY,
            PRIMARY_ROLE_CODE,
            PRIMARY_SIDE_CODE
        """,
        params=[int(player_id)],
    )
    if df.empty:
        return {
            "name": "Sin selección",
            "primary_category": "N/A",
            "primary_role_code": None,
            "primary_side_code": None,
            "goals": 0,
            "dribbles_made": 0,
            "tackles_completed": 0,
            "save_ratio": 0.0,
            "chances_created": 0,
            "passes_completed": 0,
        }
    record = df.iloc[0].to_dict()
    record["primary_role_code"] = _clean_code(record.get("primary_role_code"))
    record["primary_side_code"] = _clean_code(record.get("primary_side_code"))
    return record


@st.cache_data(ttl="1h", show_spinner=False)
def _get_club_roster_stats(club_name: str) -> list[dict]:
    df = query_base_data(
        """
        WITH roster_25_26 AS (
            SELECT DISTINCT PLAYER_ID
            FROM df_base
            WHERE SEASON_LABEL = '2025/26'
              AND CLUB_NAME = ?
        )
        SELECT
            b.NAME AS name,
            b.PRIMARY_CATEGORY AS primary_category,
            b.PRIMARY_ROLE_CODE AS primary_role_code,
            b.PRIMARY_SIDE_CODE AS primary_side_code,
            CAST(SUM(b.GOALS) AS INT) AS goals,
            CAST(SUM(b.DRIBBLES_MADE) AS INT) AS dribbles_made,
            CAST(SUM(b.TACKLES_COMPLETED) AS INT) AS tackles_completed,
            ROUND(AVG(b.SAVE_RATIO), 4) AS save_ratio,
            CAST(SUM(b.CHANCES_CREATED) AS INT) AS chances_created,
            CAST(SUM(b.PASSES_COMPLETED) AS INT) AS passes_completed
        FROM df_base b
        INNER JOIN roster_25_26 r
            ON b.PLAYER_ID = r.PLAYER_ID
        GROUP BY
            b.PLAYER_ID,
            b.NAME,
            b.PRIMARY_CATEGORY,
            b.PRIMARY_ROLE_CODE,
            b.PRIMARY_SIDE_CODE
        ORDER BY b.PRIMARY_CATEGORY, b.NAME
        """,
        params=[club_name],
    )
    records = df.to_dict(orient="records")
    for rec in records:
        rec["primary_role_code"] = _clean_code(rec.get("primary_role_code"))
        rec["primary_side_code"] = _clean_code(rec.get("primary_side_code"))
    return records


def _build_radar_chart_option(
    p1_data: dict,
    p2_data: dict,
    bounds: dict[str, tuple[float, float]],
) -> dict:
    indicators = []
    p1_values = []
    p2_values = []

    for key, label in METRICS:
        min_val, max_val = bounds[key]
        indicators.append({
            "name": label,
            "text": label,
            "min": min_val,
            "max": max_val,
        })

        v1 = p1_data[key]
        v2 = p2_data[key]

        p1_values.append(round(v1, 4) if isinstance(v1, float) else int(v1))
        p2_values.append(round(v2, 4) if isinstance(v2, float) else int(v2))

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
                        "symbolSize": 6,
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


def _render_candidate_selector(
    slot_key: str,
    title_label: str,
    default_player_name: str,
    divisions_options: list[str],
) -> int | None:
    
    st.markdown(f"**{title_label}**")
    f_col1, f_col2 = st.columns(2)

    with f_col1:
        selected_div = st.selectbox(
            "División",
            options=divisions_options,
            index=0,
            key=f"{slot_key}_div",
        )
    with f_col2:
        selected_pos = st.selectbox(
            "Posición",
            options=POSITION_OPTIONS,
            index=0,
            key=f"{slot_key}_pos",
        )

    role_options = ["Todos"] + _get_available_roles(selected_pos)

    f_col3, f_col4 = st.columns(2)
    with f_col3:
        selected_role = st.selectbox(
            "Rol (Role Code)",
            options=role_options,
            index=0,
            key=f"{slot_key}_role",
        )
    side_options = ["Todos"] + _get_available_sides(selected_pos, selected_role)
    with f_col4:
        selected_side = st.selectbox(
            "Banda / Lado (Side Code)",
            options=side_options,
            index=0,
            key=f"{slot_key}_side",
        )

    search_term = st.text_input(
        "Buscar por nombre",
        value="",
        placeholder="Ej. Vinícius, Mbappé...",
        key=f"{slot_key}_search",
    )

    candidates = _search_candidate_options(
        division=selected_div,
        category=selected_pos,
        role_code=selected_role,
        side_code=selected_side,
        search_term=search_term,
        default_name=default_player_name,
        limit=80,
    )

    if not candidates:
        st.info("No se encontraron jugadores con esos filtros.")
        return None

    option_ids = [c["player_id"] for c in candidates]
    label_map = {
        c["player_id"]: (
            f"{c['name']} - "
            f"{_format_position_tag(c.get('primary_category'), c.get('primary_role_code'), c.get('primary_side_code'))}"
        )
        for c in candidates
    }

    default_idx = 0
    for idx, c in enumerate(candidates):
        if c["name"] == default_player_name:
            default_idx = idx
            break

    selected_id = st.selectbox(
        "Seleccionar Futbolista - Top 80 por puntaje de habilidad",
        options=option_ids,
        index=default_idx,
        format_func=lambda pid: label_map.get(pid, str(pid)),
        key=f"{slot_key}_player_id",
    )
    return selected_id


def p_comparativa():
    banner(
        title="Comparativa Radar de Rendimiento",
        subtitle="Análisis multidimensional de perfiles de jugadores y selección de los mismos con apoyo de nuestro agente director deportivo de IA.",
    )

    st.markdown(
        """
        ### Propósito del Módulo y Flujo de Trabajo

        Esta herramienta permite comparar perfiles de rendimiento entre dos futbolistas en seis dimensiones esenciales: goles, regates realizados, entradas completadas, ratio de paradas, ocasiones creadas y pases completados. Los ejes emplean una escala normalizada con topes referenciales globales extraídos del modelo dimensional, garantizando que el perfil geométrico de cada jugador permanezca inmutable al contrastarlo frente a distintos rivales.

        **Pasos para el análisis:**
        1. **Inspección del Radar**: Observa la superposición de polígonos en la tarjeta visual. Al interactuar con cada vértice, el cursor revelará la estadística cuantitativa acumulada real.
        2. **Configuración de Candidatos**: Filtra por división, posición, rol, lado o nombre para acotar la búsqueda y selecciona a los dos futbolistas a confrontar.
        3. **Asignación del Club Objetivo**: Selecciona la división y el equipo donde se proyecta la evaluación de los perfiles para activar la comunicación con el módulo de inteligencia.
        4. **Envío al Agente Coach**: Acciona el botón de envío para empaquetar los datos de los futbolistas y la plantilla actual (2025/26) del club en la estructura estandarizada que procesará el agente para el reporte final.
        """
    )

    bounds = _get_global_metric_bounds()
    divisions = _get_available_divisions()
    divisions_filter_options = ["Todas"] + divisions

    radar_container = st.container()
    controls_container = st.container()

    with controls_container:
        col1, col2 = st.columns(2)
        with col1:
            p1_id = _render_candidate_selector(
                slot_key="comp_p1",
                title_label="Jugador 1 (Candidato A)",
                default_player_name="Nesto Groen",
                divisions_options=divisions_filter_options,
            )
        with col2:
            p2_id = _render_candidate_selector(
                slot_key="comp_p2",
                title_label="Jugador 2 (Candidato B)",
                default_player_name="Vinícius Júnior",
                divisions_options=divisions_filter_options,
            )

        st.markdown("#### Selección de Club Objetivo (Temporada 2025/26)")
        team_col1, team_col2 = st.columns(2)

        with team_col1:
            selected_team_div = st.selectbox(
                "División",
                options=divisions,
                index=None,
                placeholder="Seleccione primero una división...",
                key="comp_team_div",
            )
        with team_col2:
            clubs_in_div = (
                _get_clubs_by_division(selected_team_div)
                if selected_team_div
                else []
            )
            selected_team = st.selectbox(
                "Selecciona el equipo para la Comparativa",
                options=clubs_in_div,
                index=None,
                placeholder=(
                    "Seleccione un equipo..."
                    if selected_team_div
                    else "Elija una división para listar sus clubes..."
                ),
                disabled=not bool(selected_team_div),
                key="comp_team",
            )

        send_coach_clicked = st.button(
            "Enviar al Agente Coach",
            type="primary",
            use_container_width=True,
            disabled=not bool(selected_team and p1_id is not None and p2_id is not None),
        )

    p1_data = _get_player_stats_by_id(p1_id) if p1_id is not None else _get_player_stats_by_id(-1)
    p2_data = _get_player_stats_by_id(p2_id) if p2_id is not None else _get_player_stats_by_id(-1)

    with radar_container:
        tag1 = _format_position_tag(
            p1_data.get("primary_category"),
            p1_data.get("primary_role_code"),
            p1_data.get("primary_side_code"),
        )
        tag2 = _format_position_tag(
            p2_data.get("primary_category"),
            p2_data.get("primary_role_code"),
            p2_data.get("primary_side_code"),
        )

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
                <span style="color: #04f5ff;">P1: {tag1}</span>
                <span style="color: rgba(255, 255, 255, 0.25); margin: 0 8px;">|</span>
                <span style="color: #e4006f;">P2: {tag2}</span>
            </div>
        </div>
        """

        st.markdown(card_header, unsafe_allow_html=True)
        chart_option = _build_radar_chart_option(p1_data, p2_data, bounds)

        try:
            st.echarts_chart(chart_option, height=480, use_container_width=True)
        except TypeError:
            try:
                st.echarts_chart(chart_option, height=480)
            except TypeError:
                st.echarts_chart(chart_option)

    if send_coach_clicked and selected_team:
        with controls_container:
            roster_stats = _get_club_roster_stats(selected_team)
            payload = {
                "target_team": selected_team,
                "candidates": [
                    p1_data,
                    p2_data,
                ],
                "current_team_roster_stats": roster_stats,
            }

            st.success(
                "Payload generado con datos reales del modelo dimensional y listo para enviar al Agente Coach."
            )
            with st.expander("Ver JSON que se enviará al Agente Coach"):
                st.json(payload)
