import streamlit as st


def p_infomd():
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
                padding: 28px 36px;
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.1);
                display: flex;
                align-items: center;
                justify-content: flex-start;
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
                width: 100%;
                z-index: 1;
            }

            .pitchside-title {
                font-family: 'Outfit', sans-serif !important;
                font-size: clamp(24px, 2.5vw, 36px) !important;
                font-weight: 800 !important;
                color: #fbfaff !important;
                line-height: 1.22 !important;
                letter-spacing: -0.018em !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            .pitchside-desc {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-size: 14.5px !important;
                line-height: 1.55 !important;
                color: #c6b5cb !important;
                margin: 0 !important;
                max-width: 820px;
            }
        </style>

        <div class="pitchside-banner">
            <div class="pitchside-content">
                <h1 class="pitchside-title">
                    Trabajo investigativo
                </h1>
                <p class="pitchside-desc">
                 La finalidad de esta investigación es determinar si existe una correlación entre las variables de rendimiento y longevidad en el desarrollo del ciclo de vida futbolístico y como este afecta al ingreso salarial.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )