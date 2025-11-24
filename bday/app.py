# app.py
import streamlit as st
from pathlib import Path
import mimetypes
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Princess Birthday", layout="centered", initial_sidebar_state="collapsed")

# ---------- helper functions ----------
def file_to_data_url(path: Path):
    if not path.exists():
        return None
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    raw = path.read_bytes()
    return f"data:{mime};base64," + base64.b64encode(raw).decode("utf-8")

def svg_placeholder(text="Image", w=600, h=400):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#ffe9ef"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="28" fill="#ff7ea0">{text}</text></svg>'
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

# ---------- local uploaded image paths (from this chat environment) ----------
# These file paths were uploaded during the conversation and exist here.
paths = {
    "avatar": Path("/mnt/data/cover.jpeg"),
    "playlist1": Path("/mnt/data/first_text.jpeg"),
    "playlist2": Path("/mnt/data/first_video_sent.jpeg"),
    "playlist3": Path("/mnt/data/gift.jpeg"),
    "flip1": Path("/mnt/data/hbd.jpeg"),      # Cute (confirmed)
    "flip2": Path("/mnt/data/annoy.jpeg"),    # Love (confirmed)
    "flip3": Path("/mnt/data/sorry.jpeg"),    # Dream (confirmed)
    "flip4": Path("/mnt/data/us.jpeg"),       # You (confirmed)
}

# ---------- load images into base64 data URLs (fallback to svg if missing) ----------
data = {}
for k, p in paths.items():
    url = file_to_data_url(p)
    data[k] = url if url else svg_placeholder(k)

# ---------- sidebar uploaders (fallback for deployment) ----------
st.sidebar.title("Replace images (optional)")
uploaded = {}
uploaded["avatar"] = st.sidebar.file_uploader("Avatar (circle) - cover.jpeg", type=["png","jpg","jpeg","webp"], key="u_avatar")
uploaded["playlist1"] = st.sidebar.file_uploader("Playlist 1 - first_text.jpeg", type=["png","jpg","jpeg","webp"], key="u_p1")
uploaded["playlist2"] = st.sidebar.file_uploader("Playlist 2 - first_video_sent.jpeg", type=["png","jpg","jpeg","webp"], key="u_p2")
uploaded["playlist3"] = st.sidebar.file_uploader("Playlist 3 - gift.jpeg", type=["png","jpg","jpeg","webp"], key="u_p3")
uploaded["flip1"] = st.sidebar.file_uploader("Flip Cute - hbd.jpeg", type=["png","jpg","jpeg","webp"], key="u_f1")
uploaded["flip2"] = st.sidebar.file_uploader("Flip Love - annoy.jpeg", type=["png","jpg","jpeg","webp"], key="u_f2")
uploaded["flip3"] = st.sidebar.file_uploader("Flip Dream - sorry.jpeg", type=["png","jpg","jpeg","webp"], key="u_f3")
uploaded["flip4"] = st.sidebar.file_uploader("Flip You - us.jpeg", type=["png","jpg","jpeg","webp"], key="u_f4")

for k, f in uploaded.items():
    if f is not None:
        raw = f.read()
        mime = mimetypes.guess_type(f.name)[0] or "image/jpeg"
        data[k] = f"data:{mime};base64," + base64.b64encode(raw).decode("utf-8")

