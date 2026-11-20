import streamlit as st

from .data import load_base_mart_data


def warm_up_connection() -> None:
    """
    Precarga la conexión a Snowflake y la caché del modelo dimensional en la
    sesión inicial para evitar tiempos de espera al navegar entre páginas.
    """
    if not st.session_state.get("_mart_cache_warmed", False):
        try:
            load_base_mart_data()
            st.session_state["_mart_cache_warmed"] = True
        except Exception:
            # Si no hay credenciales de Snowflake configuradas, se ignora en desarrollo local
            pass

