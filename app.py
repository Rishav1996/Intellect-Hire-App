"""
Intellect Hire: The AI Talent Curator
"""
import base64
from pathlib import Path
import os
import streamlit as st


def img_to_bytes(img_path):
    """
    Convert an image file to a base64 encoded string.

    Args:
        img_path (str): The file path of the image to be converted.

    Returns:
        str: The base64 encoded string representation of the image.
    """
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    """
    Convert an image to HTML representation.

    Args:
        img_path (str): The path to the image file.

    Returns:
        str: The HTML representation of the image.
    """
    img_html = f"<img src='data:image/png;base64,{img_to_bytes(img_path)}' class='img-fluid' \
        width='96' style='display: block; margin-left: auto; margin-right: auto;'>"
    return img_html


st.set_page_config(page_title="Intellect Hire: The AI Talent Curator",
                   page_icon="./assets/chatbot.png", layout="wide",
                   initial_sidebar_state="collapsed")

GOOGLE_AI_API_KEY = st.sidebar.text_input('GOOGLE Vertex API',
                                          placeholder="Enter your API key here")

os.environ.setdefault('GOOGLE_AI_API_KEY', GOOGLE_AI_API_KEY)

icon_col = st.columns([1, 3, 1])
header_col = st.columns([1, 3, 1])
file_upload_col = st.columns([1, 5, 1])
tabs_col = st.columns([1, 5, 1])

with tabs_col[1]:
    tabs = st.tabs(['Profile', 'Ask Resume', 'Job Matching', 'Candidate Evaluation'])


with icon_col[1]:
    st.markdown(img_to_html('./assets/chatbot.png'), unsafe_allow_html=True)

with header_col[1]:
    st.markdown("<h2 style='text-align: center;'>Intellect Hire: The AI Talent Curator</h2>",
              unsafe_allow_html=True)

with file_upload_col[1]:
    file_upload_var = st.file_uploader("Upload your resume here", type=["pdf"])


with tabs[0]:
    st.info("Feature Coming Soon")

with tabs[1]:
    st.info("Feature Coming Soon")

with tabs[2]:
    st.info("Feature Coming Soon")

with tabs[3]:
    st.info("Feature Coming Soon")