# ---------- HTML template (no f-string, placeholders used) ----------
html_template = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>For My Princess</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
  <style>
    :root{--primary:#ff8fab;--dark-pink:#fb6f92;--bg:#fff2f4;--text:#531022}
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Poppins',sans-serif;background:var(--bg);color:var(--text);padding:20px}
    .wrap{max-width:760px;margin:0 auto;background:linear-gradient(180deg,#fff0f3,#ffeaf0);padding:20px;border-radius:14px;box-shadow:0 18px 50px rgba(83,16,34,0.06)}
    .center{text-align:center}
    .avatar-circle{width:130px;height:130px;border-radius:50%;border:4px solid #ff9ab3;margin:0 auto 10px;background-image:url('IMG_AVATAR');background-size:cover;background-position:center;box-shadow:0 8px 20px rgba(83,16,34,0.06)}
    .title{font-family:'Dancing Script',cursive;font-size:28px;color:var(--dark-pink);margin-top:6px}
    .subtitle{color:#666;margin-bottom:12px}
    .btn{display:inline-block;padding:10px 18px;border-radius:999px;background:linear-gradient(45deg,#ff8fab,#fb6f92);color:#fff;text-decoration:none;font-weight:600;box-shadow:0 8px 18px rgba(251,111,146,0.18)}
    .playlist{margin-top:18px;padding:14px;border-radius:12px;background:linear-gradient(180deg,#fff4f6,#fff0f3)}
    .scroll{display:flex;gap:12px;overflow-x:auto;padding:8px}
    .card{min-width:170px;background:white;padding:10px;border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,0.06)}
    .art{height:90px;border-radius:8px;margin-bottom:8px;background-size:cover;background-position:center}
    .card-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:16px}
    .flip-card{perspective:1000px;height:180px;border-radius:12px}
    .flip-inner{position:relative;width:100%;height:100%;transition:transform .6s;transform-style:preserve-3d}
    .flip-card.flipped .flip-inner{transform:rotateY(180deg)}
    .front,.back{position:absolute;inset:0;border-radius:12px;backface-visibility:hidden;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:0 8px 20px rgba(0,0,0,0.06);background:white}
    .back{transform:rotateY(180deg)}
    .back img{width:100%;height:100%;object-fit:cover;display:block}
    @media(max-width:720px){.card-grid{grid-template-columns:1fr}.avatar-circle{width:110px;height:110px}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="center">
      <div class="avatar-circle" aria-hidden="true"></div>
      <div class="title">Hey Princess! 💕</div>
      <div class="subtitle">I wanted to do something special for you — hope you like it...</div>
      <a class="btn" href="#gallery">Open My Heart 💘</a>
    </div>

    <div class="playlist">
      <div style="text-align:center;font-family:'Dancing Script',cursive;color:var(--dark-pink);font-size:20px;margin-bottom:6px">Our Love Playlist 🎵</div>
      <div style="text-align:center;color:#888;margin-bottom:8px">Songs that remind me of us</div>
      <div class="scroll">
        <div class="card"><div class="art" style="background-image:url('IMG_P1')"></div><strong style="color:var(--dark-pink)">Perfect</strong><div style="color:#888;font-size:.9rem">You're perfect to me 💕</div></div>
        <div class="card"><div class="art" style="background-image:url('IMG_P2')"></div><strong style="color:var(--dark-pink)">All of Me</strong><div style="color:#888;font-size:.9rem">Loves all of you ✨</div></div>
        <div class="card"><div class="art" style="background-image:url('IMG_P3')"></div><strong style="color:var(--dark-pink)">If the World Was Ending</strong><div style="color:#888;font-size:.9rem">I'd still find you 🌍</div></div>
      </div>
    </div>

    <div id="gallery" style="margin-top:18px">
      <div style="text-align:center;font-family:'Dancing Script',cursive;color:var(--dark-pink);font-size:20px;margin-bottom:6px">Messages from My Heart 💌</div>
      <div style="color:#888;text-align:center;margin-bottom:12px">Tap each card to reveal a picture</div>

      <div class="card-grid">
        <div class="flip-card" onclick="this.classList.toggle('flipped')">
          <div class="flip-inner">
            <div class="front">Cute</div>
            <div class="back"><img src="IMG_F1" alt="Cute"></div>
          </div>
        </div>

        <div class="flip-card" onclick="this.classList.toggle('flipped')">
          <div class="flip-inner">
            <div class="front">Love</div>
            <div class="back"><img src="IMG_F2" alt="Love"></div>
          </div>
        </div>

        <div class="flip-card" onclick="this.classList.toggle('flipped')">
          <div class="flip-inner">
            <div class="front">Dream</div>
            <div class="back"><img src="IMG_F3" alt="Dream"></div>
          </div>
        </div>

        <div class="flip-card" onclick="this.classList.toggle('flipped')">
          <div class="flip-inner">
            <div class="front">You</div>
            <div class="back"><img src="IMG_F4" alt="You"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    // keyboard support + accessibility: toggle flip with Enter/Space
    document.querySelectorAll('.flip-card').forEach(function(c){
      c.setAttribute('tabindex','0');
      c.addEventListener('keydown', function(e){
        if(e.key === 'Enter' || e.key === ' ') this.classList.toggle('flipped');
      });
    });
  </script>
</body>
</html>
"""

# ---------- replace placeholders with actual base64 data URLs ----------
html = html_template.replace("IMG_AVATAR", data["avatar"])
html = html.replace("IMG_P1", data["playlist1"])
html = html.replace("IMG_P2", data["playlist2"])
html = html.replace("IMG_P3", data["playlist3"])
html = html.replace("IMG_F1", data["flip1"])
html = html.replace("IMG_F2", data["flip2"])
html = html.replace("IMG_F3", data["flip3"])
html = html.replace("IMG_F4", data["flip4"])

# ---------- render the HTML inside Streamlit ----------
components.html(html, height=1000, scrolling=True)

# ---------- debug expander showing images loaded ----------
with st.expander("Images loaded (debug)"):
    for k in ["avatar","playlist1","playlist2","playlist3","flip1","flip2","flip3","flip4"]:
        st.write(k, "embedded" if data.get(k) else "missing")
    st.write("If an image is missing: either upload it via the sidebar, or place the file in the app folder and redeploy.")
