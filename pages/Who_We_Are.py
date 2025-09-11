import base64
import streamlit as st
from pathlib import Path
from utils.ui import apply_global_css

st.set_page_config(page_title="Detect a Bee", layout="wide", initial_sidebar_state="expanded")

BG = Path.cwd() / "assets" / "darkerhex.jpg"
apply_global_css(BG)

lk_path = Path("assets/linkedin.png")
lk_b64 = base64.b64encode(lk_path.read_bytes()).decode("utf-8")
gh_path = Path("assets/github.png")
gh_b64 = base64.b64encode(gh_path.read_bytes()).decode("utf-8")
lele_path = Path("assets/emanuele.png")
lele_b64 = base64.b64encode(lele_path.read_bytes()).decode("utf-8")
katherine_path = Path("assets/katherine.png")
katherine_b64 = base64.b64encode(katherine_path.read_bytes()).decode("utf-8")
rohan_path = Path("assets/rohan.png")
rohan_b64 = base64.b64encode(rohan_path.read_bytes()).decode("utf-8")
thahyra_path = Path("assets/thahyra.png")
thahyra_b64 = base64.b64encode(thahyra_path.read_bytes()).decode("utf-8")

st.markdown(f"""
<div style="text-align: center; line-height: 1.6;">

<!-- Emanuele Torrisi -->
<div style="font-size: 28px; margin-bottom: 40px;">
    <span style="font-weight: bold;">Emanuele Torrisi</span><br>
    <img src="data:image/jpg;base64,{lele_b64}"
     alt="Emanuele Torrisi"
     style="width:100px; height:auto; border-radius:8px; margin: 10px auto; display:block;">
    <span style="font-size: 24px; color: black;">
    I am a self-taught programmer with a background in 3D animation. Recently, I completed the
    Le Wagon Data Science & AI bootcamp, gaining skills in Python, SQL, machine learning, deep
    learning, and data visualization.
    <div style="text-align: center; margin-top: 10px;">
        <a href="https://www.linkedin.com/in/emanuele-torrisi-08a3572a4" target="_blank" style="text-decoration:none;">
            <img src="data:image/png;base64,{lk_b64}" width="28" alt="LinkedIn"
                style="margin-right:10px;" />
        </a>
        <a href="https://github.com/EmanueleTorrisi" target="_blank" style="text-decoration:none;">
            <img src="data:image/png;base64,{gh_b64}" width="28" alt="GitHub" />
        </a>
    </div>
    </span>
</div>
<hr style="border: 0; border-top: 2px solid black; margin: 30px 0;">

<!-- Katherine Stewart -->
<div style="font-size: 28px; margin-bottom: 40px;">
    <span style="font-weight: bold;">Katherine Stewart</span><br>
    <img src="data:image/jpg;base64,{katherine_b64}"
     alt="Katherine Stewart"
     style="width:100px; height:auto; border-radius:8px; margin: 10px auto; display:block;">
    <span style="font-size: 24px; color: black;">
        With a degree in Mathematics and as a Software Engineering graduate from HyperionDev
        in partnership with the University of Manchester, Katherine is excited to be
        delving into the world of Data Science and AI. After completing the bootcamp at
        Le Wagon she is looking to secure a fulltime role in Data Science. Prior to this,
        Katherine enjoyed a long and successful career as a professional violinist.
        <div style="text-align: center; margin-top: 10px;">
            <a href="https://www.linkedin.com/in/katherine-stewart-a3933b354/" target="_blank" style="text-decoration:none;">
                <img src="data:image/png;base64,{lk_b64}" width="28" alt="LinkedIn"
                    style="margin-right:10px;" />
            </a>
            <a href="https://github.com/katherinestewart" target="_blank" style="text-decoration:none;">
                <img src="data:image/png;base64,{gh_b64}" width="28" alt="GitHub" />
            </a>
        </div>
    </span>
</div>
<hr style="border: 0; border-top: 2px solid black; margin: 30px 0;">

<!-- Rohan Raghava Poojary -->
<div style="font-size: 28px; margin-bottom: 40px;">
    <span style="font-weight: bold;">Rohan Raghava Poojary</span><br>
    <img src="data:image/jpg;base64,{rohan_b64}"
     alt="Rohan Raghava Poojary"
     style="width:100px; height:auto; border-radius:8px; margin: 10px auto; display:block;">
    <span style="font-size: 24px; color: black;">
        A theoretical physicist with 10+ years' research experience Rohan has recently caught the
        AI bug and is super excited about how different neural architectures learn specific tasks.
        In his spare time he tries to predict solar wind patterns from IPS data using transformers.
        He has joined the Le Wagon bootcamp for honing industry specific skills and is actively
        looking for data science roles.
        <div style="text-align: center; margin-top: 10px;">
            <a href="https://linkedin.com/in/rohan-r-poojary-b09a25251" target="_blank" style="text-decoration:none;">
                <img src="data:image/png;base64,{lk_b64}" width="28" alt="LinkedIn"
                    style="margin-right:10px;" />
            </a>
            <a href="https://github.com/roninrp" target="_blank" style="text-decoration:none;">
                <img src="data:image/png;base64,{gh_b64}" width="28" alt="GitHub" />
            </a>
        </div>
    </span>
</div>
<hr style="border: 0; border-top: 2px solid black; margin: 30px 0;">

<!-- Thahyra van Heyningen -->
<div style="font-size: 28px; margin-bottom: 40px;">
    <span style="font-weight: bold;">Thahyra van Heyningen</span><br>
    <img src="data:image/jpg;base64,{thahyra_b64}"
     alt="Thahyra van Heyningen"
     style="width:100px; height:auto; border-radius:8px; margin: 10px auto; display:block;">
    <span style="font-size: 24px; color: black;">
        After years in Sales, Thahyra pivoted into Data & AI engineering, where she designs solutions
        that make organizations more efficient and future-proof. What excites her most is using technology
        not just as a tool for efficiency, but as a driver of societal impact, bridging people, processes,
        and data in meaningful ways.
        <div style="text-align: center; margin-top: 10px;">
            <a href="https://www.linkedin.com/in/thahyravh/" target="_blank" style="text-decoration:none;">
                <img src="data:image/png;base64,{lk_b64}" width="28" alt="LinkedIn"
                    style="margin-right:10px;" />
            </a>
            <a href="https://github.com/7CVH" target="_blank" style="text-decoration:none;">
                <img src="data:image/png;base64,{gh_b64}" width="28" alt="GitHub" />
            </a>
        </div>
    </span>
</div>

</div>
""", unsafe_allow_html=True)
