from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random

import streamlit as st
from pathlib import Path
from utils.ui import apply_global_css

st.set_page_config(page_title="Detect a Bee", layout="wide", initial_sidebar_state="expanded")

BG = Path.cwd() / "assets" / "darkerhex.jpg"
apply_global_css(BG)



def show_progress(value: float):
    """
    Render a honey-yellow progress bar.
    Accepts value in range 0.0 - 1.0 (or 0-100); it will normalize appropriately.
    NOTE: This helper does not print the numeric percent below the bar.
    """
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


QUESTIONS = [
    {"q": "Bumblebees belong to which genus?", "options": ["Bombus", "Apis", "Vespa", "Melipona"], "answer": "Bombus"},
    {"q": "Bumblebees are important for:", "options": ["Pollinating many flowers and crops", "Only making honey", "Eating other insects", "Building dams"], "answer": "Pollinating many flowers and crops"},
    {"q": "Why do bumblebees look 'fuzzy'?", "options": ["They have lots of hairs (setae) on their bodies", "They wear pollen coats", "They have scales like butterflies", "They carry feathers"], "answer": "They have lots of hairs (setae) on their bodies"},
    {"q": "Which two colors are most commonly seen on bumblebees?", "options": ["Yellow and black", "Blue and green", "Red and purple", "Pink and white"], "answer": "Yellow and black"},
    {"q": "Approximately how many bumblebee subspecies exist?", "options": ["More than 250", "About 20", "Over 2000", "Fewer than 10"], "answer": "More than 250"},
    {"q": "What does a queen bumblebee usually do in spring?", "options": ["Wake and start a new nest (found a colony)", "Collect honey for winter", "Migrate to Africa", "Spin silk webs"], "answer": "Wake and start a new nest (found a colony)"},
    {"q": "Can bumblebees sting?", "options": ["Yes — they can sting, but are generally not aggressive", "No — they never sting", "Only males can sting", "They sting only underwater"], "answer": "Yes — they can sting, but are generally not aggressive"},
    {"q": "How can bumblebees fly in cool weather?", "options": ["They make heat by vibrating flight muscles (thermoregulation)", "They use solar wings", "They store hot nectar", "They only fly at night"], "answer": "They make heat by vibrating flight muscles (thermoregulation)"},
    {"q": "Which castes are found in a social bumblebee colony?", "options": ["Queens, workers, and males", "Only queens", "Only workers", "Only males"], "answer": "Queens, workers, and males"},
    {"q": "Bumblebees are members of which family?", "options": ["Apidae", "Vespidae", "Formicidae", "Noctuidae"], "answer": "Apidae"},
    {"q": "Bumblebees collect what from flowers?", "options": ["Nectar and pollen", "Leaves and twigs", "Stone and sand", "Fish"], "answer": "Nectar and pollen"},
    {"q": "Which crop benefits from ‘buzz pollination’ by bumblebees?", "options": ["Tomatoes", "Wheat", "Soybeans", "Rice"], "answer": "Tomatoes"},
    {"q": "Where are bumblebee nests often found?", "options": ["In holes in the ground or old rodent nests", "High on cliff faces", "Floating on water", "Inside human refrigerators"], "answer": "In holes in the ground or old rodent nests"},
    {"q": "Do bumblebees store large amounts of honey like honeybees?", "options": ["No — they store only small food reserves", "Yes — they build huge honey stores", "They store only pollen, never nectar", "They make syrup instead"], "answer": "No — they store only small food reserves"},
    {"q": "What special pollination method do bumblebees use to release pollen from some flowers?", "options": ["Buzz pollination (sonication)", "Carrying the whole flower", "Using their feet to comb pollen", "Digging under the flower"], "answer": "Buzz pollination (sonication)"},
]

TOTAL = len(QUESTIONS)


