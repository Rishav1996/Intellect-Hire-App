"""
Intellect Hire: The AI Talent Curator
"""
import streamlit as st

from utils.common import check_env_api_key, img_to_html
from layout.profile import get_layout_profile
from layout.ask_resume import get_layout_ask_resume


st.set_page_config(page_title="Intellect Hire: The AI Talent Curator",
                   page_icon="./assets/chatbot.png", layout="wide",
                   initial_sidebar_state="collapsed")


if not check_env_api_key():
    GEMINI_AI = st.sidebar.text_input('Google Gemini API',
                                      placeholder="Enter your API key here", type="password")
else:
    GEMINI_AI = check_env_api_key()

icon_col = st.columns([1, 3, 1])
header_col = st.columns([1, 3, 1])


with icon_col[1]:
    st.markdown(img_to_html('./assets/chatbot.png'), unsafe_allow_html=True)

with header_col[1]:
    st.markdown("<h2 style='text-align: center;'>Intellect Hire: The AI Talent Curator</h2>",
            unsafe_allow_html=True)


if GEMINI_AI:
    file_upload_col = st.columns([1, 5, 1])
    align_tabs_col = st.columns([1, 5, 1])


    with file_upload_col[1]:
        file_upload_var = st.file_uploader("Upload your resume here", type=["pdf"])

    if file_upload_var:
        with align_tabs_col[1]:
            tabs = st.tabs(['Profile', 'Ask Resume', 'Job Matching', 'Candidate Evaluation'])

        with tabs[0]:
            get_layout_profile(file_upload_var, GEMINI_AI)

        with tabs[1]:
            get_layout_ask_resume(file_upload_var, GEMINI_AI)

        with tabs[2]:
            st.info("Feature Coming Soon")

        with tabs[3]:
            st.info("Feature Coming Soon")

else:
    st.error("Please enter your Google Gemini API key")
