"""
This file contains all the ask resume tab layout for the UI.
"""
import os
import time
import streamlit as st
import pandas as pd
from utils.common import extract_pages_from_pdf, generate_ask_resume_results


def get_layout_ask_resume(file_upload_var, GEMINI_AI):
  """
  This function returns the ask resume tab.
  """

  question = st.text_input("Ask your resume ?", placeholder="Enter your query here")
  if question:
    progress_bar = st.progress(0, 'Generating the answer ...')

    if not os.path.exists('./temp'):
        os.makedirs('./temp')

    with open('./temp/temp.pdf', mode='wb') as file:
        file.write(file_upload_var.getvalue())
    EXTRACT_PAGES = extract_pages_from_pdf('./temp/temp.pdf')

    output = generate_ask_resume_results(GEMINI_AI, EXTRACT_PAGES, question)
    progress_bar.progress(100, 'Completed')
    time.sleep(1)
    progress_bar.empty()

    st.markdown("<h5>Results</h5>", unsafe_allow_html=True)
    st.markdown(output, unsafe_allow_html=True)
  else:
    st.info("Please enter the query")
