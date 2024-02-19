"""
This file contains all the ask resume tab layout for the UI.
"""
import json
import streamlit as st
from utils.common import extract_pages_from_pdf, generate_ask_resume_results, write_file_to_pdf


def get_layout_ask_resume(file_upload_var, GEMINI_AI):
  """
  This function returns the ask resume tab.
  """
  question = st.text_input("Ask your resume ?")

  if "messages" not in st.session_state:
      st.session_state.messages = []

  button_col = st.columns([1, 2, 3])

  button_col[0].download_button("Download Chat", json.dumps(st.session_state.messages), "chat.json", "json", type="primary")
  button_col[1].button("Clear Chat", on_click=lambda: st.session_state.messages.clear())

  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  if question:
    st.session_state.messages.append({"role": "human", "content": question})
    with st.chat_message("human"):
      st.write(question)

    with st.chat_message("ai"):
      with st.spinner("Generating the answer ...."):
        write_file_to_pdf(file_upload_var)
        EXTRACT_RESUME_PAGES = extract_pages_from_pdf('./temp/temp.pdf')
        output = generate_ask_resume_results(GEMINI_AI, EXTRACT_RESUME_PAGES, question)
        st.session_state.messages.append({"role": "ai", "content": output})
        st.markdown(output)
