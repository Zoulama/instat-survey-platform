--
-- PostgreSQL database dump
--

\restrict JqrhyTWnYwfAexGLQxgOIhjOegtawhTkvGfUEzPtxw9kxWWkNcotY6Ydq9V1nim

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: AnswerOption; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."AnswerOption" (
    "OptionID" integer NOT NULL,
    "QuestionID" integer,
    "OptionText" text NOT NULL
);


ALTER TABLE public."AnswerOption" OWNER TO postgres;

--
-- Name: AnswerOption_OptionID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."AnswerOption_OptionID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."AnswerOption_OptionID_seq" OWNER TO postgres;

--
-- Name: AnswerOption_OptionID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."AnswerOption_OptionID_seq" OWNED BY public."AnswerOption"."OptionID";


--
-- Name: AuditLog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."AuditLog" (
    "LogID" integer NOT NULL,
    "UserID" integer,
    "Username" character varying(255),
    "Action" character varying(100) NOT NULL,
    "Resource" character varying(100),
    "ResourceID" character varying(100),
    "Details" json,
    "IPAddress" character varying(45),
    "UserAgent" character varying(500),
    "Success" boolean,
    "ErrorMessage" text,
    "Timestamp" timestamp without time zone
);


ALTER TABLE public."AuditLog" OWNER TO postgres;

--
-- Name: AuditLog_LogID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."AuditLog_LogID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."AuditLog_LogID_seq" OWNER TO postgres;

--
-- Name: AuditLog_LogID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."AuditLog_LogID_seq" OWNED BY public."AuditLog"."LogID";


--
-- Name: DataExports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."DataExports" (
    "ExportID" integer NOT NULL,
    "SurveyID" integer NOT NULL,
    "ExportFormat" character varying(20) NOT NULL
);


ALTER TABLE public."DataExports" OWNER TO postgres;

--
-- Name: DataExports_ExportID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."DataExports_ExportID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."DataExports_ExportID_seq" OWNER TO postgres;

--
-- Name: DataExports_ExportID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."DataExports_ExportID_seq" OWNED BY public."DataExports"."ExportID";


--
-- Name: INSTATQuestions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."INSTATQuestions" (
    "QuestionID" integer NOT NULL,
    "SurveyID" integer NOT NULL,
    "SectionID" integer,
    "SubsectionID" integer,
    "QuestionText" text NOT NULL,
    "QuestionType" character varying(50) NOT NULL,
    "IsRequired" boolean,
    "IndicatorCode" character varying(100),
    "DataSource" character varying(255),
    "CollectionMethod" character varying(100),
    "QualityRequirements" json,
    "ValidationRules" json,
    "DependsOnQuestion" integer,
    "QuestionTextEN" text,
    "QuestionTextFR" text,
    "Tags" json,
    "Priority" character varying(20)
);


ALTER TABLE public."INSTATQuestions" OWNER TO postgres;

--
-- Name: INSTATQuestions_QuestionID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."INSTATQuestions_QuestionID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."INSTATQuestions_QuestionID_seq" OWNER TO postgres;

--
-- Name: INSTATQuestions_QuestionID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."INSTATQuestions_QuestionID_seq" OWNED BY public."INSTATQuestions"."QuestionID";


--
-- Name: INSTATSurveys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."INSTATSurveys" (
    "SurveyID" integer NOT NULL,
    "Title" character varying(255) NOT NULL,
    "Description" text,
    "Domain" character varying(50) NOT NULL,
    "Category" character varying(50) NOT NULL,
    "CreatedDate" timestamp without time zone,
    "UpdatedDate" timestamp without time zone,
    "Status" character varying(50),
    "FiscalYear" integer,
    "ReportingCycle" character varying(50),
    "CreatedBy" character varying(100),
    "ReviewedBy" character varying(100),
    "ApprovedBy" character varying(100),
    "PublishedBy" character varying(100),
    "ImplementingUnit" character varying(100),
    "ReviewDate" timestamp without time zone,
    "ApprovalDate" timestamp without time zone,
    "PublicationDate" timestamp without time zone,
    "Language" character varying(10),
    "Version" character varying(20),
    "IsTemplate" boolean,
    "TargetAudience" json,
    "GeographicScope" json,
    "ComplianceFramework" json,
    "InternationalStandards" json,
    "RequiredSkills" json,
    "BudgetCategory" character varying(100),
    "EstimatedDuration" integer,
    "DomainSpecificFields" json
);


ALTER TABLE public."INSTATSurveys" OWNER TO postgres;

--
-- Name: INSTATSurveys_SurveyID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."INSTATSurveys_SurveyID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."INSTATSurveys_SurveyID_seq" OWNER TO postgres;

--
-- Name: INSTATSurveys_SurveyID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."INSTATSurveys_SurveyID_seq" OWNED BY public."INSTATSurveys"."SurveyID";


--
-- Name: ParsingResult; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ParsingResult" (
    "ResultID" integer NOT NULL,
    "FileName" character varying(255) NOT NULL,
    "ParsedData" json,
    "ValidationIssues" json,
    "Success" boolean,
    "ErrorMessage" text,
    "Timestamp" timestamp without time zone
);


ALTER TABLE public."ParsingResult" OWNER TO postgres;

--
-- Name: ParsingResult_ResultID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."ParsingResult_ResultID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ParsingResult_ResultID_seq" OWNER TO postgres;

--
-- Name: ParsingResult_ResultID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."ParsingResult_ResultID_seq" OWNED BY public."ParsingResult"."ResultID";


--
-- Name: ParsingStatistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ParsingStatistics" (
    "StatID" integer NOT NULL,
    "TotalFiles" integer,
    "SuccessfulParses" integer,
    "FailedParses" integer,
    "AverageParseTime" double precision,
    "LastUpdated" timestamp without time zone
);


ALTER TABLE public."ParsingStatistics" OWNER TO postgres;

--
-- Name: ParsingStatistics_StatID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."ParsingStatistics_StatID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ParsingStatistics_StatID_seq" OWNER TO postgres;

--
-- Name: ParsingStatistics_StatID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."ParsingStatistics_StatID_seq" OWNED BY public."ParsingStatistics"."StatID";


--
-- Name: Question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Question" (
    "QuestionID" integer NOT NULL,
    "SectionID" integer,
    "SubsectionID" integer,
    "QuestionText" text NOT NULL,
    "QuestionType" character varying(50)
);


ALTER TABLE public."Question" OWNER TO postgres;

--
-- Name: Question_QuestionID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Question_QuestionID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Question_QuestionID_seq" OWNER TO postgres;

--
-- Name: Question_QuestionID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Question_QuestionID_seq" OWNED BY public."Question"."QuestionID";


--
-- Name: Response; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Response" (
    "ResponseID" integer NOT NULL,
    "SurveyID" integer,
    "RespondentID" integer,
    "SubmittedDate" timestamp without time zone
);


ALTER TABLE public."Response" OWNER TO postgres;

--
-- Name: ResponseDetail; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ResponseDetail" (
    "ResponseDetailID" integer NOT NULL,
    "ResponseID" integer,
    "QuestionID" integer,
    "SelectedOptionID" integer,
    "AnswerText" text
);


ALTER TABLE public."ResponseDetail" OWNER TO postgres;

--
-- Name: ResponseDetail_ResponseDetailID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."ResponseDetail_ResponseDetailID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ResponseDetail_ResponseDetailID_seq" OWNER TO postgres;

--
-- Name: ResponseDetail_ResponseDetailID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."ResponseDetail_ResponseDetailID_seq" OWNED BY public."ResponseDetail"."ResponseDetailID";


--
-- Name: Response_ResponseID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Response_ResponseID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Response_ResponseID_seq" OWNER TO postgres;

--
-- Name: Response_ResponseID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Response_ResponseID_seq" OWNED BY public."Response"."ResponseID";


