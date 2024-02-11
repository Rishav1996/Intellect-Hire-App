"""
Intellect Hire: The AI Talent Curator
"""
import base64
import os
from pathlib import Path
import time
import streamlit as st
import pandas as pd

from utils.common import extract_pages_from_pdf, generate_results, get_award_info_parser, get_basic_info_parser, get_certification_info_parser, get_company_info_parser, get_contact_info_parser, get_education_info_parser, get_skill_info_parser


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

GEMINI_AI = st.sidebar.text_input('Google Gemini API', placeholder="Enter your API key here", type="password")

icon_col = st.columns([1, 3, 1])
header_col = st.columns([1, 3, 1])


with icon_col[1]:
	st.markdown(img_to_html('./assets/chatbot.png'), unsafe_allow_html=True)

with header_col[1]:
	st.markdown("<h2 style='text-align: center;'>Intellect Hire: The AI Talent Curator</h2>",
			unsafe_allow_html=True)


if GEMINI_AI:
	file_upload_col = st.columns([1, 5, 1])
	tabs_col = st.columns([1, 5, 1])


	with file_upload_col[1]:
		file_upload_var = st.file_uploader("Upload your resume here", type=["pdf"])

	if file_upload_var:
		with tabs_col[1]:
			tabs = st.tabs(['Profile', 'Ask Resume', 'Job Matching', 'Candidate Evaluation'])

		with tabs[0]:
			tab_profile_col_row_0 = st.columns([1, 1])
			tab_profile_col_row_1 = st.columns([1, 1])

			progress_bar = st.progress(0, 'Extracting pages from PDF...')

			if not os.path.exists('./temp'):
				os.makedirs('./temp')

			with open('./temp/temp.pdf', mode='wb') as file:
				file.write(file_upload_var.getvalue())
			extract_pages = extract_pages_from_pdf('./temp/temp.pdf')

			progress_bar.progress(13, 'Extracting basic information...')

			basic_info_parser = get_basic_info_parser()
			basic_info = generate_results(GEMINI_AI, extract_pages, basic_info_parser)

			progress_bar.progress(25, 'Extracting contact information...')

			contact_info_parser = get_contact_info_parser()
			contact_info = generate_results(GEMINI_AI, extract_pages, contact_info_parser)

			progress_bar.progress(38, 'Extracting education information...')

			education_info_parser = get_education_info_parser()
			education_info = generate_results(GEMINI_AI, extract_pages, education_info_parser)
			education_info = pd.DataFrame(education_info['education_info'])
			education_info.columns = ['Institution', 'Degree', 'Passing Date', 'Overall Percentage']

			progress_bar.progress(50, 'Extracting skill information...')

			skills_info_parser = get_skill_info_parser()
			skill_info = generate_results(GEMINI_AI, extract_pages, skills_info_parser)

			progress_bar.progress(63, 'Extracting company information...')

			company_info_parser = get_company_info_parser()
			company_info = generate_results(GEMINI_AI, extract_pages, company_info_parser)
			company_info = pd.DataFrame(company_info['company_info'])
			company_info.columns = ['Company Name', 'Start Date', 'End Date', 'Tenure', 'Designation']
			
			progress_bar.progress(75, 'Extracting award information...')

			award_info_parser = get_award_info_parser()
			award_info = generate_results(GEMINI_AI, extract_pages, award_info_parser)
			award_info = pd.DataFrame(award_info['award_info'])
			award_info.columns = ['Award Name', 'Organization', 'Year', 'Amount', 'Description']

			progress_bar.progress(88, 'Extracting certification information...')

			certification_info_parser = get_certification_info_parser()
			certification_info = generate_results(GEMINI_AI, extract_pages, certification_info_parser)
			certification_info = pd.DataFrame(certification_info['cert_info'])
			certification_info.columns = ['Certification Name', 'Year']

			progress_bar.progress(100, 'Completed')
			time.sleep(2)
			progress_bar.empty()

			st.markdown(f"""<h3>Basic Information</h3>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Name: </b> {basic_info['name']}</p>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Summary: </b> {basic_info['summary']}</p>""", unsafe_allow_html=True)
			basic_col = st.columns([1, 1, 1])
			basic_col[0].markdown(f"""<p><b>Total Experience: </b> {basic_info['total_experience']}</p>""", unsafe_allow_html=True)
			basic_col[1].markdown(f"""<p><b>Date of Birth: </b> {basic_info['date_of_birth']}</p>""", unsafe_allow_html=True)
			basic_col[2].markdown(f"""<p><b>Age: </b> {basic_info['age']}</p>""", unsafe_allow_html=True)

			st.divider()

			st.markdown(f"""<h3>Contact Information</h3>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Address: </b> {contact_info['address']}</p>""", unsafe_allow_html=True)
			contact_col = st.columns([1, 1, 1, 1])
			contact_col[0].markdown(f"""<p><b>City: </b> {contact_info['city']}</p>""", unsafe_allow_html=True)
			contact_col[1].markdown(f"""<p><b>State: </b> {contact_info['state']}</p>""", unsafe_allow_html=True)
			contact_col[2].markdown(f"""<p><b>Country: </b> {contact_info['country']}</p>""", unsafe_allow_html=True)
			contact_col[3].markdown(f"""<p><b>Pincode: </b> {contact_info['pincode']}</p>""", unsafe_allow_html=True)

			contact_col_phone_email = st.columns([1, 1])
			contact_col_phone_email[0].markdown(f"""<p><b>Email: </b> {contact_info['email']}</p>""", unsafe_allow_html=True)
			contact_col_phone_email[1].markdown(f"""<p><b>Phone No: </b> {contact_info['phone_no']}</p>""", unsafe_allow_html=True)

			st.divider()

			st.markdown(f"""<h3>Skill Information</h3>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Web UI: </b> {', '.join(skill_info['web_ui'])}</p>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Programming Languages: </b> {', '.join(skill_info['programming_languages'])}</p>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Web Backend: </b> {', '.join(skill_info['web_backend'])}</p>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Database: </b> {', '.join(skill_info['databases'])}</p>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Cloud: </b> {', '.join(skill_info['cloud'])}</p>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Libraries: </b> {', '.join(skill_info['libraries'])}</p>""", unsafe_allow_html=True)
			st.markdown(f"""<p><b>Others: </b> {', '.join(skill_info['others'])}</p>""", unsafe_allow_html=True)


			basic_info_tab = st.tabs(['Education Information', 'Company Information', 'Award Information', 'Certification Information'])

			with basic_info_tab[0]:
				st.markdown(f"""<h3>Education Information</h3>""", unsafe_allow_html=True)
				st.table(education_info)
			
			with basic_info_tab[1]:
				st.markdown(f"""<h3>Company Information</h3>""", unsafe_allow_html=True)
				st.table(company_info)
			
			with basic_info_tab[2]:
				st.markdown(f"""<h3>Award Information</h3>""", unsafe_allow_html=True)
				st.table(award_info)
			
			with basic_info_tab[3]:
				st.markdown(f"""<h3>Certification Information</h3>""", unsafe_allow_html=True)
				st.table(certification_info)

		with tabs[1]:
			st.info("Feature Coming Soon")

		with tabs[2]:
			st.info("Feature Coming Soon")

		with tabs[3]:
			st.info("Feature Coming Soon")

else:
	st.error("Please enter your Google Gemini API key")
