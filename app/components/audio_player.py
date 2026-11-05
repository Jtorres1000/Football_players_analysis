import streamlit as st
import base64
from pathlib import Path

CSS = """
<style>
    .audio-card {
        margin-top: 8px;
        padding: 10px 12px;
        border-radius: 14px;
        background: rgb(255, 40, 130, 0.85);
        border: 1px solid rgba(4, 245, 255, 0.25);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }

    .audio-title {
        font-size: 12px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 6px;
        text-align: center;
    }

    .audio-card audio {
        width: 100%;
        height: 36px;
        border-radius: 20px;
        color-scheme: dark;
        outline: none;
    }

    .audio-card audio::-webkit-media-controls-panel {
        background-color: #29032d;
    }
</style>
"""

@st.cache_data(show_spinner=False)
def _load_audio_b64() -> str:
    audio_path = Path(__file__).resolve().parents[2] / "assets" / "we_are_one.mp3"
    return base64.b64encode(audio_path.read_bytes()).decode("utf-8")


def audio_player():

    st.markdown(
            f"""
            {CSS}<div class="audio-card"> <div class="audio-title">We Are One (Ole Ola)</div><audio controls src="data:audio/mp3;base64,{_load_audio_b64()}"></audio></div>
            """,
            unsafe_allow_html=True,
        )
