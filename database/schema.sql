-- DDL for INSTAT Survey Platform - PostgreSQL
-- This script creates schemas for three macro-activities: Program, Balance Sheet, and Diagnostic

-- Create Schemas
CREATE SCHEMA IF NOT EXISTS survey_program;
CREATE SCHEMA IF NOT EXISTS survey_balance;
CREATE SCHEMA IF NOT EXISTS survey_diagnostic;

-- Create tables directly for each schema without using a function
-- to avoid escaping issues

-- Tables for survey_program schema
CREATE TABLE IF NOT EXISTS survey_program."Survey" (
    "SurveyID" serial PRIMARY KEY,
    "Title" varchar(255) NOT NULL,
    "Description" text,
    "CreatedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "UpdatedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "Status" varchar(50) DEFAULT 'draft',
    "CreatedBy" varchar(100),
    "ReviewedBy" varchar(100),
    "ApprovedBy" varchar(100),
    "PublishedBy" varchar(100),
    "ReviewDate" timestamp with time zone,
    "ApprovalDate" timestamp with time zone,
    "PublicationDate" timestamp with time zone,
    "Language" varchar(10) DEFAULT 'fr',
    "Version" integer DEFAULT 1,
    "IsTemplate" boolean DEFAULT false
);

CREATE TABLE IF NOT EXISTS survey_program."Section" (
    "SectionID" serial PRIMARY KEY,
    "SurveyID" integer REFERENCES survey_program."Survey"("SurveyID") ON DELETE CASCADE,
    "Title" varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_program."Subsection" (
    "SubsectionID" serial PRIMARY KEY,
    "SectionID" integer REFERENCES survey_program."Section"("SectionID") ON DELETE CASCADE,
    "Title" varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_program."Question" (
    "QuestionID" serial PRIMARY KEY,
    "SectionID" integer REFERENCES survey_program."Section"("SectionID") ON DELETE CASCADE,
    "SubsectionID" integer REFERENCES survey_program."Subsection"("SubsectionID") ON DELETE CASCADE,
    "QuestionText" text NOT NULL,
    "QuestionType" varchar(50)
);

CREATE TABLE IF NOT EXISTS survey_program."AnswerOption" (
    "OptionID" serial PRIMARY KEY,
    "QuestionID" integer REFERENCES survey_program."Question"("QuestionID") ON DELETE CASCADE,
    "OptionText" text NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_program."Response" (
    "ResponseID" serial PRIMARY KEY,
    "SurveyID" integer REFERENCES survey_program."Survey"("SurveyID") ON DELETE CASCADE,
    "RespondentID" integer,
    "SubmittedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS survey_program."ResponseDetail" (
    "ResponseDetailID" serial PRIMARY KEY,
    "ResponseID" integer REFERENCES survey_program."Response"("ResponseID") ON DELETE CASCADE,
    "QuestionID" integer REFERENCES survey_program."Question"("QuestionID") ON DELETE CASCADE,
    "SelectedOptionID" integer REFERENCES survey_program."AnswerOption"("OptionID") ON DELETE SET NULL,
    "AnswerText" text
);

-- Workflow tables (shared across schemas)
CREATE TABLE IF NOT EXISTS public."WorkflowActions" (
    "ActionID" serial PRIMARY KEY,
    "SurveyID" integer NOT NULL,
    "SchemaName" varchar(50) NOT NULL,
    "UserID" varchar(100),
    "ActionType" varchar(50) NOT NULL,
    "FromStatus" varchar(50),
    "ToStatus" varchar(50),
    "Comment" text,
    "Timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

-- Tables for survey_balance schema
CREATE TABLE IF NOT EXISTS survey_balance."Survey" (
    "SurveyID" serial PRIMARY KEY,
    "Title" varchar(255) NOT NULL,
    "Description" text,
    "CreatedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "UpdatedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "Status" varchar(50) DEFAULT 'draft',
    "CreatedBy" varchar(100),
    "ReviewedBy" varchar(100),
    "ApprovedBy" varchar(100),
    "PublishedBy" varchar(100),
    "ReviewDate" timestamp with time zone,
    "ApprovalDate" timestamp with time zone,
    "PublicationDate" timestamp with time zone,
    "Language" varchar(10) DEFAULT 'fr',
    "Version" integer DEFAULT 1,
    "IsTemplate" boolean DEFAULT false
);

CREATE TABLE IF NOT EXISTS survey_balance."Section" (
    "SectionID" serial PRIMARY KEY,
    "SurveyID" integer REFERENCES survey_balance."Survey"("SurveyID") ON DELETE CASCADE,
    "Title" varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_balance."Subsection" (
    "SubsectionID" serial PRIMARY KEY,
    "SectionID" integer REFERENCES survey_balance."Section"("SectionID") ON DELETE CASCADE,
    "Title" varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_balance."Question" (
    "QuestionID" serial PRIMARY KEY,
    "SectionID" integer REFERENCES survey_balance."Section"("SectionID") ON DELETE CASCADE,
    "SubsectionID" integer REFERENCES survey_balance."Subsection"("SubsectionID") ON DELETE CASCADE,
    "QuestionText" text NOT NULL,
    "QuestionType" varchar(50)
);

CREATE TABLE IF NOT EXISTS survey_balance."AnswerOption" (
    "OptionID" serial PRIMARY KEY,
    "QuestionID" integer REFERENCES survey_balance."Question"("QuestionID") ON DELETE CASCADE,
    "OptionText" text NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_balance."Response" (
    "ResponseID" serial PRIMARY KEY,
    "SurveyID" integer REFERENCES survey_balance."Survey"("SurveyID") ON DELETE CASCADE,
    "RespondentID" integer,
    "SubmittedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS survey_balance."ResponseDetail" (
    "ResponseDetailID" serial PRIMARY KEY,
    "ResponseID" integer REFERENCES survey_balance."Response"("ResponseID") ON DELETE CASCADE,
    "QuestionID" integer REFERENCES survey_balance."Question"("QuestionID") ON DELETE CASCADE,
    "SelectedOptionID" integer REFERENCES survey_balance."AnswerOption"("OptionID") ON DELETE SET NULL,
    "AnswerText" text
);

-- Tables for survey_diagnostic schema
CREATE TABLE IF NOT EXISTS survey_diagnostic."Survey" (
    "SurveyID" serial PRIMARY KEY,
    "Title" varchar(255) NOT NULL,
    "Description" text,
    "CreatedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "UpdatedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "Status" varchar(50) DEFAULT 'draft',
    "CreatedBy" varchar(100),
    "ReviewedBy" varchar(100),
    "ApprovedBy" varchar(100),
    "PublishedBy" varchar(100),
    "ReviewDate" timestamp with time zone,
    "ApprovalDate" timestamp with time zone,
    "PublicationDate" timestamp with time zone,
    "Language" varchar(10) DEFAULT 'fr',
    "Version" integer DEFAULT 1,
    "IsTemplate" boolean DEFAULT false
);

CREATE TABLE IF NOT EXISTS survey_diagnostic."Section" (
    "SectionID" serial PRIMARY KEY,
    "SurveyID" integer REFERENCES survey_diagnostic."Survey"("SurveyID") ON DELETE CASCADE,
    "Title" varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_diagnostic."Subsection" (
    "SubsectionID" serial PRIMARY KEY,
    "SectionID" integer REFERENCES survey_diagnostic."Section"("SectionID") ON DELETE CASCADE,
    "Title" varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_diagnostic."Question" (
    "QuestionID" serial PRIMARY KEY,
    "SectionID" integer REFERENCES survey_diagnostic."Section"("SectionID") ON DELETE CASCADE,
    "SubsectionID" integer REFERENCES survey_diagnostic."Subsection"("SubsectionID") ON DELETE CASCADE,
    "QuestionText" text NOT NULL,
    "QuestionType" varchar(50)
);

CREATE TABLE IF NOT EXISTS survey_diagnostic."AnswerOption" (
    "OptionID" serial PRIMARY KEY,
    "QuestionID" integer REFERENCES survey_diagnostic."Question"("QuestionID") ON DELETE CASCADE,
    "OptionText" text NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_diagnostic."Response" (
    "ResponseID" serial PRIMARY KEY,
    "SurveyID" integer REFERENCES survey_diagnostic."Survey"("SurveyID") ON DELETE CASCADE,
    "RespondentID" integer,
    "SubmittedDate" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS survey_diagnostic."ResponseDetail" (
    "ResponseDetailID" serial PRIMARY KEY,
    "ResponseID" integer REFERENCES survey_diagnostic."Response"("ResponseID") ON DELETE CASCADE,
    "QuestionID" integer REFERENCES survey_diagnostic."Question"("QuestionID") ON DELETE CASCADE,
    "SelectedOptionID" integer REFERENCES survey_diagnostic."AnswerOption"("OptionID") ON DELETE SET NULL,
    "AnswerText" text
);


-- Generic tables for users and roles (in public schema)
CREATE TABLE IF NOT EXISTS public."Users" (
    "UserID" serial PRIMARY KEY,
    "Username" varchar(255) UNIQUE NOT NULL,
    "Email" varchar(255) UNIQUE NOT NULL,
    "HashedPassword" varchar(255) NOT NULL,
    "Role" varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS public."Roles" (
    "RoleID" serial PRIMARY KEY,
    "RoleName" varchar(50) UNIQUE NOT NULL
);

INSERT INTO public."Roles" ("RoleName") VALUES ('Admin'), ('Manager'), ('Data Scientist'), ('ReadOnly'), ('Write') ON CONFLICT DO NOTHING;

