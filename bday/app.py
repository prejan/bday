import streamlit as st
import base64
from pathlib import Path
import mimetypes

st.set_page_config(page_title="Princess Birthday", layout="wide")

# -------- Convert image to base64 URL --------
def img_to_data_url(img_path):
    if not Path(img_path).exists():
        return ""
    mime = mimetypes.guess_type(img_path)[0] or "image/jpeg"
    with open(img_path, "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
        return f"data:{mime};base64,{b64}"

# -------- List of images used in your HTML --------
image_map = {
    "cover.jpeg": img_to_data_url("cover.jpeg"),
    "first_text.jpeg": img_to_data_url("first_text.jpeg"),
    "first_video_sent.jpeg": img_to_data_url("first_video_sent.jpeg"),
    "gift.jpeg": img_to_data_url("gift.jpeg"),
    "hbd.jpeg": img_to_data_url("hbd.jpeg"),
    "annoy.jpeg": img_to_data_url("annoy.jpeg"),
    "sorry.jpeg": img_to_data_url("sorry.jpeg"),
    "us.jpeg": img_to_data_url("us.jpeg"),
}

# -------- Load your HTML --------
html = Path("index.html").read_text(encoding="utf-8")

# -------- Replace file names with base64 in HTML --------
for filename, data_url in image_map.items():
    html = html.replace(filename, data_url)

# -------- Render inside Streamlit --------
st.components.v1.html(html, height=1800, scrolling=True)
