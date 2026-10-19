import streamlit as st

SELECTED_FILTER_CSS = """
<style>

    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        background: 
            radial-gradient(ellipse 90% 45% at 50% 0%, rgba(228, 0, 111, 0.20) 0%, transparent 70%),
            radial-gradient(ellipse 75% 35% at 50% 100%, rgba(4, 245, 255, 0.12) 0%, transparent 70%),
            linear-gradient(180deg, #35093b 0%, #29032d 45%, #1c0020 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    section[data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebarHeader"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    span[aria-label="Selected values"] [data-tag],
    span[aria-label="Selected values"] [data-tag] span,
    [data-baseweb="tag"],
    [data-baseweb="tag"] span {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    span[aria-label="Selected values"] [data-tag] button,
    span[aria-label="Selected values"] [data-tag] svg,
    [data-baseweb="tag"] svg {
        color: #000000 !important;
        fill: #000000 !important;
    }

    span[aria-label="Selected values"] [data-tag] svg path {
        stroke: #000000 !important;
    }

    div[data-baseweb="popover"] li[aria-selected="true"],
    div[data-baseweb="popover"] li[aria-selected="true"] *,
    ul[role="listbox"] li[aria-selected="true"],
    ul[role="listbox"] li[aria-selected="true"] * {
        color: #000000 !important;
        font-weight: 600 !important;
    }

</style>
"""
SESSION_DEFAULTS = {
    "sb_season": [], 
    "sb_positions": [],
    "sb_age_groups": [],
    "sb_age_range": (15, 38),
    "sb_min_wage": 0,
}


def _reset_filters() -> None:
    for key, val in SESSION_DEFAULTS.items():
        st.session_state[key] = val


def sidebar() -> dict:

    for key, val in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val

    with st.sidebar:
        st.markdown(SELECTED_FILTER_CSS, unsafe_allow_html=True)
        st.header("Filtros de Búsqueda")

        selected_seasons = st.multiselect(
            label="Temporada",
            options=[
                "2025-2026",
                "2024-2025",
                "2023-2024",
                "2022-2023",
            ],
            key="sb_season",
            placeholder="Todas las temporadas...",
        )

        selected_positions = st.multiselect(
            label="Posición",
            options=[
                "Delanteros (ATT)",
                "Centrocampistas (MID)",
                "Defensas (DEF)",
                "Porteros (GK)",
            ],
            key="sb_positions",
            placeholder="Todas las posiciones...",
        )

        selected_age_groups = st.multiselect(
            label="Grupo Etario",
            options=[
                "15–21",
                "22–26",
                "27–31",
                "32–38",
            ],
            key="sb_age_groups",
            placeholder="Todos los grupos...",
        )

        selected_age_range = st.slider(
            label="Rango de Edad",
            min_value=15,
            max_value=38,
            key="sb_age_range",
        )

        selected_min_wage = st.slider(
            label="Salario Anual Mínimo (€)",
            min_value=0,
            max_value=20_000_000,
            step=250_000,
            format="€%d",
            key="sb_min_wage",
        )

        st.button(
            label="Restablecer Filtros",
            key="btn_reset_filters",
            width="stretch",
            on_click=_reset_filters,
        )

    return {
        "season": selected_seasons,
        "positions": selected_positions,
        "age_groups": selected_age_groups,
        "age_range": selected_age_range,
        "min_wage": selected_min_wage,
    }