import streamlit as st
from pathlib import Path
from components import sidebar
from pages import p_inicio, p_infomd, p_exploratorio, p_comparativa, p_cuestionario
from utils import warm_up_connection, global_css, download_parquets_to_duckdb

st.set_page_config(page_title="Fútbol Análisis.", layout="wide", page_icon=":material/sports_soccer:")

LOCAL_DUCKDB_PATH = Path(__file__).resolve().parents[1] / "data" / "football_local.duckdb"

global_css()

filtros = sidebar()

p_inicio = st.Page(p_inicio, title="Inicio", icon=":material/home:")
p_infomd = st.Page(p_infomd, title="Trabajo investigativo", icon=":material/info:")
p_exploratorio = st.Page(p_exploratorio, title="Análisis exploratorio", icon=":material/bar_chart:")
p_comparativa = st.Page(p_comparativa, title="Comparativa Radar", icon=":material/target:")
p_cuestionario = st.Page(p_cuestionario, title="Cuestionario SQL", icon=":material/question_answer:")

pg = st.navigation([p_inicio, p_infomd, p_exploratorio, p_comparativa, p_cuestionario], position="top")
pg.run()

warm_up_connection()

if not LOCAL_DUCKDB_PATH.exists():
    download_parquets_to_duckdb(LOCAL_DUCKDB_PATH)
