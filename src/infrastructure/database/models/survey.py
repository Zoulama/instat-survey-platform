"""
Survey models for the platform
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from ..base import Base


class Survey(Base):
    """Survey model for all schemas"""
    __tablename__ = "Survey"
    
    SurveyID = Column(Integer, primary_key=True, index=True)
    Title = Column(String(255), nullable=False)
    Description = Column(Text)
    CreatedDate = Column(DateTime, default=datetime.utcnow)
    UpdatedDate = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    Status = Column(String(50), default="draft")
    CreatedBy = Column(String(100))
    ReviewedBy = Column(String(100))
    ApprovedBy = Column(String(100))
    PublishedBy = Column(String(100))
    ReviewDate = Column(DateTime)
    ApprovalDate = Column(DateTime)
    PublicationDate = Column(DateTime)
    Language = Column(String(10), default="fr")
    Version = Column(Integer, default=1)
    IsTemplate = Column(Boolean, default=False)
    
    # Relationships
    sections = relationship("Section", back_populates="survey", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="survey", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'SurveyID': self.SurveyID,
            'Title': self.Title,
            'Description': self.Description,
            'CreatedDate': self.CreatedDate,
            'UpdatedDate': self.UpdatedDate,
            'Status': self.Status,
            'CreatedBy': self.CreatedBy,
            'ReviewedBy': self.ReviewedBy,
            'ApprovedBy': self.ApprovedBy,
            'PublishedBy': self.PublishedBy,
            'ReviewDate': self.ReviewDate,
            'ApprovalDate': self.ApprovalDate,
            'PublicationDate': self.PublicationDate,
            'Language': self.Language,
            'Version': self.Version,
            'IsTemplate': self.IsTemplate
        }


class Section(Base):
    """Section model for all schemas"""
    __tablename__ = "Section"
    
    SectionID = Column(Integer, primary_key=True, index=True)
    SurveyID = Column(Integer, ForeignKey("Survey.SurveyID", ondelete="CASCADE"))
    Title = Column(String(255), nullable=False)
    
    # Relationships
    survey = relationship("Survey", back_populates="sections")
    subsections = relationship("Subsection", back_populates="section", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="section", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'SectionID': self.SectionID,
            'SurveyID': self.SurveyID,
            'Title': self.Title
        }


class Subsection(Base):
    """Subsection model for all schemas"""
    __tablename__ = "Subsection"
    
    SubsectionID = Column(Integer, primary_key=True, index=True)
    SectionID = Column(Integer, ForeignKey("Section.SectionID", ondelete="CASCADE"))
    Title = Column(String(255), nullable=False)
    
    # Relationships
    section = relationship("Section", back_populates="subsections")
    questions = relationship("Question", back_populates="subsection", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'SubsectionID': self.SubsectionID,
            'SectionID': self.SectionID,
            'Title': self.Title
        }


class Question(Base):
    """Question model for all schemas"""
    __tablename__ = "Question"
    
    QuestionID = Column(Integer, primary_key=True, index=True)
    SectionID = Column(Integer, ForeignKey("Section.SectionID", ondelete="CASCADE"))
    SubsectionID = Column(Integer, ForeignKey("Subsection.SubsectionID", ondelete="CASCADE"), nullable=True)
    QuestionText = Column(Text, nullable=False)
    QuestionType = Column(String(50))
    
    # Relationships
    section = relationship("Section", back_populates="questions")
    subsection = relationship("Subsection", back_populates="questions")
    answer_options = relationship("AnswerOption", back_populates="question", cascade="all, delete-orphan")
    response_details = relationship("ResponseDetail", back_populates="question", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'QuestionID': self.QuestionID,
            'SectionID': self.SectionID,
            'SubsectionID': self.SubsectionID,
            'QuestionText': self.QuestionText,
            'QuestionType': self.QuestionType
        }


class AnswerOption(Base):
    """Answer option model for all schemas"""
    __tablename__ = "AnswerOption"
    
    OptionID = Column(Integer, primary_key=True, index=True)
    QuestionID = Column(Integer, ForeignKey("Question.QuestionID", ondelete="CASCADE"))
    OptionText = Column(Text, nullable=False)
    
    # Relationships
    question = relationship("Question", back_populates="answer_options")
    response_details = relationship("ResponseDetail", back_populates="selected_option")
    
    def to_dict(self):
        return {
            'OptionID': self.OptionID,
            'QuestionID': self.QuestionID,
            'OptionText': self.OptionText
        }


class Response(Base):
    """Response model for all schemas"""
    __tablename__ = "Response"
    
    ResponseID = Column(Integer, primary_key=True, index=True)
    SurveyID = Column(Integer, ForeignKey("Survey.SurveyID", ondelete="CASCADE"))
    RespondentID = Column(Integer)
    SubmittedDate = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    survey = relationship("Survey", back_populates="responses")
    response_details = relationship("ResponseDetail", back_populates="response", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'ResponseID': self.ResponseID,
            'SurveyID': self.SurveyID,
            'RespondentID': self.RespondentID,
            'SubmittedDate': self.SubmittedDate
        }


class ResponseDetail(Base):
    """Response detail model for all schemas"""
    __tablename__ = "ResponseDetail"
    
    ResponseDetailID = Column(Integer, primary_key=True, index=True)
    ResponseID = Column(Integer, ForeignKey("Response.ResponseID", ondelete="CASCADE"))
    QuestionID = Column(Integer, ForeignKey("Question.QuestionID", ondelete="CASCADE"))
    SelectedOptionID = Column(Integer, ForeignKey("AnswerOption.OptionID", ondelete="SET NULL"), nullable=True)
    AnswerText = Column(Text)
    
    # Relationships
    response = relationship("Response", back_populates="response_details")
    question = relationship("Question", back_populates="response_details")
    selected_option = relationship("AnswerOption", back_populates="response_details")
    
    def to_dict(self):
        return {
            'ResponseDetailID': self.ResponseDetailID,
            'ResponseID': self.ResponseID,
            'QuestionID': self.QuestionID,
            'SelectedOptionID': self.SelectedOptionID,
            'AnswerText': self.AnswerText
        }
