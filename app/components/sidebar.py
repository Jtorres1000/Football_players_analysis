import streamlit as st


NOMBRE_TITULO = "Filtros de Búsqueda"
NOMBRE_FILTRO_TEMPORADA = "Temporada"
NOMBRE_FILTRO_POSICION = "Posición"
NOMBRE_FILTRO_GRUPO_ETARIO = "Grupo Etario"
NOMBRE_FILTRO_RANGO_EDAD = "Rango de Edad"
NOMBRE_FILTRO_SALARIO = "Salario Anual Mínimo (€)"
NOMBRE_BOTON_RESET = "Restablecer Filtros"

SELECTED_FILTER_CSS = """
<style>
    /* Degradado de fondo del sidebar (arriba hacia abajo) con los colores del banner */
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

    /* 1. Texto de las opciones seleccionadas en multiselect (chips/tags) */
    div[data-baseweb="tag"],
    span[data-baseweb="tag"],
    [data-baseweb="tag"] span,
    [data-baseweb="tag"] div,
    [data-baseweb="tag"] p {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Ícono 'x' para eliminar la selección en el tag */
    [data-baseweb="tag"] svg {
        fill: #000000 !important;
        color: #000000 !important;
    }

    /* 2. Opciones seleccionadas o activas dentro de la lista desplegable (dropdown) */
    div[data-baseweb="popover"] li[aria-selected="true"],
    div[data-baseweb="popover"] li[aria-selected="true"] *,
    ul[role="listbox"] li[aria-selected="true"],
    ul[role="listbox"] li[aria-selected="true"] * {
        color: #000000 !important;
        font-weight: 600 !important;
    }
</style>
"""


def sidebar(
    seasons: list[str] | None = None,
    positions: list[str] | None = None,
    age_groups: list[str] | None = None,
    min_age: int = 15,
    max_age: int = 38,
    filter_names: dict[str, str] | None = None,
) -> dict:


    names = {
        "title": NOMBRE_TITULO,
        "season": NOMBRE_FILTRO_TEMPORADA,
        "position": NOMBRE_FILTRO_POSICION,
        "age_group": NOMBRE_FILTRO_GRUPO_ETARIO,
        "age_range": NOMBRE_FILTRO_RANGO_EDAD,
        "salary": NOMBRE_FILTRO_SALARIO,
        "reset": NOMBRE_BOTON_RESET,
    }
    if filter_names:
        names.update(filter_names)


    default_seasons = seasons or [
        "2025-2026",
        "2024-2025",
        "2023-2024",
        "2022-2023",
        "Todas las temporadas",
    ]

    default_positions = positions or [
        "Delanteros (ATT)",
        "Centrocampistas (MID)",
        "Defensas (DEF)",
        "Porteros (GK)",
    ]

    default_age_groups = age_groups or [
        "15–21",
        "22–26",
        "27–31",
        "32–38",
    ]

  
    SESSION_DEFAULTS = {
        "sb_season": default_seasons[0],
        "sb_positions": [],
        "sb_age_groups": [],
        "sb_age_range": (min_age, max_age),
        "sb_min_wage": 0,
    }

    for key, val in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val

    def _reset_filters():
        for k, v in SESSION_DEFAULTS.items():
            st.session_state[k] = v

    with st.sidebar:
       
        st.markdown(SELECTED_FILTER_CSS, unsafe_allow_html=True)

        
        st.header(names["title"])

        
        selected_season = st.selectbox(
            label=names["season"],
            options=default_seasons,
            key="sb_season",
        )

        
        selected_positions = st.multiselect(
            label=names["position"],
            options=default_positions,
            key="sb_positions",
            placeholder="Todas las posiciones...",
        )

       
        selected_age_groups = st.multiselect(
            label=names["age_group"],
            options=default_age_groups,
            key="sb_age_groups",
            placeholder="Todos los grupos...",
        )

       
        selected_age_range = st.slider(
            label=names["age_range"],
            min_value=min_age,
            max_value=max_age,
            key="sb_age_range",
        )

        
        selected_min_wage = st.slider(
            label=names["salary"],
            min_value=0,
            max_value=20_000_000,
            step=250_000,
            format="€%d",
            key="sb_min_wage",
        )

        
        st.button(
            label=names["reset"],
            key="btn_reset_filters",
            use_container_width=True,
            on_click=_reset_filters,
        )

    return {
        "season": selected_season,
        "positions": selected_positions,
        "age_groups": selected_age_groups,
        "age_range": selected_age_range,
        "min_wage": selected_min_wage,
    }