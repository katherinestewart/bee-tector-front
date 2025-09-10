import base64
from pathlib import Path
import streamlit as st

def _b64(path):
    return base64.b64encode(path.read_bytes()).decode()

def apply_global_css(bg_path: Path | None = None):
    """Inject global CSS (header/sidebar + optional background image)."""
    css = [
        "<style>",
        'header[data-testid="stHeader"] { height: 2rem; background: transparent; border: none; }',
        '[data-testid="stSidebarCollapsedControl"] {'
        '  position: fixed; top: .5rem; right: 1rem; left: auto !important; z-index: 2000;'
        '  background: rgba(0,0,0,.4); border-radius: 50%; padding: 2px;'
        '}',
        'section[data-testid="stSidebar"] { background: black !important; }',
        'section[data-testid="stSidebar"] * { color: white !important; }',
    ]

    if bg_path and bg_path.exists():
        ext = bg_path.suffix.lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        b64 = _b64(bg_path)
        css += [
            ".stApp {",
            f'  background: linear-gradient(rgba(255,255,255,0.4), rgba(255,255,255,0.4)), url("data:{mime};base64,{b64}");',
            "  background-size: cover;",
            "  background-position: center;",
            "  background-repeat: no-repeat;",
            "}",
        ]

    css.append("</style>")
    st.markdown("\n".join(css), unsafe_allow_html=True)
