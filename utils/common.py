"""
This file contains the common functions used in the Intellect Hire app.
"""
from langchain.output_parsers import PydanticOutputParser
from utils.prompt_structure import BasicInfoTemplate, ContactInfoTemplate, \
  EducationListInfoTemplate, CompanyListInfoTemplate, AwardListInfoTemplate, \
  CertificationListInfoTemplate, SkillInfoTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
import google.generativeai as genai

generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}


basic_prompt = """# ROLE : `{role}`
# CONTEXT : `{context}`
# QUESTION : `{question}`
# FEEDBACK : `{feedback}`
# FORMAT : `{format}`"""

prompt_template = PromptTemplate.from_template(basic_prompt)

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


def extract_pages_from_pdf(filepath):
    """
    Extract the pages from a PDF file.
    """
    document = PyPDFLoader(filepath)
    pages = document.load()
    page = '\n'.join([i.page_content for i in pages])
    return page


def generate_results(api_key, page, output_parser):
    max_retries = 10
    result_obj = ""
    feedback = "N/A"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
    while max_retries != 0:
        try:
            prompt = prompt_template.format(role="You are an AI Based Resume Parser",
                                            context=page,
                                            question="Extract the below information with respect to the context provided",
                                            feedback=feedback,
                                            format=output_parser.get_format_instructions())
            response = model.generate_content(prompt)
            result_obj = output_parser.parse_with_prompt(prompt=prompt, completion=response.text)
            break
        except Exception as exp:
            feedback = f"Generate a proper formated JSON as mentioned in instructions {max_retries} out of 10"
            max_retries = max_retries - 1
    result_obj = result_obj.dict()
    return result_obj
