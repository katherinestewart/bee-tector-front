# pages/World_Map.py
from pathlib import Path

import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="World Map", layout="wide")
st.title("Bumble Bee Observations")

# ********** MAP 1 **********
st.subheader("Observations of the 12 subspecies this app can detect")

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

# ********** DOT COLOURS **********
COLOR_LIST = [
    [230, 25, 75],   # red
    [60, 180, 75],   # green
    [255, 225, 25],  # yellow
    [0, 130, 200],   # blue
    [245, 130, 48],  # orange
    [145, 30, 180],  # purple
    [70, 240, 240],  # cyan
    [240, 50, 230],  # magenta
    [210, 245, 60],  # lime
    [250, 190, 190], # pink
    [0, 128, 128],   # teal
    [128, 128, 0],   # olive
]

# ********** COUNTRIES CSV **********
ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "bees_with_countries_raw.csv"

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

try:
    df = load_csv(CSV_PATH)
except Exception as e:
    st.error(f"Could not load CSV at '{CSV_PATH}'.\n{e}")
    st.stop()

lat_col = "lat" if "lat" in df.columns else None
lon_col = "lon" if "lon" in df.columns else None
name_col = "common_name" if "common_name" in df.columns else None

if not (lat_col and lon_col and name_col):
    st.warning("CSV is missing lat/lon/common_name columns, skipping map.")
    st.stop()

df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")

# ********** FILTER & IMAGE LINKS **********
keep = list(SPECIES_IMG.keys())
df = df[df[name_col].isin(keep)].dropna(subset=[lat_col, lon_col]).copy()
df["img_url"] = df[name_col].map(SPECIES_IMG)

if df.empty:
    st.warning("No valid rows left after filtering.")
    st.stop()

# ********** MAP **********
color_map = {sp: COLOR_LIST[i % len(COLOR_LIST)] + [220]  # add alpha
             for i, sp in enumerate(keep)}
df["color"] = df[name_col].map(color_map)

view_state = pdk.ViewState(
    latitude=float(df["lat"].mean()),
    longitude=float(df["lon"].mean()),
    zoom=2,
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[lon, lat]",
    get_fill_color="color",
    get_line_color=[255, 255, 255, 220],
    stroked=True,
    line_width_min_pixels=1,
    get_radius=6,
    radius_units="pixels",
    pickable=True,
)

tooltip = {
    "html": "<b>{common_name}</b><br/><img src='{img_url}' width='180'/>",
    "style": {"backgroundColor": "white", "color": "black"},
}

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_provider="carto",
    map_style="light",
    tooltip={
        "html": "<b>{common_name}</b><br/><img src='{img_url}' width='180'/>",
        "style": {"backgroundColor": "white", "color": "black"},
    },
)

st.pydeck_chart(deck)

st.caption("Images from Wikimedia Commons; check file pages for licenses.")

# ********** MAP 2 **********
st.subheader("All Observations")

df_all = load_csv(CSV_PATH)

df_all[lat_col] = pd.to_numeric(df_all[lat_col], errors="coerce")
df_all[lon_col] = pd.to_numeric(df_all[lon_col], errors="coerce")
df2 = df_all.dropna(subset=[lat_col, lon_col]).copy()
df2 = df2[df2[name_col].str.strip().str.lower() != "bumble bees"]

view_state2 = pdk.ViewState(
    latitude=float(df2[lat_col].mean()),
    longitude=float(df2[lon_col].mean()),
    zoom=2,
)

layer2 = pdk.Layer(
    "ScatterplotLayer",
    data=df2,
    get_position=[lon_col, lat_col],
    get_fill_color=[0, 0, 0, 220],
    get_line_color=[255, 255, 255, 230],
    stroked=True,
    line_width_min_pixels=1,
    get_radius=5,
    radius_units="pixels",
    pickable=True,
)

deck2 = pdk.Deck(
    layers=[layer2],
    initial_view_state=view_state2,
    map_provider="carto",
    map_style="light",
    tooltip={
        "html": f"<b>{{{name_col}}}</b>",
        "style": {"backgroundColor": "white", "color": "black"},
    },
)

st.pydeck_chart(deck2)