--
-- Name: Roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Roles" (
    "RoleID" integer NOT NULL,
    "RoleName" character varying(50) NOT NULL
);


ALTER TABLE public."Roles" OWNER TO postgres;

--
-- Name: Roles_RoleID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Roles_RoleID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Roles_RoleID_seq" OWNER TO postgres;

--
-- Name: Roles_RoleID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Roles_RoleID_seq" OWNED BY public."Roles"."RoleID";


--
-- Name: Section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Section" (
    "SectionID" integer NOT NULL,
    "SurveyID" integer,
    "Title" character varying(255) NOT NULL
);


ALTER TABLE public."Section" OWNER TO postgres;

--
-- Name: Section_SectionID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Section_SectionID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Section_SectionID_seq" OWNER TO postgres;

--
-- Name: Section_SectionID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Section_SectionID_seq" OWNED BY public."Section"."SectionID";


--
-- Name: Subsection; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Subsection" (
    "SubsectionID" integer NOT NULL,
    "SectionID" integer,
    "Title" character varying(255) NOT NULL
);


ALTER TABLE public."Subsection" OWNER TO postgres;

--
-- Name: Subsection_SubsectionID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Subsection_SubsectionID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Subsection_SubsectionID_seq" OWNER TO postgres;

--
-- Name: Subsection_SubsectionID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Subsection_SubsectionID_seq" OWNED BY public."Subsection"."SubsectionID";


--
-- Name: Survey; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Survey" (
    "SurveyID" integer NOT NULL,
    "Title" character varying(255) NOT NULL,
    "Description" text,
    "CreatedDate" timestamp without time zone,
    "UpdatedDate" timestamp without time zone,
    "Status" character varying(50),
    "CreatedBy" character varying(100),
    "ReviewedBy" character varying(100),
    "ApprovedBy" character varying(100),
    "PublishedBy" character varying(100),
    "ReviewDate" timestamp without time zone,
    "ApprovalDate" timestamp without time zone,
    "PublicationDate" timestamp without time zone,
    "Language" character varying(10),
    "Version" integer,
    "IsTemplate" boolean
);


ALTER TABLE public."Survey" OWNER TO postgres;

--
-- Name: SurveyMetrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."SurveyMetrics" (
    "MetricID" integer NOT NULL,
    "SurveyID" integer NOT NULL,
    "TotalResponses" integer,
    "CompletionRate" double precision,
    "AverageCompletionTime" double precision,
    "DataQualityScore" double precision,
    "ValidationErrorRate" double precision,
    "IncompleteResponses" integer,
    "ResponseByRegion" json,
    "ResponseTrend" json,
    "DataCollectionCost" double precision,
    "TimeToComplete" integer,
    "CoverageRate" double precision,
    "LastUpdated" timestamp without time zone
);


ALTER TABLE public."SurveyMetrics" OWNER TO postgres;

--
-- Name: SurveyMetrics_MetricID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."SurveyMetrics_MetricID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."SurveyMetrics_MetricID_seq" OWNER TO postgres;

--
-- Name: SurveyMetrics_MetricID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."SurveyMetrics_MetricID_seq" OWNED BY public."SurveyMetrics"."MetricID";


--
-- Name: SurveyTemplates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."SurveyTemplates" (
    "TemplateID" integer NOT NULL,
    "TemplateName" character varying(255) NOT NULL,
    "Domain" character varying(50) NOT NULL,
    "Category" character varying(50) NOT NULL,
    "Version" character varying(20),
    "CreatedBy" character varying(100),
    "CreatedDate" timestamp without time zone,
    "LastModified" timestamp without time zone,
    "ApprovedBy" character varying(100),
    "ApprovalDate" timestamp without time zone,
    "Sections" json,
    "DefaultQuestions" json,
    "UsageCount" integer,
    "LastUsed" timestamp without time zone,
    "UsageGuidelines" text,
    "ExampleImplementations" json
);


ALTER TABLE public."SurveyTemplates" OWNER TO postgres;

--
-- Name: SurveyTemplates_TemplateID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."SurveyTemplates_TemplateID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."SurveyTemplates_TemplateID_seq" OWNER TO postgres;

--
-- Name: SurveyTemplates_TemplateID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."SurveyTemplates_TemplateID_seq" OWNED BY public."SurveyTemplates"."TemplateID";


--
-- Name: Survey_SurveyID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Survey_SurveyID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Survey_SurveyID_seq" OWNER TO postgres;

--
-- Name: Survey_SurveyID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Survey_SurveyID_seq" OWNED BY public."Survey"."SurveyID";


--
-- Name: Users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Users" (
    "UserID" integer NOT NULL,
    "Username" character varying(255) NOT NULL,
    "Email" character varying(255) NOT NULL,
    "HashedPassword" character varying(255) NOT NULL,
    "FirstName" character varying(100) NOT NULL,
    "LastName" character varying(100) NOT NULL,
    "Role" character varying(50) NOT NULL,
    "Status" character varying(50) NOT NULL,
    "Department" character varying(100),
    "CreatedAt" timestamp without time zone NOT NULL,
    "UpdatedAt" timestamp without time zone NOT NULL
);


ALTER TABLE public."Users" OWNER TO postgres;

--
-- Name: Users_UserID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Users_UserID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Users_UserID_seq" OWNER TO postgres;

--
-- Name: Users_UserID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Users_UserID_seq" OWNED BY public."Users"."UserID";


--
-- Name: WorkflowActions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."WorkflowActions" (
    "ActionID" integer NOT NULL,
    "SurveyID" integer NOT NULL,
    "SchemaName" character varying(50) NOT NULL,
    "UserID" character varying(100),
    "ActionType" character varying(50) NOT NULL,
    "FromStatus" character varying(50),
    "ToStatus" character varying(50),
    "Comment" text,
    "Timestamp" timestamp without time zone
);


ALTER TABLE public."WorkflowActions" OWNER TO postgres;

--
-- Name: WorkflowActions_ActionID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."WorkflowActions_ActionID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."WorkflowActions_ActionID_seq" OWNER TO postgres;

--
-- Name: WorkflowActions_ActionID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."WorkflowActions_ActionID_seq" OWNED BY public."WorkflowActions"."ActionID";


