"""
This file contains all the Job Matching layout for the UI.
"""
import streamlit as st

from utils.common import extract_pages_from_pdf, generate_job_match_results, \
    get_job_matcher_parser, write_file_to_pdf


def get_layout_job_matcher(file_upload_var, gemini_ai_api_key):
    """
    This function returns the Job Matching tab.
    """
    job_description = st.text_area("Enter your job description", height=200)
    job_description = job_description[:2000]
    job_submit_button = st.button("Analyze", type='primary')
    if job_submit_button:
        with st.spinner("Analyzing..."):
            write_file_to_pdf(file_upload_var)
            extract_resume_pages = extract_pages_from_pdf('./temp/temp.pdf')
            job_match_template = get_job_matcher_parser()
            output = generate_job_match_results(gemini_ai_api_key, extract_resume_pages,
                                                job_description, job_match_template)
            st.markdown(f"<h6>Job Matching Score : </h6> {output['job_matching_score'] * 100} %",
                        unsafe_allow_html=True)
            st.markdown(f"<br><h6>Improvement Areas : </h6>\
                        {'<br>'.join(['- '+i for i in output['improvement_area']])}",
                        unsafe_allow_html=True)
            st.markdown(f"<br><h6>Job Required Skills : </h6>\
                        {'<br>'.join(['- '+i for i in output['job_required_skills']])}",
                        unsafe_allow_html=True)
