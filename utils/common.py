"""
This file contains the common functions used in the Intellect Hire app.
"""
from langchain.output_parsers import PydanticOutputParser
from utils.prompt_structure import BasicInfoTemplate, ContactInfoTemplate, \
  EducationListInfoTemplate, CompanyListInfoTemplate, AwardListInfoTemplate, \
  CertificationListInfoTemplate, SkillInfoTemplate


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
