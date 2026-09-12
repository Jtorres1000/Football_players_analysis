import streamlit as st

from pages import p_inicio

st.set_page_config(page_title="Fútbol Análisis.", layout="wide", page_icon="⚽")

# Páginas del dashboard

p_inicio = st.Page(p_inicio, title="Inicio", icon="🏠")

# Creación del menú de navegación

pg = st.navigation([p_inicio], position="top")
pg.run()