--
-- Name: cmr_indicators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cmr_indicators (
    id integer NOT NULL,
    indicator_id character varying(50) NOT NULL,
    indicator_name text NOT NULL,
    category character varying(100),
    measurement_unit character varying(100),
    data_source character varying(255),
    collection_frequency character varying(50),
    responsible_structure character varying(100),
    baseline_value character varying(100),
    target_value character varying(100),
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.cmr_indicators OWNER TO postgres;

--
-- Name: COLUMN cmr_indicators.indicator_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.indicator_id IS 'Code de l''indicateur';


--
-- Name: COLUMN cmr_indicators.indicator_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.indicator_name IS 'Nom de l''indicateur';


--
-- Name: COLUMN cmr_indicators.category; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.category IS 'Catégorie';


--
-- Name: COLUMN cmr_indicators.measurement_unit; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.measurement_unit IS 'Unité de mesure';


--
-- Name: COLUMN cmr_indicators.data_source; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.data_source IS 'Source des données';


--
-- Name: COLUMN cmr_indicators.collection_frequency; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.collection_frequency IS 'Fréquence de collecte';


--
-- Name: COLUMN cmr_indicators.responsible_structure; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.responsible_structure IS 'Structure responsable';


--
-- Name: COLUMN cmr_indicators.baseline_value; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.baseline_value IS 'Valeur de référence';


--
-- Name: COLUMN cmr_indicators.target_value; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.cmr_indicators.target_value IS 'Valeur cible';


--
-- Name: cmr_indicators_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cmr_indicators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cmr_indicators_id_seq OWNER TO postgres;

--
-- Name: cmr_indicators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cmr_indicators_id_seq OWNED BY public.cmr_indicators.id;


--
-- Name: financing_sources; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.financing_sources (
    id integer NOT NULL,
    source_code character varying(20) NOT NULL,
    source_name character varying(255) NOT NULL,
    source_type character varying(100),
    currency character varying(10),
    min_amount double precision,
    max_amount double precision,
    financing_conditions text,
    contact_info json,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.financing_sources OWNER TO postgres;

--
-- Name: COLUMN financing_sources.source_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.financing_sources.source_code IS 'Code de la source';


--
-- Name: COLUMN financing_sources.source_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.financing_sources.source_name IS 'Nom de la source de financement';


--
-- Name: COLUMN financing_sources.source_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.financing_sources.source_type IS 'Type de source';


--
-- Name: COLUMN financing_sources.currency; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.financing_sources.currency IS 'Devise';


--
-- Name: COLUMN financing_sources.min_amount; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.financing_sources.min_amount IS 'Montant minimum';


--
-- Name: COLUMN financing_sources.max_amount; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.financing_sources.max_amount IS 'Montant maximum';


--
-- Name: COLUMN financing_sources.financing_conditions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.financing_sources.financing_conditions IS 'Conditions de financement';


--
-- Name: COLUMN financing_sources.contact_info; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.financing_sources.contact_info IS 'Informations de contact';


--
-- Name: financing_sources_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.financing_sources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.financing_sources_id_seq OWNER TO postgres;

--
-- Name: financing_sources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.financing_sources_id_seq OWNED BY public.financing_sources.id;


--
-- Name: instat_structures; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.instat_structures (
    id integer NOT NULL,
    structure_id character varying(20) NOT NULL,
    structure_name character varying(255) NOT NULL,
    abbreviation character varying(50),
    structure_type character varying(100),
    responsible_for_collection boolean,
    contact_info json,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.instat_structures OWNER TO postgres;

--
-- Name: COLUMN instat_structures.structure_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.instat_structures.structure_id IS 'Code de la structure';


--
-- Name: COLUMN instat_structures.structure_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.instat_structures.structure_name IS 'Nom de la structure';


--
-- Name: COLUMN instat_structures.abbreviation; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.instat_structures.abbreviation IS 'Abréviation';


--
-- Name: COLUMN instat_structures.structure_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.instat_structures.structure_type IS 'Type de structure';


--
-- Name: COLUMN instat_structures.responsible_for_collection; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.instat_structures.responsible_for_collection IS 'Structure en charge de collecte';


--
-- Name: COLUMN instat_structures.contact_info; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.instat_structures.contact_info IS 'Informations de contact';


--
-- Name: instat_structures_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.instat_structures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instat_structures_id_seq OWNER TO postgres;

--
-- Name: instat_structures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.instat_structures_id_seq OWNED BY public.instat_structures.id;


--
-- Name: mali_cercles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mali_cercles (
    id integer NOT NULL,
    cercle_code character varying(10) NOT NULL,
    cercle_name character varying(100) NOT NULL,
    region_code character varying(10),
    cercle_capital character varying(100),
    population integer,
    surface double precision,
    status character varying(20),
    coordinates json,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.mali_cercles OWNER TO postgres;

--
-- Name: COLUMN mali_cercles.cercle_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_cercles.cercle_code IS 'Code du cercle';


--
-- Name: COLUMN mali_cercles.cercle_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_cercles.cercle_name IS 'Nom du cercle';


--
-- Name: COLUMN mali_cercles.region_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_cercles.region_code IS 'Code de la région';


--
-- Name: COLUMN mali_cercles.cercle_capital; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_cercles.cercle_capital IS 'Chef-lieu de cercle';


--
-- Name: COLUMN mali_cercles.population; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_cercles.population IS 'Population';


--
-- Name: COLUMN mali_cercles.surface; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_cercles.surface IS 'Superficie en km²';


--
-- Name: COLUMN mali_cercles.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_cercles.status IS 'Statut';


--
-- Name: COLUMN mali_cercles.coordinates; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_cercles.coordinates IS 'Coordonnées géographiques';


--
-- Name: mali_cercles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mali_cercles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mali_cercles_id_seq OWNER TO postgres;

--
-- Name: mali_cercles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mali_cercles_id_seq OWNED BY public.mali_cercles.id;


--
-- Name: mali_regions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mali_regions (
    id integer NOT NULL,
    region_code character varying(10) NOT NULL,
    region_name character varying(100) NOT NULL,
    region_capital character varying(100),
    population integer,
    surface double precision,
    status character varying(20),
    coordinates json,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.mali_regions OWNER TO postgres;

--
-- Name: COLUMN mali_regions.region_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_regions.region_code IS 'Code de la région';


--
-- Name: COLUMN mali_regions.region_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_regions.region_name IS 'Nom de la région';


--
-- Name: COLUMN mali_regions.region_capital; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_regions.region_capital IS 'Chef-lieu de région';


--
-- Name: COLUMN mali_regions.population; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_regions.population IS 'Population';


--
-- Name: COLUMN mali_regions.surface; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_regions.surface IS 'Superficie en km²';


--
-- Name: COLUMN mali_regions.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_regions.status IS 'Statut';


--
-- Name: COLUMN mali_regions.coordinates; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.mali_regions.coordinates IS 'Coordonnées géographiques';


--
-- Name: mali_regions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mali_regions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mali_regions_id_seq OWNER TO postgres;

--
-- Name: mali_regions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mali_regions_id_seq OWNED BY public.mali_regions.id;


--
-- Name: monitoring_indicators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.monitoring_indicators (
    id integer NOT NULL,
    indicator_code character varying(50) NOT NULL,
    indicator_name text NOT NULL,
    category character varying(100),
    measurement_method text,
    reporting_frequency character varying(50),
    target_value character varying(100),
    data_collection_method text,
    responsible_unit character varying(100),
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.monitoring_indicators OWNER TO postgres;

--
-- Name: COLUMN monitoring_indicators.indicator_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.monitoring_indicators.indicator_code IS 'Code de l''indicateur';


--
-- Name: COLUMN monitoring_indicators.indicator_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.monitoring_indicators.indicator_name IS 'Nom de l''indicateur';


--
-- Name: COLUMN monitoring_indicators.category; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.monitoring_indicators.category IS 'Catégorie';


--
-- Name: COLUMN monitoring_indicators.measurement_method; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.monitoring_indicators.measurement_method IS 'Méthode de mesure';


--
-- Name: COLUMN monitoring_indicators.reporting_frequency; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.monitoring_indicators.reporting_frequency IS 'Fréquence de rapportage';


--
-- Name: COLUMN monitoring_indicators.target_value; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.monitoring_indicators.target_value IS 'Valeur cible';


--
-- Name: COLUMN monitoring_indicators.data_collection_method; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.monitoring_indicators.data_collection_method IS 'Méthode de collecte des données';


--
-- Name: COLUMN monitoring_indicators.responsible_unit; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.monitoring_indicators.responsible_unit IS 'Unité responsable';


--
-- Name: monitoring_indicators_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.monitoring_indicators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.monitoring_indicators_id_seq OWNER TO postgres;

--
-- Name: monitoring_indicators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.monitoring_indicators_id_seq OWNED BY public.monitoring_indicators.id;


--
-- Name: operational_results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.operational_results (
    id integer NOT NULL,
    result_code character varying(50) NOT NULL,
    axis_code character varying(20),
    objective_code character varying(20),
    result_description text NOT NULL,
    performance_indicators json,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.operational_results OWNER TO postgres;

--
-- Name: COLUMN operational_results.result_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operational_results.result_code IS 'Code du résultat';


--
-- Name: COLUMN operational_results.axis_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operational_results.axis_code IS 'Code de l''axe';


--
-- Name: COLUMN operational_results.objective_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operational_results.objective_code IS 'Code de l''objectif';


--
-- Name: COLUMN operational_results.result_description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operational_results.result_description IS 'Description du résultat';


--
-- Name: COLUMN operational_results.performance_indicators; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operational_results.performance_indicators IS 'Indicateurs de performance';


--
-- Name: operational_results_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.operational_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.operational_results_id_seq OWNER TO postgres;

--
-- Name: operational_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.operational_results_id_seq OWNED BY public.operational_results.id;


--
-- Name: participating_structures; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participating_structures (
    id integer NOT NULL,
    structure_code character varying(20) NOT NULL,
    structure_name character varying(255) NOT NULL,
    participation_type character varying(100),
    role text,
    contact_info text,
    expertise_areas json,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.participating_structures OWNER TO postgres;

--
-- Name: COLUMN participating_structures.structure_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participating_structures.structure_code IS 'Code de la structure';


--
-- Name: COLUMN participating_structures.structure_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participating_structures.structure_name IS 'Nom de la structure';


--
-- Name: COLUMN participating_structures.participation_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participating_structures.participation_type IS 'Type de participation';


--
-- Name: COLUMN participating_structures.role; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participating_structures.role IS 'Rôle dans l''activité';


--
-- Name: COLUMN participating_structures.contact_info; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participating_structures.contact_info IS 'Informations de contact';


--
-- Name: COLUMN participating_structures.expertise_areas; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participating_structures.expertise_areas IS 'Domaines d''expertise';


--
-- Name: participating_structures_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participating_structures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participating_structures_id_seq OWNER TO postgres;

--
-- Name: participating_structures_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participating_structures_id_seq OWNED BY public.participating_structures.id;


--
-- Name: sds_activity_surveys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sds_activity_surveys (
    id integer NOT NULL,
    fiche_number character varying(50) NOT NULL,
    order_number integer NOT NULL,
    total_fiches integer NOT NULL,
    region_code character varying(10),
    cercle_code character varying(10),
    implementing_structure character varying(20),
    data_collection_structure character varying(20),
    activity_title text,
    is_data_disaggregatable boolean,
    disaggregation_by_gender boolean,
    disaggregation_by_age boolean,
    disaggregation_by_sex boolean,
    disaggregation_by_disability boolean,
    disaggregation_by_decision_participation boolean,
    disaggregation_by_territory boolean,
    disaggregation_by_residence_area boolean,
    region_level boolean,
    cercle_level boolean,
    arrondissement_level boolean,
    commune_level boolean,
    urban_area boolean,
    rural_area boolean,
    financing_sources json,
    activity_cost double precision,
    monitoring_indicators json,
    completion_result character varying(10),
    created_by character varying(100),
    reviewed_by character varying(100),
    approved_by character varying(100),
    review_date timestamp with time zone,
    approval_date timestamp with time zone,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.sds_activity_surveys OWNER TO postgres;

--
-- Name: COLUMN sds_activity_surveys.fiche_number; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.fiche_number IS 'Numéro de fiche';


--
-- Name: COLUMN sds_activity_surveys.order_number; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.order_number IS 'Numéro d''ordre';


--
-- Name: COLUMN sds_activity_surveys.total_fiches; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.total_fiches IS 'Nombre total de fiches';


--
-- Name: COLUMN sds_activity_surveys.region_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.region_code IS 'Code de la région';


--
-- Name: COLUMN sds_activity_surveys.cercle_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.cercle_code IS 'Code du cercle';


--
-- Name: COLUMN sds_activity_surveys.implementing_structure; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.implementing_structure IS 'Structure en charge de réalisation';


--
-- Name: COLUMN sds_activity_surveys.data_collection_structure; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.data_collection_structure IS 'Structure en charge de collecte';


--
-- Name: COLUMN sds_activity_surveys.activity_title; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.activity_title IS 'Intitulé de l''activité';


--
-- Name: COLUMN sds_activity_surveys.is_data_disaggregatable; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.is_data_disaggregatable IS 'Les données sont-elles désagrégées?';


--
-- Name: COLUMN sds_activity_surveys.disaggregation_by_gender; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.disaggregation_by_gender IS 'Désagrégation par genre';


--
-- Name: COLUMN sds_activity_surveys.disaggregation_by_age; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.disaggregation_by_age IS 'Désagrégation par âge';


--
-- Name: COLUMN sds_activity_surveys.disaggregation_by_sex; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.disaggregation_by_sex IS 'Désagrégation par sexe';


--
-- Name: COLUMN sds_activity_surveys.disaggregation_by_disability; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.disaggregation_by_disability IS 'Désagrégation par handicap';


--
-- Name: COLUMN sds_activity_surveys.disaggregation_by_decision_participation; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.disaggregation_by_decision_participation IS 'Désagrégation par participation à la décision';


--
-- Name: COLUMN sds_activity_surveys.disaggregation_by_territory; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.disaggregation_by_territory IS 'Désagrégation territoriale';


--
-- Name: COLUMN sds_activity_surveys.disaggregation_by_residence_area; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.disaggregation_by_residence_area IS 'Désagrégation par milieu de résidence';


--
-- Name: COLUMN sds_activity_surveys.region_level; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.region_level IS 'Niveau région';


--
-- Name: COLUMN sds_activity_surveys.cercle_level; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.cercle_level IS 'Niveau cercle';


--
-- Name: COLUMN sds_activity_surveys.arrondissement_level; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.arrondissement_level IS 'Niveau arrondissement';


--
-- Name: COLUMN sds_activity_surveys.commune_level; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.commune_level IS 'Niveau commune';


--
-- Name: COLUMN sds_activity_surveys.urban_area; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.urban_area IS 'Urbain';


--
-- Name: COLUMN sds_activity_surveys.rural_area; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.rural_area IS 'Rural';


--
-- Name: COLUMN sds_activity_surveys.financing_sources; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.financing_sources IS 'Sources de financement';


--
-- Name: COLUMN sds_activity_surveys.activity_cost; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.activity_cost IS 'Coût de l''activité en FCFA';


--
-- Name: COLUMN sds_activity_surveys.monitoring_indicators; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.monitoring_indicators IS 'Indicateurs de suivi';


--
-- Name: COLUMN sds_activity_surveys.completion_result; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.completion_result IS 'Résultat de remplissage: 1=Complet, 2=Partiel, 3=Non rempli';


--
-- Name: COLUMN sds_activity_surveys.created_by; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.created_by IS 'Créé par';


--
-- Name: COLUMN sds_activity_surveys.reviewed_by; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.reviewed_by IS 'Revu par';


--
-- Name: COLUMN sds_activity_surveys.approved_by; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.approved_by IS 'Approuvé par';


--
-- Name: COLUMN sds_activity_surveys.review_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.review_date IS 'Date de révision';


--
-- Name: COLUMN sds_activity_surveys.approval_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.sds_activity_surveys.approval_date IS 'Date d''approbation';


--
-- Name: sds_activity_surveys_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sds_activity_surveys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sds_activity_surveys_id_seq OWNER TO postgres;

--
-- Name: sds_activity_surveys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sds_activity_surveys_id_seq OWNED BY public.sds_activity_surveys.id;


--
-- Name: strategic_axis_results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.strategic_axis_results (
    id integer NOT NULL,
    result_id character varying(50) NOT NULL,
    strategic_axis text NOT NULL,
    operational_objective text NOT NULL,
    expected_result text NOT NULL,
    activity text NOT NULL,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.strategic_axis_results OWNER TO postgres;

--
-- Name: COLUMN strategic_axis_results.result_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.strategic_axis_results.result_id IS 'Code du résultat';


--
-- Name: COLUMN strategic_axis_results.strategic_axis; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.strategic_axis_results.strategic_axis IS 'Axe stratégique';


--
-- Name: COLUMN strategic_axis_results.operational_objective; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.strategic_axis_results.operational_objective IS 'Objectifs opérationnels';


--
-- Name: COLUMN strategic_axis_results.expected_result; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.strategic_axis_results.expected_result IS 'Résultats attendus';


--
-- Name: COLUMN strategic_axis_results.activity; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.strategic_axis_results.activity IS 'Activité';


--
-- Name: strategic_axis_results_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.strategic_axis_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.strategic_axis_results_id_seq OWNER TO postgres;

--
-- Name: strategic_axis_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.strategic_axis_results_id_seq OWNED BY public.strategic_axis_results.id;


--
-- Name: survey_responses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.survey_responses (
    id integer NOT NULL,
    survey_id integer NOT NULL,
    question_id integer NOT NULL,
    response_value text,
    table_reference character varying(50),
    reference_code character varying(50),
    respondent_id character varying(100),
    response_date timestamp with time zone DEFAULT now(),
    is_validated boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.survey_responses OWNER TO postgres;

--
-- Name: COLUMN survey_responses.survey_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.survey_responses.survey_id IS 'ID de l''enquête';


--
-- Name: COLUMN survey_responses.question_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.survey_responses.question_id IS 'ID de la question';


--
-- Name: COLUMN survey_responses.response_value; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.survey_responses.response_value IS 'Valeur de la réponse';


--
-- Name: COLUMN survey_responses.table_reference; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.survey_responses.table_reference IS 'Reference à la table (e.g., ''TableRef:08'')';


--
-- Name: COLUMN survey_responses.reference_code; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.survey_responses.reference_code IS 'Code de la table de référence';


--
-- Name: COLUMN survey_responses.respondent_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.survey_responses.respondent_id IS 'ID du répondant';


--
-- Name: survey_responses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.survey_responses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.survey_responses_id_seq OWNER TO postgres;

--
-- Name: survey_responses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.survey_responses_id_seq OWNED BY public.survey_responses.id;


--
-- Name: table_reference_mappings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.table_reference_mappings (
    id integer NOT NULL,
    table_ref character varying(20) NOT NULL,
    table_name character varying(100) NOT NULL,
    model_class character varying(100) NOT NULL,
    description text,
    display_fields json,
    search_fields json,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.table_reference_mappings OWNER TO postgres;

--
-- Name: COLUMN table_reference_mappings.table_ref; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.table_reference_mappings.table_ref IS 'Table reference (e.g., ''TableRef:08'')';


--
-- Name: COLUMN table_reference_mappings.table_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.table_reference_mappings.table_name IS 'Nom de la table';


--
-- Name: COLUMN table_reference_mappings.model_class; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.table_reference_mappings.model_class IS 'Nom de la classe de modèle';


--
-- Name: COLUMN table_reference_mappings.description; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.table_reference_mappings.description IS 'Description de la table';


--
-- Name: COLUMN table_reference_mappings.display_fields; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.table_reference_mappings.display_fields IS 'Champs à afficher';


--
-- Name: COLUMN table_reference_mappings.search_fields; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.table_reference_mappings.search_fields IS 'Champs de recherche';


--
-- Name: table_reference_mappings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.table_reference_mappings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.table_reference_mappings_id_seq OWNER TO postgres;

--
-- Name: table_reference_mappings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.table_reference_mappings_id_seq OWNED BY public.table_reference_mappings.id;


--
-- Name: AnswerOption OptionID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AnswerOption" ALTER COLUMN "OptionID" SET DEFAULT nextval('public."AnswerOption_OptionID_seq"'::regclass);


--
-- Name: AuditLog LogID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AuditLog" ALTER COLUMN "LogID" SET DEFAULT nextval('public."AuditLog_LogID_seq"'::regclass);


--
-- Name: DataExports ExportID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataExports" ALTER COLUMN "ExportID" SET DEFAULT nextval('public."DataExports_ExportID_seq"'::regclass);


--
-- Name: INSTATQuestions QuestionID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INSTATQuestions" ALTER COLUMN "QuestionID" SET DEFAULT nextval('public."INSTATQuestions_QuestionID_seq"'::regclass);


--
-- Name: INSTATSurveys SurveyID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INSTATSurveys" ALTER COLUMN "SurveyID" SET DEFAULT nextval('public."INSTATSurveys_SurveyID_seq"'::regclass);


--
-- Name: ParsingResult ResultID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ParsingResult" ALTER COLUMN "ResultID" SET DEFAULT nextval('public."ParsingResult_ResultID_seq"'::regclass);


--
-- Name: ParsingStatistics StatID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ParsingStatistics" ALTER COLUMN "StatID" SET DEFAULT nextval('public."ParsingStatistics_StatID_seq"'::regclass);


--
-- Name: Question QuestionID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Question" ALTER COLUMN "QuestionID" SET DEFAULT nextval('public."Question_QuestionID_seq"'::regclass);


--
-- Name: Response ResponseID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Response" ALTER COLUMN "ResponseID" SET DEFAULT nextval('public."Response_ResponseID_seq"'::regclass);


--
-- Name: ResponseDetail ResponseDetailID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ResponseDetail" ALTER COLUMN "ResponseDetailID" SET DEFAULT nextval('public."ResponseDetail_ResponseDetailID_seq"'::regclass);


--
-- Name: Roles RoleID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Roles" ALTER COLUMN "RoleID" SET DEFAULT nextval('public."Roles_RoleID_seq"'::regclass);


--
-- Name: Section SectionID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Section" ALTER COLUMN "SectionID" SET DEFAULT nextval('public."Section_SectionID_seq"'::regclass);


--
-- Name: Subsection SubsectionID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Subsection" ALTER COLUMN "SubsectionID" SET DEFAULT nextval('public."Subsection_SubsectionID_seq"'::regclass);


--
-- Name: Survey SurveyID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Survey" ALTER COLUMN "SurveyID" SET DEFAULT nextval('public."Survey_SurveyID_seq"'::regclass);


--
-- Name: SurveyMetrics MetricID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."SurveyMetrics" ALTER COLUMN "MetricID" SET DEFAULT nextval('public."SurveyMetrics_MetricID_seq"'::regclass);


--
-- Name: SurveyTemplates TemplateID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."SurveyTemplates" ALTER COLUMN "TemplateID" SET DEFAULT nextval('public."SurveyTemplates_TemplateID_seq"'::regclass);


--
-- Name: Users UserID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users" ALTER COLUMN "UserID" SET DEFAULT nextval('public."Users_UserID_seq"'::regclass);


--
-- Name: WorkflowActions ActionID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."WorkflowActions" ALTER COLUMN "ActionID" SET DEFAULT nextval('public."WorkflowActions_ActionID_seq"'::regclass);


--
-- Name: cmr_indicators id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cmr_indicators ALTER COLUMN id SET DEFAULT nextval('public.cmr_indicators_id_seq'::regclass);


--
-- Name: financing_sources id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.financing_sources ALTER COLUMN id SET DEFAULT nextval('public.financing_sources_id_seq'::regclass);


--
-- Name: instat_structures id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instat_structures ALTER COLUMN id SET DEFAULT nextval('public.instat_structures_id_seq'::regclass);


--
-- Name: mali_cercles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mali_cercles ALTER COLUMN id SET DEFAULT nextval('public.mali_cercles_id_seq'::regclass);


--
-- Name: mali_regions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mali_regions ALTER COLUMN id SET DEFAULT nextval('public.mali_regions_id_seq'::regclass);


--
-- Name: monitoring_indicators id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitoring_indicators ALTER COLUMN id SET DEFAULT nextval('public.monitoring_indicators_id_seq'::regclass);


--
-- Name: operational_results id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operational_results ALTER COLUMN id SET DEFAULT nextval('public.operational_results_id_seq'::regclass);


--
-- Name: participating_structures id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participating_structures ALTER COLUMN id SET DEFAULT nextval('public.participating_structures_id_seq'::regclass);


--
-- Name: sds_activity_surveys id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sds_activity_surveys ALTER COLUMN id SET DEFAULT nextval('public.sds_activity_surveys_id_seq'::regclass);


--
-- Name: strategic_axis_results id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.strategic_axis_results ALTER COLUMN id SET DEFAULT nextval('public.strategic_axis_results_id_seq'::regclass);


--
-- Name: survey_responses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.survey_responses ALTER COLUMN id SET DEFAULT nextval('public.survey_responses_id_seq'::regclass);


--
-- Name: table_reference_mappings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_reference_mappings ALTER COLUMN id SET DEFAULT nextval('public.table_reference_mappings_id_seq'::regclass);


--
-- Data for Name: AnswerOption; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."AnswerOption" ("OptionID", "QuestionID", "OptionText") FROM stdin;
\.


--
-- Data for Name: AuditLog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."AuditLog" ("LogID", "UserID", "Username", "Action", "Resource", "ResourceID", "Details", "IPAddress", "UserAgent", "Success", "ErrorMessage", "Timestamp") FROM stdin;
\.


--
-- Data for Name: DataExports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."DataExports" ("ExportID", "SurveyID", "ExportFormat") FROM stdin;
\.


--
-- Data for Name: INSTATQuestions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."INSTATQuestions" ("QuestionID", "SurveyID", "SectionID", "SubsectionID", "QuestionText", "QuestionType", "IsRequired", "IndicatorCode", "DataSource", "CollectionMethod", "QualityRequirements", "ValidationRules", "DependsOnQuestion", "QuestionTextEN", "QuestionTextFR", "Tags", "Priority") FROM stdin;
\.


--
-- Data for Name: INSTATSurveys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."INSTATSurveys" ("SurveyID", "Title", "Description", "Domain", "Category", "CreatedDate", "UpdatedDate", "Status", "FiscalYear", "ReportingCycle", "CreatedBy", "ReviewedBy", "ApprovedBy", "PublishedBy", "ImplementingUnit", "ReviewDate", "ApprovalDate", "PublicationDate", "Language", "Version", "IsTemplate", "TargetAudience", "GeographicScope", "ComplianceFramework", "InternationalStandards", "RequiredSkills", "BudgetCategory", "EstimatedDuration", "DomainSpecificFields") FROM stdin;
\.


--
-- Data for Name: ParsingResult; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ParsingResult" ("ResultID", "FileName", "ParsedData", "ValidationIssues", "Success", "ErrorMessage", "Timestamp") FROM stdin;
\.


--
-- Data for Name: ParsingStatistics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ParsingStatistics" ("StatID", "TotalFiles", "SuccessfulParses", "FailedParses", "AverageParseTime", "LastUpdated") FROM stdin;
\.


--
-- Data for Name: Question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Question" ("QuestionID", "SectionID", "SubsectionID", "QuestionText", "QuestionType") FROM stdin;
\.


--
-- Data for Name: Response; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Response" ("ResponseID", "SurveyID", "RespondentID", "SubmittedDate") FROM stdin;
\.


--
-- Data for Name: ResponseDetail; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ResponseDetail" ("ResponseDetailID", "ResponseID", "QuestionID", "SelectedOptionID", "AnswerText") FROM stdin;
\.


--
-- Data for Name: Roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Roles" ("RoleID", "RoleName") FROM stdin;
\.


--
-- Data for Name: Section; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Section" ("SectionID", "SurveyID", "Title") FROM stdin;
\.


--
-- Data for Name: Subsection; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Subsection" ("SubsectionID", "SectionID", "Title") FROM stdin;
\.


--
-- Data for Name: Survey; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Survey" ("SurveyID", "Title", "Description", "CreatedDate", "UpdatedDate", "Status", "CreatedBy", "ReviewedBy", "ApprovedBy", "PublishedBy", "ReviewDate", "ApprovalDate", "PublicationDate", "Language", "Version", "IsTemplate") FROM stdin;
\.


--
-- Data for Name: SurveyMetrics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."SurveyMetrics" ("MetricID", "SurveyID", "TotalResponses", "CompletionRate", "AverageCompletionTime", "DataQualityScore", "ValidationErrorRate", "IncompleteResponses", "ResponseByRegion", "ResponseTrend", "DataCollectionCost", "TimeToComplete", "CoverageRate", "LastUpdated") FROM stdin;
\.


--
-- Data for Name: SurveyTemplates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."SurveyTemplates" ("TemplateID", "TemplateName", "Domain", "Category", "Version", "CreatedBy", "CreatedDate", "LastModified", "ApprovedBy", "ApprovalDate", "Sections", "DefaultQuestions", "UsageCount", "LastUsed", "UsageGuidelines", "ExampleImplementations") FROM stdin;
\.


--
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Users" ("UserID", "Username", "Email", "HashedPassword", "FirstName", "LastName", "Role", "Status", "Department", "CreatedAt", "UpdatedAt") FROM stdin;
\.


--
-- Data for Name: WorkflowActions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."WorkflowActions" ("ActionID", "SurveyID", "SchemaName", "UserID", "ActionType", "FromStatus", "ToStatus", "Comment", "Timestamp") FROM stdin;
\.


--
-- Data for Name: cmr_indicators; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cmr_indicators (id, indicator_id, indicator_name, category, measurement_unit, data_source, collection_frequency, responsible_structure, baseline_value, target_value, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: financing_sources; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.financing_sources (id, source_code, source_name, source_type, currency, min_amount, max_amount, financing_conditions, contact_info, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: instat_structures; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.instat_structures (id, structure_id, structure_name, abbreviation, structure_type, responsible_for_collection, contact_info, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: mali_cercles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mali_cercles (id, cercle_code, cercle_name, region_code, cercle_capital, population, surface, status, coordinates, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: mali_regions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mali_regions (id, region_code, region_name, region_capital, population, surface, status, coordinates, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: monitoring_indicators; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.monitoring_indicators (id, indicator_code, indicator_name, category, measurement_method, reporting_frequency, target_value, data_collection_method, responsible_unit, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: operational_results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.operational_results (id, result_code, axis_code, objective_code, result_description, performance_indicators, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: participating_structures; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participating_structures (id, structure_code, structure_name, participation_type, role, contact_info, expertise_areas, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: sds_activity_surveys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sds_activity_surveys (id, fiche_number, order_number, total_fiches, region_code, cercle_code, implementing_structure, data_collection_structure, activity_title, is_data_disaggregatable, disaggregation_by_gender, disaggregation_by_age, disaggregation_by_sex, disaggregation_by_disability, disaggregation_by_decision_participation, disaggregation_by_territory, disaggregation_by_residence_area, region_level, cercle_level, arrondissement_level, commune_level, urban_area, rural_area, financing_sources, activity_cost, monitoring_indicators, completion_result, created_by, reviewed_by, approved_by, review_date, approval_date, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: strategic_axis_results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.strategic_axis_results (id, result_id, strategic_axis, operational_objective, expected_result, activity, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: survey_responses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.survey_responses (id, survey_id, question_id, response_value, table_reference, reference_code, respondent_id, response_date, is_validated, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: table_reference_mappings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.table_reference_mappings (id, table_ref, table_name, model_class, description, display_fields, search_fields, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Name: AnswerOption_OptionID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."AnswerOption_OptionID_seq"', 1, false);


--
-- Name: AuditLog_LogID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."AuditLog_LogID_seq"', 1, false);


--
-- Name: DataExports_ExportID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."DataExports_ExportID_seq"', 1, false);


--
-- Name: INSTATQuestions_QuestionID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."INSTATQuestions_QuestionID_seq"', 1, false);


--
-- Name: INSTATSurveys_SurveyID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."INSTATSurveys_SurveyID_seq"', 1, false);


--
-- Name: ParsingResult_ResultID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."ParsingResult_ResultID_seq"', 1, false);


--
-- Name: ParsingStatistics_StatID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."ParsingStatistics_StatID_seq"', 1, false);


--
-- Name: Question_QuestionID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Question_QuestionID_seq"', 1, false);


--
-- Name: ResponseDetail_ResponseDetailID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."ResponseDetail_ResponseDetailID_seq"', 1, false);


--
-- Name: Response_ResponseID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Response_ResponseID_seq"', 1, false);


--
-- Name: Roles_RoleID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Roles_RoleID_seq"', 1, false);


--
-- Name: Section_SectionID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Section_SectionID_seq"', 1, false);


--
-- Name: Subsection_SubsectionID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Subsection_SubsectionID_seq"', 1, false);


--
-- Name: SurveyMetrics_MetricID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."SurveyMetrics_MetricID_seq"', 1, false);


--
-- Name: SurveyTemplates_TemplateID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."SurveyTemplates_TemplateID_seq"', 1, false);


--
-- Name: Survey_SurveyID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Survey_SurveyID_seq"', 1, false);


--
-- Name: Users_UserID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Users_UserID_seq"', 1, false);


--
-- Name: WorkflowActions_ActionID_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."WorkflowActions_ActionID_seq"', 1, false);


--
-- Name: cmr_indicators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cmr_indicators_id_seq', 1, false);


--
-- Name: financing_sources_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.financing_sources_id_seq', 1, false);


--
-- Name: instat_structures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.instat_structures_id_seq', 1, false);


--
-- Name: mali_cercles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mali_cercles_id_seq', 1, false);


--
-- Name: mali_regions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mali_regions_id_seq', 1, false);


--
-- Name: monitoring_indicators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.monitoring_indicators_id_seq', 1, false);


--
-- Name: operational_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.operational_results_id_seq', 1, false);


--
-- Name: participating_structures_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participating_structures_id_seq', 1, false);


--
-- Name: sds_activity_surveys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sds_activity_surveys_id_seq', 1, false);


--
-- Name: strategic_axis_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.strategic_axis_results_id_seq', 1, false);


--
-- Name: survey_responses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.survey_responses_id_seq', 1, false);


--
-- Name: table_reference_mappings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.table_reference_mappings_id_seq', 1, false);


--
-- Name: AnswerOption AnswerOption_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AnswerOption"
    ADD CONSTRAINT "AnswerOption_pkey" PRIMARY KEY ("OptionID");


--
-- Name: AuditLog AuditLog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AuditLog"
    ADD CONSTRAINT "AuditLog_pkey" PRIMARY KEY ("LogID");


--
-- Name: DataExports DataExports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataExports"
    ADD CONSTRAINT "DataExports_pkey" PRIMARY KEY ("ExportID");


--
-- Name: INSTATQuestions INSTATQuestions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INSTATQuestions"
    ADD CONSTRAINT "INSTATQuestions_pkey" PRIMARY KEY ("QuestionID");


--
-- Name: INSTATSurveys INSTATSurveys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INSTATSurveys"
    ADD CONSTRAINT "INSTATSurveys_pkey" PRIMARY KEY ("SurveyID");


--
-- Name: ParsingResult ParsingResult_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ParsingResult"
    ADD CONSTRAINT "ParsingResult_pkey" PRIMARY KEY ("ResultID");


--
-- Name: ParsingStatistics ParsingStatistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ParsingStatistics"
    ADD CONSTRAINT "ParsingStatistics_pkey" PRIMARY KEY ("StatID");


--
-- Name: Question Question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Question"
    ADD CONSTRAINT "Question_pkey" PRIMARY KEY ("QuestionID");


--
-- Name: ResponseDetail ResponseDetail_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ResponseDetail"
    ADD CONSTRAINT "ResponseDetail_pkey" PRIMARY KEY ("ResponseDetailID");


--
-- Name: Response Response_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Response"
    ADD CONSTRAINT "Response_pkey" PRIMARY KEY ("ResponseID");


--
-- Name: Roles Roles_RoleName_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Roles"
    ADD CONSTRAINT "Roles_RoleName_key" UNIQUE ("RoleName");


--
-- Name: Roles Roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Roles"
    ADD CONSTRAINT "Roles_pkey" PRIMARY KEY ("RoleID");


--
-- Name: Section Section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Section"
    ADD CONSTRAINT "Section_pkey" PRIMARY KEY ("SectionID");


--
-- Name: Subsection Subsection_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Subsection"
    ADD CONSTRAINT "Subsection_pkey" PRIMARY KEY ("SubsectionID");


--
-- Name: SurveyMetrics SurveyMetrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."SurveyMetrics"
    ADD CONSTRAINT "SurveyMetrics_pkey" PRIMARY KEY ("MetricID");


--
-- Name: SurveyTemplates SurveyTemplates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."SurveyTemplates"
    ADD CONSTRAINT "SurveyTemplates_pkey" PRIMARY KEY ("TemplateID");


--
-- Name: Survey Survey_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Survey"
    ADD CONSTRAINT "Survey_pkey" PRIMARY KEY ("SurveyID");


--
-- Name: Users Users_Email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_Email_key" UNIQUE ("Email");


--
-- Name: Users Users_Username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_Username_key" UNIQUE ("Username");


--
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY ("UserID");


--
-- Name: WorkflowActions WorkflowActions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."WorkflowActions"
    ADD CONSTRAINT "WorkflowActions_pkey" PRIMARY KEY ("ActionID");


--
-- Name: cmr_indicators cmr_indicators_indicator_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cmr_indicators
    ADD CONSTRAINT cmr_indicators_indicator_id_key UNIQUE (indicator_id);


--
-- Name: cmr_indicators cmr_indicators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cmr_indicators
    ADD CONSTRAINT cmr_indicators_pkey PRIMARY KEY (id);


--
-- Name: financing_sources financing_sources_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.financing_sources
    ADD CONSTRAINT financing_sources_pkey PRIMARY KEY (id);


--
-- Name: financing_sources financing_sources_source_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.financing_sources
    ADD CONSTRAINT financing_sources_source_code_key UNIQUE (source_code);


--
-- Name: instat_structures instat_structures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instat_structures
    ADD CONSTRAINT instat_structures_pkey PRIMARY KEY (id);


--
-- Name: instat_structures instat_structures_structure_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instat_structures
    ADD CONSTRAINT instat_structures_structure_id_key UNIQUE (structure_id);


--
-- Name: mali_cercles mali_cercles_cercle_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mali_cercles
    ADD CONSTRAINT mali_cercles_cercle_code_key UNIQUE (cercle_code);


--
-- Name: mali_cercles mali_cercles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mali_cercles
    ADD CONSTRAINT mali_cercles_pkey PRIMARY KEY (id);


--
-- Name: mali_regions mali_regions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mali_regions
    ADD CONSTRAINT mali_regions_pkey PRIMARY KEY (id);


--
-- Name: mali_regions mali_regions_region_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mali_regions
    ADD CONSTRAINT mali_regions_region_code_key UNIQUE (region_code);


--
-- Name: monitoring_indicators monitoring_indicators_indicator_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitoring_indicators
    ADD CONSTRAINT monitoring_indicators_indicator_code_key UNIQUE (indicator_code);


--
-- Name: monitoring_indicators monitoring_indicators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.monitoring_indicators
    ADD CONSTRAINT monitoring_indicators_pkey PRIMARY KEY (id);


--
-- Name: operational_results operational_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operational_results
    ADD CONSTRAINT operational_results_pkey PRIMARY KEY (id);


--
-- Name: operational_results operational_results_result_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operational_results
    ADD CONSTRAINT operational_results_result_code_key UNIQUE (result_code);


--
-- Name: participating_structures participating_structures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participating_structures
    ADD CONSTRAINT participating_structures_pkey PRIMARY KEY (id);


--
-- Name: participating_structures participating_structures_structure_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participating_structures
    ADD CONSTRAINT participating_structures_structure_code_key UNIQUE (structure_code);


--
-- Name: sds_activity_surveys sds_activity_surveys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sds_activity_surveys
    ADD CONSTRAINT sds_activity_surveys_pkey PRIMARY KEY (id);


--
-- Name: strategic_axis_results strategic_axis_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.strategic_axis_results
    ADD CONSTRAINT strategic_axis_results_pkey PRIMARY KEY (id);


--
-- Name: strategic_axis_results strategic_axis_results_result_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.strategic_axis_results
    ADD CONSTRAINT strategic_axis_results_result_id_key UNIQUE (result_id);


--
-- Name: survey_responses survey_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.survey_responses
    ADD CONSTRAINT survey_responses_pkey PRIMARY KEY (id);


--
-- Name: table_reference_mappings table_reference_mappings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_reference_mappings
    ADD CONSTRAINT table_reference_mappings_pkey PRIMARY KEY (id);


--
-- Name: ix_AnswerOption_OptionID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_AnswerOption_OptionID" ON public."AnswerOption" USING btree ("OptionID");


--
-- Name: ix_Question_QuestionID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_Question_QuestionID" ON public."Question" USING btree ("QuestionID");


--
-- Name: ix_ResponseDetail_ResponseDetailID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_ResponseDetail_ResponseDetailID" ON public."ResponseDetail" USING btree ("ResponseDetailID");


--
-- Name: ix_Response_ResponseID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_Response_ResponseID" ON public."Response" USING btree ("ResponseID");


--
-- Name: ix_Section_SectionID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_Section_SectionID" ON public."Section" USING btree ("SectionID");


--
-- Name: ix_Subsection_SubsectionID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_Subsection_SubsectionID" ON public."Subsection" USING btree ("SubsectionID");


--
-- Name: ix_Survey_SurveyID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_Survey_SurveyID" ON public."Survey" USING btree ("SurveyID");


--
-- Name: ix_public_AuditLog_LogID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_AuditLog_LogID" ON public."AuditLog" USING btree ("LogID");


--
-- Name: ix_public_DataExports_ExportID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_DataExports_ExportID" ON public."DataExports" USING btree ("ExportID");


--
-- Name: ix_public_INSTATQuestions_QuestionID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_INSTATQuestions_QuestionID" ON public."INSTATQuestions" USING btree ("QuestionID");


--
-- Name: ix_public_INSTATSurveys_SurveyID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_INSTATSurveys_SurveyID" ON public."INSTATSurveys" USING btree ("SurveyID");


--
-- Name: ix_public_ParsingResult_ResultID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_ParsingResult_ResultID" ON public."ParsingResult" USING btree ("ResultID");


--
-- Name: ix_public_ParsingStatistics_StatID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_ParsingStatistics_StatID" ON public."ParsingStatistics" USING btree ("StatID");


--
-- Name: ix_public_Roles_RoleID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_Roles_RoleID" ON public."Roles" USING btree ("RoleID");


--
-- Name: ix_public_SurveyMetrics_MetricID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_SurveyMetrics_MetricID" ON public."SurveyMetrics" USING btree ("MetricID");


--
-- Name: ix_public_SurveyTemplates_TemplateID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_SurveyTemplates_TemplateID" ON public."SurveyTemplates" USING btree ("TemplateID");


--
-- Name: ix_public_Users_UserID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_Users_UserID" ON public."Users" USING btree ("UserID");


--
-- Name: ix_public_WorkflowActions_ActionID; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_public_WorkflowActions_ActionID" ON public."WorkflowActions" USING btree ("ActionID");


--
-- Name: AnswerOption AnswerOption_QuestionID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AnswerOption"
    ADD CONSTRAINT "AnswerOption_QuestionID_fkey" FOREIGN KEY ("QuestionID") REFERENCES public."Question"("QuestionID") ON DELETE CASCADE;


--
-- Name: Question Question_SectionID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Question"
    ADD CONSTRAINT "Question_SectionID_fkey" FOREIGN KEY ("SectionID") REFERENCES public."Section"("SectionID") ON DELETE CASCADE;


--
-- Name: Question Question_SubsectionID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Question"
    ADD CONSTRAINT "Question_SubsectionID_fkey" FOREIGN KEY ("SubsectionID") REFERENCES public."Subsection"("SubsectionID") ON DELETE CASCADE;


--
-- Name: ResponseDetail ResponseDetail_QuestionID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ResponseDetail"
    ADD CONSTRAINT "ResponseDetail_QuestionID_fkey" FOREIGN KEY ("QuestionID") REFERENCES public."Question"("QuestionID") ON DELETE CASCADE;


--
-- Name: ResponseDetail ResponseDetail_ResponseID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ResponseDetail"
    ADD CONSTRAINT "ResponseDetail_ResponseID_fkey" FOREIGN KEY ("ResponseID") REFERENCES public."Response"("ResponseID") ON DELETE CASCADE;


--
-- Name: ResponseDetail ResponseDetail_SelectedOptionID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ResponseDetail"
    ADD CONSTRAINT "ResponseDetail_SelectedOptionID_fkey" FOREIGN KEY ("SelectedOptionID") REFERENCES public."AnswerOption"("OptionID") ON DELETE SET NULL;


--
-- Name: Response Response_SurveyID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Response"
    ADD CONSTRAINT "Response_SurveyID_fkey" FOREIGN KEY ("SurveyID") REFERENCES public."Survey"("SurveyID") ON DELETE CASCADE;


--
-- Name: Section Section_SurveyID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Section"
    ADD CONSTRAINT "Section_SurveyID_fkey" FOREIGN KEY ("SurveyID") REFERENCES public."Survey"("SurveyID") ON DELETE CASCADE;


--
-- Name: Subsection Subsection_SectionID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Subsection"
    ADD CONSTRAINT "Subsection_SectionID_fkey" FOREIGN KEY ("SectionID") REFERENCES public."Section"("SectionID") ON DELETE CASCADE;


--
-- Name: mali_cercles mali_cercles_region_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mali_cercles
    ADD CONSTRAINT mali_cercles_region_code_fkey FOREIGN KEY (region_code) REFERENCES public.mali_regions(region_code);


--
-- Name: sds_activity_surveys sds_activity_surveys_cercle_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sds_activity_surveys
    ADD CONSTRAINT sds_activity_surveys_cercle_code_fkey FOREIGN KEY (cercle_code) REFERENCES public.mali_cercles(cercle_code);


--
-- Name: sds_activity_surveys sds_activity_surveys_data_collection_structure_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sds_activity_surveys
    ADD CONSTRAINT sds_activity_surveys_data_collection_structure_fkey FOREIGN KEY (data_collection_structure) REFERENCES public.instat_structures(structure_id);


--
-- Name: sds_activity_surveys sds_activity_surveys_implementing_structure_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sds_activity_surveys
    ADD CONSTRAINT sds_activity_surveys_implementing_structure_fkey FOREIGN KEY (implementing_structure) REFERENCES public.instat_structures(structure_id);


--
-- Name: sds_activity_surveys sds_activity_surveys_region_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sds_activity_surveys
    ADD CONSTRAINT sds_activity_surveys_region_code_fkey FOREIGN KEY (region_code) REFERENCES public.mali_regions(region_code);


--
-- PostgreSQL database dump complete
--

\unrestrict JqrhyTWnYwfAexGLQxgOIhjOegtawhTkvGfUEzPtxw9kxWWkNcotY6Ydq9V1nim

