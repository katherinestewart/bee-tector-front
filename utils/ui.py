import base64
from pathlib import Path
import streamlit as st

def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

def apply_global_css(bg_path: Path | None):
    css = [
        "<style>",
        'header[data-testid="stHeader"] { height: 2rem; background: transparent !important; border: none !important; }',

        'section[data-testid="stSidebar"] { background: black !important; }',
        'section[data-testid="stSidebar"] * { color: white !important; }',
    ]

    if bg_path and bg_path.exists():
        mime = "image/png" if bg_path.suffix.lower() == ".png" else "image/jpeg"
        b64 = _b64(bg_path)
        css += [
            ".stApp::before, .stApp::after { content:none !important; display:none !important; }",
            ".stApp { background: none !important; }",

            ".stApp {",
            f'  background-image: url("data:{mime};base64,{b64}") !important;',
            "  background-size: cover !important;",
            "  background-position: center !important;",
            "  background-repeat: no-repeat !important;",
            "}",
        ]

    css.append("</style>")
    st.markdown("\n".join(css), unsafe_allow_html=True)
