# pages/World_Map.py
from pathlib import Path

import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="World Map", layout="wide")
st.title("Bumble Bee Observations")

# ********** IMAGE URLS **********
SPECIES_IMG = {
    "Common Eastern Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20impatiens.jpg",
    "Common Carder Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20pascuorum%20Zurich%20lateral.jpg",
    "Brown-belted Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20griseocollis%20Female%20brown-belted%20bumble%20bee%20on%20purple%20prairie%20clover%20Sand%20Lake%20WMD%20(12842806815).jpg",
    "Buff-tailed Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20terrestris.jpg",
    "Red-tailed Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20lapidarius%20-%20Sonchus%20asper%20-%20Keila.jpg",
    "Two-spotted Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20bimaculatus%2079944979.jpg",
    "Tricolored Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20ternariusCHP.JPG",
    "Yellow-faced Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20vosnesenskii%20(23838057375).jpg",
    "White-tailed Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20lucorum%2001.JPG",
    "American Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/American%20Bumble%20Bee,%20female%20(Apidae,%20Bombus%20pensylvanicus)%20(28668814812).jpg",
    "Red-belted Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20rufocinctus.jpg",
    "Half-black Bumble Bee": "https://commons.wikimedia.org/wiki/Special:FilePath/Bombus%20vagans%2010699048.jpg",
}

# ********** COUNTRIES CSV **********
ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "bees_with_countries.csv"

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

try:
    df = load_csv(CSV_PATH)
except Exception as e:
    st.error(f"Could not load CSV at '{CSV_PATH}'.\n{e}")
    st.stop()

# ********** FILTER & IMAGE LINKS **********
keep = list(SPECIES_IMG.keys())
df = df[df["common_name"].isin(keep)].dropna(subset=["lat", "lon"]).copy()
df["img_url"] = df["common_name"].map(SPECIES_IMG)

if df.empty:
    st.warning("No rows after filtering, check columns common_name, lat, lon.")
    st.stop()

# ********** MAP **********
view_state = pdk.ViewState(
    latitude=float(df["lat"].mean()),
    longitude=float(df["lon"].mean()),
    zoom=2,
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[lon, lat]",
    get_radius=80000,
    pickable=True,
)

tooltip = {
    "html": "<b>{common_name}</b><br/><img src='{img_url}' width='180'/>",
    "style": {"backgroundColor": "white", "color": "black"},
}

deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
st.pydeck_chart(deck)

st.caption("Images from Wikimedia Commons; check file pages for licenses.")
