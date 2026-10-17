import streamlit as st
from components import banner

def p_inicio():
    banner(
            title='Análisis del ciclo de vida futbolístico según la posición con base en el rendimiento, la longevidad y el impacto de estos en el ingreso salarial en el periodo 2022-2026',
            stat1_label='RANGO ETARIO<br>ANALIZADO',
            stat1_value='15–38',
            stat2_label='COBERTURA<br>TEMPORAL',
            stat2_value='2022–26'
        )