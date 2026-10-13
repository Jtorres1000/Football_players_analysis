import streamlit as st

from pages import p_inicio, p_infomd

st.set_page_config(page_title="Fútbol Análisis.", layout="wide", page_icon="⚽")

# Páginas del dashboard

p_inicio = st.Page(p_inicio, title="Inicio", icon="🏠")
p_infomd = st.Page(p_infomd, title="Información", icon="ℹ️")


# Creación del menú de navegación

pg = st.navigation([p_inicio, p_infomd], position="top")
pg.run()