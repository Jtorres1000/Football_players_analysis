import streamlit as st

from components import banner
from objetivos import objetivo1, objetivo2, objetivo3

def p_exploratorio():
    banner(
        title="Análisis Exploratorio",
        subtitle="Rendimiento, longevidad y salario de los futbolistas según grupo etario y posición, periodo 2022-2026", 
    )
    tab1, tab2, tab3 = st.tabs(["Objetivo 1", "Objetivo 2", "Objetivo 3"])
    
    with tab1:
        objetivo1()
    
    with tab2:
        objetivo2()
    
    with tab3:
        objetivo3()