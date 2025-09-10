import os
import base64
import streamlit as st
from pathlib import Path
from PIL import Image
import requests
import pycountry

# API_URL = st.secrets.get("API_URL") or os.getenv("API_URL") or "https://imageapi2-646220559180.europe-west1.run.app"
API_URL = "http://localhost:8000"

# Hide header
st.markdown(
    """
    <style>
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.markdown(
    """
    <style>
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: black;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Background image
BG_PATH = Path("assets/0005.jpg")
def get_base64(file_path):
    return base64.b64encode(open(file_path, "rb").read()).decode()

if BG_PATH.exists():
    b64 = get_base64(BG_PATH)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.1), rgba(255,255,255,0.8)),
                        url("data:image/png;base64,{b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* keep widgets flat (no extra boxes) */
        [data-testid="stFileUploader"] [data-testid="stFileUploadDropzone"],
        [data-testid="stFileUploader"] > div:first-child {{
            background: transparent !important;
            border: 1px dashed #aaa !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


st.set_page_config(page_title="Detect a Bee", layout="wide")

# st.title("BeeTector")

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "assets" / "logohd.png"

st.image(str(IMG), width=300)


st.markdown('<div class="bee-sentinel"></div>', unsafe_allow_html=True)

country_codes = [c.alpha_2 for c in pycountry.countries]
selected_country = st.selectbox("Select a country (optional)", [""] + country_codes)

img_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if st.button("Predict") and img_file:
    st.image(Image.open(img_file), caption="Uploaded Image", use_container_width=True)

    files = {"files": (img_file.name, img_file.getvalue(), img_file.type or "image/jpeg")}
    data = {"data": selected_country} if selected_country else {}

    with st.spinner("Bee patient..."):
        try:
            res = requests.post(f"{API_URL}/upload_image/", files=files, data=data, timeout=120)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        else:

            try:
                result = res.json()
            except Exception:
                st.error("API returned invalid JSON.")
                result = {}

            st.subheader("Prediction Result")

            stage = result.get("stage")
            bee_prob = result.get("bumblebee_prob", 0.0)
            st.write(f"**Stage:** {stage}")
            st.progress(bee_prob)

            if stage in ["subspecies_high_conf", "subspecies_low_conf"]:
                prediction = result.get("prediction", {}) or {}
                class_name = prediction.get("class_name", "Unknown")
                prob = prediction.get("prob", 0.0)


                if selected_country:
                    context_species = result.get("context_species_in_country", []) or []


                    known_names = {
                        (s.get("class_name") or "").strip().lower()
                        for s in context_species
                        if s.get("class_name")
                    }

                    if class_name and class_name.strip().lower() in known_names:

                        st.write(f"**This is your subspecies:** {class_name}")
                        st.write(f"**Confidence:** {prob:.2%}")
                        st.progress(prob)

                        matched_lower = class_name.strip().lower()
                        other_species = [
                            s for s in context_species
                            if (s.get("class_name") or "").strip().lower() != matched_lower
                        ]

                        if other_species:
                            st.write("**These are other subspecies in your area:**")
                            for s in other_species:
                                st.write(f"- {s.get('class_name')} ({s.get('common_name')})")
                        else:
                            st.write("_No other known subspecies are listed for the selected country._")
                    else:

                        st.write("**Unable to identify this subspecies, here is the most common one in your area:**")
                        if context_species:
                            for s in context_species:
                                st.write(f"- {s.get('class_name')} ({s.get('common_name')})")
                        else:
                            st.write("_No known subspecies are listed for the selected country._")
                else:

                    st.write(f"**Subspecies:** {class_name}")
                    st.write(f"**Confidence:** {prob:.2%}")
                    st.progress(prob)

            context_species = result.get("context_species_in_country", [])
            if context_species and not (stage in ["subspecies_high_conf", "subspecies_low_conf"] and selected_country):

                st.write("**Known subspecies in selected country:**")
                for s in context_species:
                    st.write(f"- {s.get('class_name')} ({s.get('common_name')})")
