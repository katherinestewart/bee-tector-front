import os
import streamlit as st
from PIL import Image
import requests
import pycountry
from pathlib import Path
from utils.ui import apply_global_css

API_URL = st.secrets.get("API_URL") or os.getenv("API_URL") or "https://imageapi2-646220559180.europe-west1.run.app"
# API_URL = "http://localhost:8000"

st.set_page_config(page_title="Detect a Bee", layout="wide", initial_sidebar_state="expanded")

BG = Path.cwd() / "assets" / "darkerhex.jpg"
apply_global_css(BG)

ROOT = Path(__file__).resolve().parent
IMG = ROOT / "assets" / "logohd.png"

st.image(str(IMG), width=300)


def prettify_name(name: str) -> str:
    if not name:
        return name
    return name.replace("_", " ").strip()


def _normalize_for_compare(text: str) -> str:

    if not text:
        return ""
    return "".join(text.replace("_", " ").split()).lower()


def format_common_with_scientific(scientific_raw: str, common_raw: str) -> str:

    sci = (scientific_raw or "").strip()
    common = (common_raw or "").strip()

    if common:

        if sci and _normalize_for_compare(common) != _normalize_for_compare(sci):
            return f"{common} ({sci})"
        return common


    if sci:
        return sci

    return ""


def lookup_names_for_class(class_name_raw: str, context_species: list) -> tuple:

    class_key = (class_name_raw or "").strip().lower()
    if class_key and context_species:
        for s in context_species:
            if (s.get("class_name") or "").strip().lower() == class_key:
                return (s.get("scientific_name") or "", s.get("common_name") or "")


    fallback_common = prettify_name(class_name_raw) if class_name_raw else ""
    return ("", fallback_common)



def show_progress(value: float):

    try:

        if value is None:
            pct = 0
        else:
            try:

                val = float(value)
                pct = int(val * 100) if val <= 1 else int(val)
            except Exception:
                pct = 0
        if pct < 0:
            pct = 0
        if pct > 100:
            pct = 100


        bar_html = f"""
        <style>
        .progress-honey {{
            width: 100%;
            height: 18px;
            -webkit-appearance: none;
            appearance: none;
            border-radius: 9px;
            overflow: hidden;
        }}
        .progress-honey::-webkit-progress-bar {{
            background-color: rgba(0,0,0,0.06);
        }}
        .progress-honey::-webkit-progress-value {{
            background: linear-gradient(90deg, #F6C84C 0%, #F3B430 100%);
        }}
        .progress-honey::-moz-progress-bar {{
            background: linear-gradient(90deg, #F6C84C 0%, #F3B430 100%);
        }}
        </style>
        <progress class="progress-honey" value="{pct}" max="100"></progress>
        """
        st.markdown(bar_html, unsafe_allow_html=True)
    except Exception:

        try:
            st.progress(value)
        except Exception:
            pass



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
                    show_progress(bee_prob)
                except Exception:
                    pass

                if country_chosen and context_species:
                    st.markdown("**Here are some common subspecies in your country:**")
                    for s in context_species:

                        sci_raw = s.get("scientific_name") or s.get("class_name") or ""
                        commonn = s.get("common_name") or ""
                        display = format_common_with_scientific(sci_raw, commonn)
                        if not display:
                            display = prettify_name(s.get("class_name") or "") or "Unknown"
                        st.write(f"- {display}")

            else:

                high_conf_and_present = (
                    stage == "subspecies_high_conf" and
                    (not country_chosen or (class_name_raw and class_name_raw.lower() in known_names))
                )

                if high_conf_and_present:
                    st.write("We found your bumblebee!")


                    sci_pred, common_pred = lookup_names_for_class(class_name_raw, context_species)
                    display_pred = format_common_with_scientific(sci_pred, common_pred)
                    if not display_pred:

                        display_pred = prettify_name(class_name_raw) or "Unknown"

                    if class_name_raw:
                        st.write(f"**Subspecies:** {display_pred}")
                        st.write(f"**Confidence:** {prob:.2%}")
                        try:
                            show_progress(prob)
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
                                sci_raw = s.get("scientific_name") or s.get("class_name") or ""
                                commonn = s.get("common_name") or ""
                                display = format_common_with_scientific(sci_raw, commonn)
                                if not display:
                                    display = prettify_name(s.get("class_name") or "") or "Unknown"
                                st.write(f"- {display}")
                        else:
                            st.write("_No other known subspecies are listed for the selected country._")

                elif stage in ["subspecies_low_conf", "subspecies_high_conf"]:
                    st.write("This is a bumblebee, but not a subspecies our model can detect.")

                else:
                    st.write(stage or "Unknown stage")
                    try:
                        show_progress(bee_prob)
                    except Exception:
                        pass

                if country_chosen and context_species and not high_conf_and_present:
                    st.markdown("**Here are some common subspecies in your country:**")
                    for s in context_species:
                        sci_raw = s.get("scientific_name") or s.get("class_name") or ""
                        commonn = s.get("common_name") or ""
                        display = format_common_with_scientific(sci_raw, commonn)
                        if not display:
                            display = prettify_name(s.get("class_name") or "") or "Unknown"
                        st.write(f"- {display}")
