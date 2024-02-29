"""
This file contains the prompt structure of the Intellect Hire app.
"""
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class BasicInfoTemplate(BaseModel):
    """
    This class represents the basic information of the candidate.
    """
    name: str = Field(description="Extract the name of the candidate", type='string')
    summary: str = Field(description="Summarize the profile's candidate under 50 words",
                         type='string')
    total_experience: str | None = Field(description="Extract the total experience of the \
                                         candidate from the extracted summary",
                                         type='string')
    date_of_birth: str | None = Field(description="Extract the date of birth of the candidate",
                                      type='string')
    age: str | None = Field(description="(Current date - Extracted date of birth of the candidate) \
                     convert into years & months",
                     type='string')


class ContactInfoTemplate(BaseModel):
    """
    This class represents the contact information of the candidate.
    """
    email: str | None = Field(description="Extract the email of the candidate", type='string')
    address: str | None = Field(description="Extract the address of the candidate", type='string')
    city: str | None = Field(description="Extract the city of the candidate from \
                             the extracted address",
                             type='string')
    state: str | None = Field(description="Extract the state of the candidate from \
                              the extracted address",
                              type='string')
    country: str | None = Field(description="Extract the country of the candidate from the \
                                extracted address",
                                type='string')
    pincode: str | None = Field(description="Extract the pincode of the candidate from the \
                                extracted address",
                                type='string')
    phone_no: int | None = Field(description="Extract the contact details of the candidate",
                                 type='int')


class EducationBaseInfoTemplate(BaseModel):
    """
    This class represents the education information of the candidate.
    """
    institution_name: str | None = Field(description="Extract the instituation name where \
                                         candidate has studied",
                                         type='str')
    type_of_degree: str | None = Field(description="Extract the degree of the candidate from the \
                                       instituation",
                                       type='str')
    passing_date: str | None = Field(description="Extract the passing date of the candidate from \
                                     the instituation",
                                     type='str')
    overall_percentage: str | None = Field(description="Extract the percentage of the candidate \
                                           for the instituation",
                                           type='str')


class EducationListInfoTemplate(BaseModel):
    """
    This class represents the education information of the candidate in a list.
    """
    education_info: List[EducationBaseInfoTemplate] = Field(description="Extract the \
                                                            instituation information",
                                                            type='list')


class CompanyInfoTemplate(BaseModel):
    """
    This class represents the company information of the candidate.
    """
    company_name: str | None = Field(description="Extract the company name where candidate \
                                     has worked",
                                     type='str')
    start_date: str | None = Field(description="Extract the start date for the company",
                                   type='str')
    end_date: str | None = Field(description="Extract the end date for the company", type='str')
    tenure: str | None = Field(description="Calculate the tenure in years & months for the \
                               company",
                               type='str')
    designation: str | None = Field(description="Extract the role of the candidate for the \
                                    company",
                                    type='str')


class CompanyListInfoTemplate(BaseModel):
    """
    This class represents the company information of the candidate in a list.
    """
    company_info: List[CompanyInfoTemplate] = Field(description="Extract the company information",
                                                    type='list')


class AwardInfoTemplate(BaseModel):
    """
    This class represents the award information of the candidate.
    """
    award_name: str | None = Field(description="Extract the award name which candidate has \
                                   achieved",
                                   type='str')
    award_org: str | None = Field(description="Extract the organisation name which have \
                                  given the award",type='str')
    award_year: str | None = Field(description="Extract the year when candidate has \
                                   achieved for the award achieved",
                                   type='str')
    award_amt: str | None = Field(description="Extract the award amount which candidate has \
                                  achieved for the award achieved",
                                  type='str')
    award_desc: str | None = Field(description="Summarize the award which candidate has achieved",
                                   type='str')


class AwardListInfoTemplate(BaseModel):
    """
    This class represents the award information of the candidate in a list.
    """
    award_info: List[AwardInfoTemplate] = Field(description="Extract the award information",
                                                type='list')


class CertificationInfoTemplate(BaseModel):
    """
    This class represents the certification information of the candidate.
    """
    cert_name: str | None = Field(description="Extract the certificate name which candidate has \
                                  gained",
                                  type='str')
    cert_year: str | None = Field(description="Extract the certification year when candidate has \
                                  gained for the certification extracted",
                                  type='str')


class CertificationListInfoTemplate(BaseModel):
    """
    This class represents the certification information of the candidate in a list.
    """
    cert_info: List[CertificationInfoTemplate] = Field(description="Extract the certificate \
                                                       information",
                                                       type='list')


class SkillInfoTemplate(BaseModel):
    """
    This class represents the skill information of the candidate.
    """
    web_ui: list = Field(description="Extract the list of Web UI skills of the candidate has \
                         learned",
                         type='list')
    web_backend: list = Field(description="Extract the list of Web Backend skills of the \
                              candidate has learned",
                              type='list')
    programming_languages: list = Field(description="Extract the list of Programming \
                                        Languages of the candidate has learned",
                                        type='list')
    libraries: list = Field(description="Extract the list of Libraries of the candidate has \
                            learned",
                            type='list')
    databases: list = Field(description="Extract the list of Databases of the candidate has \
                            learned",
                            type='list')
    cloud: list = Field(description="Extract the list of cloud platforms has the candidate \
                        worked upon",
                        type='list')
    others: list = Field(description="Extract the list of other skills / technologies of the \
                         candidate has learned",
                         type='list')


class JobMatchingTemplate(BaseModel):
    """
    This class represents the Job Matching Comparison of the candidate.
    """
    job_matching_score: float = Field(description="Generate a Job Match Score between \
                                      the given resume context & job description",
                                      type='float')
    improvement_area: list = Field(description="Generate the list of improvement area \
                                   for the given resume context with respect to job description",
                                   type='list')
    job_required_skills: list = Field(description="Extract the list of skills provided \
                                      in the job description",
                                      type='list')
