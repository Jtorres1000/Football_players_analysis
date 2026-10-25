import streamlit as st

from components import banner
from objetivos import objetivo1

def p_exploratorio():
    banner(
        title="Análisis Exploratorio",
        subtitle="Rendimiento, longevidad y salario de los futbolistas según grupo etario y posición, periodo 2022-2026", 
    )
    objetivo1() 