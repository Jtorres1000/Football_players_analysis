import streamlit as st


def p_inicio():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

            .pitchside-banner {
                position: relative;
                background: 
                    radial-gradient(ellipse 65% 75% at 5% 0%, rgba(228, 0, 111, 0.20) 0%, transparent 60%),
                    radial-gradient(ellipse 55% 65% at 95% 50%, rgba(4, 245, 255, 0.12) 0%, transparent 60%),
                    linear-gradient(135deg, #35093b 0%, #29032d 45%, #1c0020 100%);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 30px 36px;
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.1);
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: space-between;
                gap: 28px;
                margin-bottom: 24px;
                overflow: hidden;
            }

            .pitchside-banner::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(228, 0, 111, 0.5) 20%, rgba(4, 245, 255, 0.5) 80%, transparent);
                pointer-events: none;
            }

            .pitchside-content {
                flex: 1 1 560px;
                min-width: 280px;
                z-index: 1;
            }

            .pitchside-title {
                font-family: 'Outfit', sans-serif !important;
                font-size: clamp(22px, 2.4vw, 34px) !important;
                font-weight: 800 !important;
                color: #fbfaff !important;
                line-height: 1.22 !important;
                letter-spacing: -0.018em !important;
                margin: 0 0 12px 0 !important;
                padding: 0 !important;
            }

            

            .pitchside-stats {
                display: flex;
                gap: 14px;
                align-items: center;
                flex-wrap: wrap;
                z-index: 1;
            }

            .pitchside-stat-card {
                background: rgba(26, 2, 29, 0.72);
                border: 1px solid rgba(255, 255, 255, 0.09);
                border-radius: 12px;
                padding: 14px 22px;
                min-width: 160px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
                backdrop-filter: blur(8px);
                display: flex;
                flex-direction: column;
                justify-content: center;
            }

            .pitchside-stat-label {
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                color: #c6b5cb;
                line-height: 1.25;
                margin-bottom: 6px;
            }

            .pitchside-stat-value {
                font-family: 'Outfit', sans-serif;
                font-size: 28px;
                font-weight: 800;
                line-height: 1;
                letter-spacing: -0.01em;
            }

            .pitchside-stat-value.green {
                color: #00ff87;
                text-shadow: 0 0 12px rgba(0, 255, 135, 0.35);
            }

            .pitchside-stat-value.cyan {
                color: #04f5ff;
                text-shadow: 0 0 12px rgba(4, 245, 255, 0.35);
            }
        </style>

        <div class="pitchside-banner">
            <div class="pitchside-content">
                <h1 class="pitchside-title">
                    Análisis del ciclo de vida futbolístico según la posición con base en el rendimiento, la longevidad y el impacto de estos en el ingreso salarial en el periodo 2022-2026
                </h1>
        </div>
            <div class="pitchside-stats">
                <div class="pitchside-stat-card">
                    <div class="pitchside-stat-label">RANGO ETARIO<br>ANALIZADO</div>
                    <div class="pitchside-stat-value green">15–38</div>
                </div>
                <div class="pitchside-stat-card">
                    <div class="pitchside-stat-label">COBERTURA<br>TEMPORAL</div>
                    <div class="pitchside-stat-value cyan">2022–26</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
