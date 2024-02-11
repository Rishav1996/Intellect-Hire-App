import streamlit as st
import base64
from pathlib import Path
import os


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid' width='96' style='display: block; margin-left: auto; margin-right: auto;'>".format(
      img_to_bytes(img_path)
    )
    return img_html


st.set_page_config(page_title="Intellect Hires: The AI Talent Curator", 
                   page_icon="./assets/chatbot.png", layout="wide", initial_sidebar_state="collapsed")

GOOGLE_AI_API_KEY = st.sidebar.text_input('GOOGLE Vertex API', placeholder="Enter your API key here")

os.environ.setdefault('GOOGLE_AI_API_KEY', GOOGLE_AI_API_KEY)

icon_col = st.columns([1, 3, 1])
header_col = st.columns([1, 3, 1])
file_upload_col = st.columns([0.25, 1, 0.25])
tabs = st.tabs(['Profile', 'Job Matching', 'Candidate Evaluation'])


with icon_col[1]:
  st.markdown(img_to_html('./assets/chatbot.png'), unsafe_allow_html=True)

with header_col[1]:
  st.markdown("<h2 style='text-align: center;'>Intellect Hires: The AI Talent Curator</h2>", unsafe_allow_html=True)

with file_upload_col[1]:
  file_upload_var = st.file_uploader("Upload your resume here", type=["pdf"])


with tabs[0]:
   st.info("Feature Coming Soon")

with tabs[1]:
   st.info("Feature Coming Soon")

with tabs[2]:
   st.info("Feature Coming Soon")
