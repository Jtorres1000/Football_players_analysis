import streamlit as st


def p_inicio():
    st.markdown(
        """
        <div style="
            background-color: #38003c;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #04f5ff;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
            margin-bottom: 20px;
        ">
            <h1 style="
                font-family: 'Outfit', sans-serif;
                color: #fbfaff;
                margin: 0;
                font-size: 45px;
                font-weight: 900;
                letter-spacing: -0.015em;
            ">Análisis del ciclo de vida futbolístico según la posición con base en el rendimiento, la longevidad y el impacto de estos en el ingreso salarial en el periodo 2022-2026</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