def _init_state():
    if "bumbleeq_index" not in st.session_state:
        st.session_state.bumbleeq_index = 0
    if "bumbleeq_score" not in st.session_state:
        st.session_state.bumbleeq_score = 0
    if "bumbleeq_finished" not in st.session_state:
        st.session_state.bumbleeq_finished = False
    if "bumbleeq_reset_msg" not in st.session_state:
        st.session_state.bumbleeq_reset_msg = ""
    if "bumbleeq_cert_bytes" not in st.session_state:
        st.session_state.bumbleeq_cert_bytes = None
    if "bumbleeq_name" not in st.session_state:
        st.session_state.bumbleeq_name = ""
    if "bumbleeq_confetti_shown" not in st.session_state:
        st.session_state.bumbleeq_confetti_shown = False
    if "bumbleeq_shuffled_opts" not in st.session_state:
        st.session_state.bumbleeq_shuffled_opts = None

_init_state()


def init_shuffled_options(force=False):
    if st.session_state.bumbleeq_shuffled_opts is not None and not force:
        return
    shuffled = []
    for q in QUESTIONS:
        ans = q["answer"]
        opts = list(q.get("options", []))
        if ans not in opts:
            opts.append(ans)
        unique_opts = []
        for o in opts:
            if o not in unique_opts:
                unique_opts.append(o)
        if len(unique_opts) > 4:
            unique_opts = unique_opts[:4]
        random.shuffle(unique_opts)
        if ans not in unique_opts:
            replace_idx = random.randrange(len(unique_opts))
            unique_opts[replace_idx] = ans
        shuffled.append(unique_opts)
    st.session_state.bumbleeq_shuffled_opts = shuffled

init_shuffled_options(force=False)


def measure_text(draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        try:
            return draw.textsize(text, font=font)
        except Exception:
            try:
                return font.getsize(text)
            except Exception:
                mask = font.getmask(text)
                return mask.size

def _show_confetti():
    html = """
    <canvas id="confetti-canvas" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:999999;"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    (function() {
      var canvas = document.getElementById('confetti-canvas');
      var myConfetti = confetti.create(canvas, { resize: true, useWorker: true });
      var duration = 4000;
      var end = Date.now() + duration;
      (function frame() {
        myConfetti({ particleCount: 6, angle: 60, spread: 55, origin: { x: 0 } });
        myConfetti({ particleCount: 6, angle: 120, spread: 55, origin: { x: 1 } });
        if (Date.now() < end) {
          requestAnimationFrame(frame);
        } else {
          try { canvas.remove(); } catch(e) {}
        }
      })();
    })();
    </script>
    """
    st.components.v1.html(html, height=150, scrolling=False)


def generate_certificate(name: str) -> bytes:
    W, H = 1200, 800
    img = Image.new("RGB", (W, H), color=("yellow"))
    draw = ImageDraw.Draw(img)


    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 50)
        font_body = ImageFont.truetype("DejaVuSans.ttf", 40)
        font_name = ImageFont.truetype("DejaVuSans-Bold.ttf", 80)
        font_date = ImageFont.truetype("DejaVuSans.ttf", 28)
        font_desc = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except Exception:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_name = ImageFont.load_default()
        font_date = ImageFont.load_default()
        font_desc = ImageFont.load_default()


    title_text = "BumbleeQuiz Certificate of Completion"
    w_title, h_title = measure_text(draw, title_text, font_title)
    draw.text(((W - w_title) / 2, 160), title_text, fill="#000000", font=font_title)


    subtitle = "This certifies that"
    w_sub, h_sub = measure_text(draw, subtitle, font_desc)
    draw.text(((W - w_sub) / 2, 310), subtitle, fill="#5D4037", font=font_desc)


    w_name, h_name = measure_text(draw, name, font_name)
    draw.text(((W - w_name) / 2, 360), name, fill=
              "#000000", font=font_name)


    footer = f"Is an official BeeTector"
    w_foot, h_foot = measure_text(draw, footer, font_body)
    draw.text(((W - w_foot) / 2, 480), footer, fill="#5D4037", font=font_body)


    date_text = datetime.now().strftime("%B %d, %Y")
    w_date, h_date = measure_text(draw, date_text, font_date)
    draw.text(((W - w_date) / 2, 570), date_text, fill="#5D4037", font=font_date)


    border_thickness = 12
    for i in range(border_thickness):
        draw.rectangle([i, i, W - i - 1, H - i - 1], outline="#000000")


    for x, y in [(80, 80), (W-120, 80), (80, H-120), (W-120, H-120)]:
        draw.ellipse([x, y, x+20, y+20], fill="#000000", outline="#000000")


    buf = BytesIO()
    img.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    return buf.getvalue()


