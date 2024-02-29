"""
This file contains the common functions used in the Intellect Hire app.
"""
import base64
from pathlib import Path
import os
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
import google.generativeai as genai
import dotenv
import streamlit as st

from utils.prompt_structure import BasicInfoTemplate, ContactInfoTemplate, \
  EducationListInfoTemplate, CompanyListInfoTemplate, AwardListInfoTemplate, \
  CertificationListInfoTemplate, JobMatchingTemplate, SkillInfoTemplate


generation_basic_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048
}

generation_ask_resume_config = {
  "temperature": 1,
  "max_output_tokens": 2048
}

generation_job_matcher_config = {
  "temperature": 0,
  "max_output_tokens": 2048
}

BASIC_PROMPT = """# ROLE : `{role}`
# CONTEXT : `{context}`
# QUESTION : `{question}`
# FEEDBACK : `{feedback}`
# FORMAT : `{format}`"""

ASK_RESUME_PROMPT = """# ROLE : `{role}`
# CONTEXT : `{context}`
# QUESTION : `{question}`
# NOTE : `{note}`
# OUTPUT : """

JOB_MATCH_PROMPT = """# ROLE : `{role}`
# CONTEXT : `{context}`
# JOB DESCRIPTION : `{job_description}`
# FORMAT : `{format}`"""

basic_prompt_template = PromptTemplate.from_template(BASIC_PROMPT)
ask_resume_prompt_template = PromptTemplate.from_template(ASK_RESUME_PROMPT)
job_match_prompt_template = PromptTemplate.from_template(JOB_MATCH_PROMPT)


def check_env_api_key():
    """
    Check if the API key is set in the .env file.
    """
    if os.path.exists(".env"):
        get_gemini_key = dotenv.get_key(".env", "GEMINI_API")
        return get_gemini_key
    return None


def get_basic_info_parser():
    """
    Returns a PydanticOutputParser instance for BasicInfoTemplate
    """
    basic_object_output_parser = PydanticOutputParser(pydantic_object=BasicInfoTemplate)
    return basic_object_output_parser


def get_contact_info_parser():
    """
    Returns a PydanticOutputParser object for parsing contact information.
    """
    contact_object_output_parser = PydanticOutputParser(pydantic_object=ContactInfoTemplate)
    return contact_object_output_parser


def get_education_info_parser():
    """
    Return the PydanticOutputParser object for the EducationListInfoTemplate.
    """
    education_list_object_output_parser = PydanticOutputParser(
        pydantic_object=EducationListInfoTemplate)
    return education_list_object_output_parser


def get_company_info_parser():
    """
    This function returns a PydanticOutputParser object for parsing company list information.
    """
    company_list_object_output_parser = PydanticOutputParser(
        pydantic_object=CompanyListInfoTemplate)
    return company_list_object_output_parser


def get_award_info_parser():
    """
    Return a PydanticOutputParser object for the AwardListInfoTemplate.
    """
    award_list_object_output_parser = PydanticOutputParser(pydantic_object=AwardListInfoTemplate)
    return award_list_object_output_parser


def get_certification_info_parser():
    """
    This function initializes and returns a PydanticOutputParser object for the 
    CertificationListInfoTemplate class.
    """
    cert_list_object_output_parser = PydanticOutputParser(
        pydantic_object=CertificationListInfoTemplate)
    return cert_list_object_output_parser


def get_skill_info_parser():
    """
    Function to get the skill information parser.
    """
    skill_object_output_parser = PydanticOutputParser(pydantic_object=SkillInfoTemplate)
    return skill_object_output_parser


def get_job_matcher_parser():
    """
    Function to get the job matcher parser.
    """
    job_matcher_object_output_parser = PydanticOutputParser(pydantic_object=JobMatchingTemplate)
    return job_matcher_object_output_parser


@st.cache_data(max_entries=10, show_spinner=False, ttl=3600)
def write_file_to_pdf(file_upload_var):
    """
    Write a file to a PDF.
    """
    if not os.path.exists('./temp'):
        os.makedirs('./temp')

    with open('./temp/temp.pdf', mode='wb') as file:
        file.write(file_upload_var.getvalue())


def extract_pages_from_pdf(filepath):
    """
    Extract the pages from a PDF file.
    """
    document = PyPDFLoader(filepath)
    pages = document.load()
    page = '\n'.join([i.page_content for i in pages])
    return page


@st.cache_data(max_entries=10, show_spinner=False, ttl=3600)
def generate_basic_results(api_key, page, flag, _output_parser):
    """
    A function to generate basic results using an API key, page, and output parser.
    It attempts to configure the API key, initialize a generative model, and generate content.
    If an exception occurs, it retries a maximum of 10 times with feedback about the failure.
    The result object is then parsed and returned.
    """
    print(f'Flag : {flag}')
    max_retries = 10
    result_obj = ""
    feedback = "N/A"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_basic_config)
    while max_retries != 0:
        try:
            prompt = basic_prompt_template.format(role="You are an AI Based Resume Parser",
                                            context=page,
                                            question="Extract the below information with respect \
                                                to the context provided",
                                            feedback=feedback,
                                            format=_output_parser.get_format_instructions())
            response = model.generate_content(prompt)
            result_obj = _output_parser.parse_with_prompt(prompt=prompt, completion=response.text)
            break
        except Exception:
            feedback = f"Generate a proper formated JSON as mentioned in \
                instructions {max_retries} out of 10"
            max_retries = max_retries - 1
    result_obj = result_obj.dict()
    return result_obj


@st.cache_data(max_entries=10, show_spinner=False, ttl=3600)
def generate_ask_resume_results(api_key, page, question):
    """
    Generate ask resume results using the specified API key, page, and question.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_ask_resume_config)

    prompt = ask_resume_prompt_template.format(role="You are an AI Based Question & Answer \
                                               Generation",
                                               context=page,
                                               question=question,
                                               note="Generate the answer under 50 words")
    response = model.generate_content(prompt)
    response = response.text
    return response


@st.cache_data(max_entries=10, show_spinner=False, ttl=3600)
def generate_job_match_results(api_key, page, job_description, _output_parser):
    """
    Generate job match results using the specified API key, page, and job description.
    """
    result_obj = ""
    max_retries = 10
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_job_matcher_config)
    while max_retries != 0:
        try:
            prompt = job_match_prompt_template.format(role="You are an AI Based Job Description Matcher",
                                                    context=page,
                                                    job_description=job_description,
                                                    format=_output_parser.get_format_instructions())
            response = model.generate_content(prompt)
            result_obj = _output_parser.parse_with_prompt(prompt=prompt, completion=response.text)
            result_obj = result_obj.dict()
            break
        except Exception:
            max_retries = max_retries - 1
    return result_obj


@st.cache_data
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


@st.cache_data
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
