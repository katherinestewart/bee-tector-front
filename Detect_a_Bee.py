import os
import streamlit as st
from PIL import Image
import requests
import pycountry

from pathlib import Path
import pycountry
from utils.ui import apply_global_css

API_URL = st.secrets.get("API_URL") or os.getenv("API_URL") or "https://imageapi2-646220559180.europe-west1.run.app"
# API_URL = "http://localhost:8000"

st.set_page_config(page_title="Detect a Bee", layout="wide", initial_sidebar_state="expanded")

BG = Path.cwd() / "assets" / "darkerhex.jpg"
apply_global_css(BG)

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "assets" / "logohd.png"

st.image(str(IMG), width=300)

st.markdown(
    """
    <div style="font-size:20px; line-height:1.6; margin-bottom:40px;">
        Welcome to <b>BeeTector</b> - an AI-powered tool for identifying <b>bumblebee</b> subspecies from photos.
        Simply upload an image, and the app will predict the subspecies if it is one of the twelve our model was trained to detect.
        <br><br>For more detailed and accurate feedback, please enter the location the photo was taken.
    </div>
    """,
    unsafe_allow_html=True,
)


def prettify_name(name: str) -> str:
    if not name:
        return name
    return name.replace("_", " ").strip()

countries = list(pycountry.countries)
name_to_code = {c.name: c.alpha_2 for c in countries}

country_names_sorted = sorted(name_to_code.keys(), key=lambda s: s.lower())


placeholder_option = "(optional)"
options = [placeholder_option] + country_names_sorted


selected_country_name = st.selectbox("Select a country", options, index=0, key="country_select")


country_chosen = (selected_country_name != placeholder_option)

selected_country_for_api = name_to_code.get(selected_country_name, "") if country_chosen else ""

img_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if st.button("Detect this bee") and img_file:
    st.image(Image.open(img_file), caption="Uploaded Image", use_container_width=True)

    files = {"files": (img_file.name, img_file.getvalue(), img_file.type or "image/jpeg")}
    data = {"data": selected_country_for_api} if selected_country_for_api else {}

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

            st.subheader("Bee-tection Result")


            stage = result.get("stage")
            bee_prob = result.get("bumblebee_prob", 0.0)


            prediction = result.get("prediction", {}) or {}
            class_name_raw = (prediction.get("class_name") or "").strip()
            prob = prediction.get("prob", 0.0)


            class_name = prettify_name(class_name_raw)


            context_species = result.get("context_species_in_country", []) or []
            known_names = {
                (s.get("class_name") or "").strip().lower()
                for s in context_species
                if s.get("class_name")
            }


            if stage == "no_bumblebee_detected":
                st.write("We didn't detect a bumblebee in this picture")
                try:
                    st.progress(bee_prob)
                except Exception:
                    pass


                if country_chosen and context_species:
                    st.markdown("**Here are some common subspecies in your country:**")
                    for s in context_species:
                        classn_raw = s.get("class_name") or "Unknown"
                        classn = prettify_name(classn_raw)
                        commonn = s.get("common_name")
                        if commonn:
                            st.write(f"- {classn} ({commonn})")
                        else:
                            st.write(f"- {classn}")

            else:

                high_conf_and_present = (
                    stage == "subspecies_high_conf" and
                    (not country_chosen or (class_name_raw and class_name_raw.lower() in known_names))
                )

                if high_conf_and_present:
                    st.write("We found your bumblebee!")
                    if class_name:
                        st.write(f"**Subspecies:** {class_name}")
                        st.write(f"**Confidence:** {prob:.2%}")
                        try:
                            st.progress(prob)
                        except Exception:
                            pass


                    if country_chosen:

                        matched_lower = (class_name_raw or "").strip().lower()
                        other_species = [
                            s for s in context_species
                            if (s.get("class_name") or "").strip().lower() != matched_lower
                        ]
                        st.markdown("**Here are some other common subspecies in your country:**")
                        if other_species:
                            for s in other_species:
                                classn_raw = s.get("class_name") or "Unknown"
                                classn = prettify_name(classn_raw)
                                commonn = s.get("common_name")
                                if commonn:
                                    st.write(f"- {classn} ({commonn})")
                                else:
                                    st.write(f"- {classn}")
                        else:
                            st.write("_No other known subspecies are listed for the selected country._")


                elif stage in ["subspecies_low_conf", "subspecies_high_conf"]:

                    st.write("This is a bumblebee, but not a subspecies our model can detect.")


                else:
                    st.write(stage or "Unknown stage")
                    try:
                        st.progress(bee_prob)
                    except Exception:
                        pass


                if country_chosen and context_species and not high_conf_and_present:
                    st.markdown("**Here are some common subspecies in your country:**")
                    for s in context_species:
                        classn_raw = s.get("class_name") or "Unknown"
                        classn = prettify_name(classn_raw)
                        commonn = s.get("common_name")
                        if commonn:
                            st.write(f"- {classn} ({commonn})")
                        else:
                            st.write(f"- {classn}")