st.title("BumbleeQuiz — Easy Bumble Bee Quiz")
st.write("Click an answer to select it. Any mistake resets your progress to 0 and restarts the quiz.")

progress_value = min(max(st.session_state.bumbleeq_score / TOTAL, 0.0), 1.0)
show_progress(progress_value)
st.write(f"Score: **{st.session_state.bumbleeq_score}** / {TOTAL}")

if st.session_state.bumbleeq_reset_msg:
    st.warning(st.session_state.bumbleeq_reset_msg)
    st.session_state.bumbleeq_reset_msg = ""


if st.session_state.bumbleeq_score >= TOTAL or st.session_state.bumbleeq_finished:
    st.session_state.bumbleeq_finished = True

    if not st.session_state.bumbleeq_confetti_shown:
        try:
            _show_confetti()
        except Exception:
            st.balloons()
        st.session_state.bumbleeq_confetti_shown = True

    st.subheader("Perfect! You answered all questions correctly.")
    st.write("Enter your name to generate your completion certificate (JPG).")

    name = st.text_input("Insert your name:", value=st.session_state.bumbleeq_name, key="bumbleeq_name_input")
    if st.button("Confirm and Generate Certificate"):
        if not name.strip():
            st.error("Name cannot be empty.")
        else:
            st.session_state.bumbleeq_name = name.strip()
            st.session_state.bumbleeq_cert_bytes = generate_certificate(name.strip())

    if st.session_state.bumbleeq_cert_bytes:
        st.success("Certificate generated.")
        st.image(st.session_state.bumbleeq_cert_bytes, caption="Certificate preview", use_container_width=True)
        st.download_button(
            label="Download certificate (JPG)",
            data=st.session_state.bumbleeq_cert_bytes,
            file_name=f"bumbleequiz_certificate_{st.session_state.bumbleeq_name.replace(' ', '_')}.jpg",
            mime="image/jpeg",
        )

    if st.button("Restart Quiz"):
        st.session_state.bumbleeq_index = 0
        st.session_state.bumbleeq_score = 0
        st.session_state.bumbleeq_finished = False
        st.session_state.bumbleeq_cert_bytes = None
        st.session_state.bumbleeq_name = ""
        st.session_state.bumbleeq_confetti_shown = False
        init_shuffled_options(force=True)


else:
    idx = st.session_state.bumbleeq_index
    if idx < 0 or idx >= TOTAL:
        st.session_state.bumbleeq_index = 0
        idx = 0

    if st.session_state.bumbleeq_shuffled_opts is None:
        init_shuffled_options(force=True)

    q_obj = QUESTIONS[idx]
    opts = st.session_state.bumbleeq_shuffled_opts[idx]
    if not opts or not isinstance(opts, list):
        opts = list(q_obj.get("options", []))
        random.shuffle(opts)
        st.session_state.bumbleeq_shuffled_opts[idx] = opts

    st.subheader(f"Question {idx + 1} of {TOTAL}")
    st.write(q_obj["q"])

    for i, opt in enumerate(opts):
        key = f"bumbleeq_opt_{idx}_{i}"
        if st.button(opt, key=key):
            if opt == q_obj["answer"]:
                st.session_state.bumbleeq_score += 1
                st.session_state.bumbleeq_index += 1
                if st.session_state.bumbleeq_score >= TOTAL:
                    st.session_state.bumbleeq_finished = True
            else:
                st.session_state.bumbleeq_score = 0
                st.session_state.bumbleeq_index = 0
                st.session_state.bumbleeq_reset_msg = "Incorrect answer — progress reset to 0. Quiz restarted."
                st.session_state.bumbleeq_cert_bytes = None
                st.session_state.bumbleeq_name = ""
                st.session_state.bumbleeq_confetti_shown = False
                init_shuffled_options(force=True)
