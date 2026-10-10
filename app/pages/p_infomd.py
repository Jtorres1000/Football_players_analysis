import streamlit as st

def p_infomd():
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
            ">Finalidad del trabajo</h1>
            <p style="color: #FFFFFF; font-size:20px; margin-top: 8px;">
                <span style="color: #04f5ff; font-weight: bold;">> · 
</span>La finalidad de esta investigación es determinar si existe una correlación entre las variables de rendimiento y longevidad en el desarrollo del ciclo de vida futbolístico y como este afecta al ingreso salarial.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )