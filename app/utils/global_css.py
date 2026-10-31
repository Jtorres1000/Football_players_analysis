import streamlit as st

def global_css():
  st.markdown(
      """
    <style>

    /* Variables de estilos css */

    :root {
        --surface-card: #38003c;
        --table-header-bg: #2e0332;
        --table-row-alt: #320236;
        --surface-hover: #4a0650;
        
        --text-primary: #fbfaff;
        --text-secondary: #c6b5cb;
        --text-on-accent: #27042a;
        
        --primary: #04f5ff;
        --primary-hover: #66f8ff;
        --secondary: #ff2882;
        --tertiary: #00ff87;
        
        --border-card: rgba(255, 255, 255, 0.08);
        --border-focus: rgba(4, 245, 255, 0.5);
        --glow-cyan-sm: 0 0 12px rgba(4, 245, 255, 0.35);
        --glow-cyan-md: 0 0 16px rgba(4, 245, 255, 0.40);
    }

    /* estilos para st.metric  */

    [data-testid="stMetric"] {
        background-color: var(--surface-card);
        border: 1px solid var(--border-card);
        border-radius: 0.75rem; /* 12px */
        padding: 0.75rem 0.50rem;
        transition: all 0.2s ease-in-out;
    }

    [data-testid="stMetric"]:hover {
        border-color: var(--border-focus);
        box-shadow: var(--glow-cyan-sm);
    }

    /* Label superior pequeña */

    [data-testid="stMetricLabel"] p {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        line-height: 16px !important;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        color: var(--text-secondary) !important;
    }

    /* Valor principal métrica*/
    [data-testid="stMetricValue"] div {
        font-family: 'Outfit', sans-serif !important;
        font-size: 32px !important;
        font-weight: 500 !important;
        line-height: 36px !important;
        letter-spacing: -0.01em;
        font-variant-numeric: tabular-nums;
        color: var(--text-primary) !important;
    }

    /* Colores para los diff de métrica */
    [data-testid="stMetricDelta"] svg[fill*="green"], 
    [data-testid="stMetricDelta"] > div[style*="green"] {
        color: var(--tertiary) !important;
        fill: var(--tertiary) !important;
    }

    [data-testid="stMetricDelta"] svg[fill*="red"], 
    [data-testid="stMetricDelta"] > div[style*="red"] {
        color: var(--secondary) !important;
        fill: var(--secondary) !important;
    }

    /* Botones primarios y secundarios st.button */
    /* botones primarios*/
    button[kind="primary"] {
        background-color: var(--primary) !important;
        color: var(--text-on-accent) !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 18px !important;
        letter-spacing: 0.01em;
        border: none !important;
        border-radius: 0.5rem !important; /* 8px */
        transition: all 0.2s ease;
    }

    button[kind="primary"]:hover {
        background-color: var(--primary-hover) !important;
        box-shadow: var(--glow-cyan-md) !important;
        color: var(--text-on-accent) !important;
    }

    /* Botón secundario*/
    button[kind="secondary"] {
        background-color: transparent !important;
        color: var(--secondary) !important;
        border: 1px solid var(--secondary) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        line-height: 18px !important;
        border-radius: 0.5rem !important; /* 8px */
        transition: all 0.2s ease;
    }

    button[kind="secondary"]:hover {
        background-color: rgba(255, 40, 130, 0.12) !important;
        border-color: var(--secondary) !important;
    }

    </style>
    """,
      unsafe_allow_html=True,
  )
