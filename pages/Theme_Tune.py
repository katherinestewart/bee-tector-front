import streamlit as st
from pathlib import Path

from utils.ui import apply_global_css

st.set_page_config(page_title="Detect a Bee", layout="wide", initial_sidebar_state="expanded")

BG = Path.cwd() / "assets" / "darkerhex.jpg"
apply_global_css(BG)

st.title("BeeTector Theme Tune")

st.markdown(
    """
    <iframe src="https://suno.com/embed/7186eaeb-7c75-4af5-ab03-82a657fb8ce8"
            width="760" height="240"
            frameborder="0"
            allowfullscreen>
    </iframe>
    """,
    unsafe_allow_html=True,
)
