"""
This file contains all the profile layout for the UI.
"""
import os
import time
import streamlit as st
import pandas as pd

from utils.common import extract_pages_from_pdf, generate_basic_results, get_award_info_parser, \
        get_basic_info_parser, get_certification_info_parser, get_company_info_parser, \
        get_contact_info_parser, get_education_info_parser, get_skill_info_parser, write_file_to_pdf


def get_layout_profile(file_upload_var, GEMINI_AI):
  """
  This function returns the basic information tab.
  """

  progress_bar = st.progress(0, 'Extracting pages from PDF...')

  write_file_to_pdf(file_upload_var)
  EXTRACT_PROFILE_PAGES = extract_pages_from_pdf('./temp/temp.pdf')

  progress_bar.progress(13, 'Extracting basic information...')

  basic_info_parser = get_basic_info_parser()
  basic_info = generate_basic_results(GEMINI_AI, EXTRACT_PROFILE_PAGES, 'BASIC', basic_info_parser)

  progress_bar.progress(25, 'Extracting contact information...')

  contact_info_parser = get_contact_info_parser()
  contact_info = generate_basic_results(GEMINI_AI, EXTRACT_PROFILE_PAGES, 'CONTACT',
                                        contact_info_parser)

  progress_bar.progress(38, 'Extracting education information...')

  education_info_parser = get_education_info_parser()
  education_info = generate_basic_results(GEMINI_AI, EXTRACT_PROFILE_PAGES, 'EDUCATION',
                                          education_info_parser)
  education_info = pd.DataFrame(education_info['education_info'])
  if len(education_info.columns) == 4 and education_info.shape[0] > 0:
      education_info.columns = ['Institution', 'Degree', 'Passing Date',
                                'Overall Percentage']
  else:
      education_info = pd.DataFrame()

  progress_bar.progress(50, 'Extracting skill information...')

  skills_info_parser = get_skill_info_parser()
  skill_info = generate_basic_results(GEMINI_AI, EXTRACT_PROFILE_PAGES, 'SKILLS',
                                      skills_info_parser)

  progress_bar.progress(63, 'Extracting company information...')

  company_info_parser = get_company_info_parser()
  company_info = generate_basic_results(GEMINI_AI, EXTRACT_PROFILE_PAGES, 'COMPANY',
                                        company_info_parser)
  company_info = pd.DataFrame(company_info['company_info'])
  if len(company_info.columns) == 5 and company_info.shape[0] > 0:
      company_info.columns = ['Company Name', 'Start Date', 'End Date', \
                              'Tenure', 'Designation']
  else:
      company_info = pd.DataFrame()

  progress_bar.progress(75, 'Extracting award information...')

  award_info_parser = get_award_info_parser()
  award_info = generate_basic_results(GEMINI_AI, EXTRACT_PROFILE_PAGES, 'AWARD',
                                      award_info_parser)
  award_info = pd.DataFrame(award_info['award_info'])
  if len(award_info.columns) == 5 and award_info.shape[0] > 0:
      award_info.columns = ['Award Name', 'Organization', 'Year', 'Amount',
                            'Description']
  else:
      award_info = pd.DataFrame()

  progress_bar.progress(88, 'Extracting certification information...')

  certification_info_parser = get_certification_info_parser()
  certification_info = generate_basic_results(GEMINI_AI, EXTRACT_PROFILE_PAGES, 'CERTIFICATION',
                                              certification_info_parser)
  certification_info = pd.DataFrame(certification_info['cert_info'])
  if len(certification_info.columns) == 2 and certification_info.shape[0] > 0:
      certification_info.columns = ['Certification Name', 'Year']
  else:
      certification_info = pd.DataFrame()

  progress_bar.progress(100, 'Completed')
  time.sleep(2)
  progress_bar.empty()

  st.markdown("""<h3>Basic Information</h3>""", unsafe_allow_html=True)
  st.markdown(f"""<p><b>Name: </b> {basic_info['name']}</p>""", unsafe_allow_html=True)
  st.markdown(f"""<p><b>Summary: </b> {basic_info['summary']}</p>""",
              unsafe_allow_html=True)
  basic_col = st.columns([1, 1, 1])
  basic_col[0].markdown(f"""<p><b>Total Experience: </b> \
                        {basic_info['total_experience']}</p>""",
                        unsafe_allow_html=True)
  basic_col[1].markdown(f"""<p><b>Date of Birth: </b> \
                        {basic_info['date_of_birth']}</p>""",
                        unsafe_allow_html=True)
  basic_col[2].markdown(f"""<p><b>Age: </b> {basic_info['age']}</p>""",
                        unsafe_allow_html=True)

  st.divider()

  st.markdown("""<h3>Contact Information</h3>""", unsafe_allow_html=True)
  st.markdown(f"""<p><b>Address: </b> {contact_info['address']}</p>""",
              unsafe_allow_html=True)
  contact_col = st.columns([1, 1, 1, 1])
  contact_col[0].markdown(f"""<p><b>City: </b> {contact_info['city']}</p>""",
                          unsafe_allow_html=True)
  contact_col[1].markdown(f"""<p><b>State: </b> {contact_info['state']}</p>""",
                          unsafe_allow_html=True)
  contact_col[2].markdown(f"""<p><b>Country: </b> {contact_info['country']}</p>""",
                          unsafe_allow_html=True)
  contact_col[3].markdown(f"""<p><b>Pincode: </b> {contact_info['pincode']}</p>""",
                          unsafe_allow_html=True)

  contact_col_phone_email = st.columns([1, 1])
  contact_col_phone_email[0].markdown(f"""<p><b>Email: </b> \
                                      {contact_info['email']}</p>""",
                                      unsafe_allow_html=True)
  contact_col_phone_email[1].markdown(f"""<p><b>Phone No: </b> \
                                      {contact_info['phone_no']}</p>""",
                                      unsafe_allow_html=True)

  st.divider()

  st.markdown("""<h3>Skill Information</h3>""", unsafe_allow_html=True)
  st.markdown(f"""<p><b>Web UI: </b> {', '.join(skill_info['web_ui'])}</p>""",
              unsafe_allow_html=True)
  st.markdown(f"""<p><b>Programming Languages: </b> \
              {', '.join(skill_info['programming_languages'])}</p>""",
              unsafe_allow_html=True)
  st.markdown(f"""<p><b>Web Backend: </b> {', '.join(skill_info['web_backend'])}</p>""",
              unsafe_allow_html=True)
  st.markdown(f"""<p><b>Database: </b> {', '.join(skill_info['databases'])}</p>""",
              unsafe_allow_html=True)
  st.markdown(f"""<p><b>Cloud: </b> {', '.join(skill_info['cloud'])}</p>""",
              unsafe_allow_html=True)
  st.markdown(f"""<p><b>Libraries: </b> {', '.join(skill_info['libraries'])}</p>""",
              unsafe_allow_html=True)
  st.markdown(f"""<p><b>Others: </b> {', '.join(skill_info['others'])}</p>""",
              unsafe_allow_html=True)


  basic_info_tab = st.tabs(['Education Information', 'Company Information',
                            'Award Information', 'Certification Information'])

  with basic_info_tab[0]:
      if education_info.shape[0] > 0:
          st.table(education_info)
      else:
          st.warning('No education information found')

  with basic_info_tab[1]:
      if company_info.shape[0] > 0:
          st.table(company_info)
      else:
          st.warning('No company information found')

  with basic_info_tab[2]:
      if award_info.shape[0] > 0:
          st.table(award_info)
      else:
          st.warning('No award information found')

  with basic_info_tab[3]:
      if certification_info.shape[0] > 0:
          st.table(certification_info)
      else:
          st.warning('No certification information found')

