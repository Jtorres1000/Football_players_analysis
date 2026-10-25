import streamlit as st

from components import sidebar
from pages import p_inicio, p_infomd, p_exploratorio, p_comparativa
from utils import warm_up_connection

st.set_page_config(page_title="Fútbol Análisis.", layout="wide", page_icon="⚽")

filtros = sidebar()

p_inicio = st.Page(p_inicio, title="Inicio", icon="🏠")
p_infomd = st.Page(p_infomd, title="Trabajo investigativo", icon="ℹ️")
p_exploratorio = st.Page(p_exploratorio, title="Análisis exploratorio", icon="📊")
p_comparativa = st.Page(p_comparativa, title="Comparativa Radar", icon="🎯")

pg = st.navigation([p_inicio, p_infomd, p_exploratorio, p_comparativa], position="top")
pg.run()

warm_up_connection()
