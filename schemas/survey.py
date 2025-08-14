"""
Pydantic schemas for Survey, Section, Question, etc.
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


# Schema for AnswerOption
class AnswerOptionBase(BaseModel):
    OptionText: str


class AnswerOptionCreate(AnswerOptionBase):
    pass


class AnswerOption(AnswerOptionBase):
    OptionID: int
    QuestionID: int

    class Config:
        orm_mode = True


# Schema for Question
class QuestionBase(BaseModel):
    QuestionText: str
    QuestionType: str


class QuestionCreate(QuestionBase):
    AnswerOptions: Optional[List[AnswerOptionCreate]] = []


class Question(QuestionBase):
    QuestionID: int
    SectionID: int
    SubsectionID: Optional[int] = None
    AnswerOptions: List[AnswerOption] = []

    class Config:
        orm_mode = True


# Schema for Subsection
class SubsectionBase(BaseModel):
    Title: str


class SubsectionCreate(SubsectionBase):
    Questions: Optional[List[QuestionCreate]] = []


class Subsection(SubsectionBase):
    SubsectionID: int
    SectionID: int
    Questions: List[Question] = []

    class Config:
        orm_mode = True


# Schema for Section
class SectionBase(BaseModel):
    Title: str


class SectionCreate(SectionBase):
    Subsections: Optional[List[SubsectionCreate]] = []
    Questions: Optional[List[QuestionCreate]] = []


class Section(SectionBase):
    SectionID: int
    SurveyID: int
    Subsections: List[Subsection] = []
    Questions: List[Question] = []

    class Config:
        orm_mode = True


# Schema for Survey
class SurveyBase(BaseModel):
    Title: str
    Description: Optional[str] = None
    Status: Optional[str] = "draft"
    Language: Optional[str] = "fr"
    IsTemplate: Optional[bool] = False


class SurveyCreate(SurveyBase):
    Sections: List[SectionCreate] = []
    CreatedBy: Optional[str] = None


class SurveyUpdate(BaseModel):
    Title: Optional[str] = None
    Description: Optional[str] = None
    Status: Optional[str] = None
    Language: Optional[str] = None
    IsTemplate: Optional[bool] = None
    ReviewedBy: Optional[str] = None
    ApprovedBy: Optional[str] = None
    PublishedBy: Optional[str] = None


class Survey(SurveyBase):
    SurveyID: int
    CreatedDate: datetime
    UpdatedDate: Optional[datetime] = None
    CreatedBy: Optional[str] = None
    ReviewedBy: Optional[str] = None
    ApprovedBy: Optional[str] = None
    PublishedBy: Optional[str] = None
    ReviewDate: Optional[datetime] = None
    ApprovalDate: Optional[datetime] = None
    PublicationDate: Optional[datetime] = None
    Version: Optional[int] = 1
    Sections: List[Section] = []

    class Config:
        orm_mode = True
