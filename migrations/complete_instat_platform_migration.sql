-- =====================================================================
-- INSTAT Survey Platform - Complete Database Migration
-- This script creates all required tables and structures for the platform
-- =====================================================================

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS public;

-- =====================================================================
-- CORE SURVEY SYSTEM TABLES
-- =====================================================================

-- Users table with enhanced fields for OAuth2
CREATE TABLE IF NOT EXISTS "Users" (
    "UserID" SERIAL PRIMARY KEY,
    "Username" VARCHAR(255) UNIQUE NOT NULL,
    "Email" VARCHAR(255) UNIQUE NOT NULL,
    "HashedPassword" VARCHAR(255) NOT NULL,
    "FirstName" VARCHAR(100) NOT NULL DEFAULT '',
    "LastName" VARCHAR(100) NOT NULL DEFAULT '',
    "Role" VARCHAR(50) NOT NULL DEFAULT 'readonly',
    "Status" VARCHAR(50) NOT NULL DEFAULT 'active',
    "Department" VARCHAR(100),
    "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "IsActive" BOOLEAN DEFAULT TRUE,
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "UpdatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "LastLogin" TIMESTAMP WITH TIME ZONE,
    "ProfileData" JSONB
);

-- Roles table
CREATE TABLE IF NOT EXISTS "Roles" (
    "RoleID" SERIAL PRIMARY KEY,
    "RoleName" VARCHAR(50) UNIQUE NOT NULL,
    "Description" TEXT,
    "Permissions" JSONB
);

-- Base Surveys table
CREATE TABLE IF NOT EXISTS "Surveys" (
    "SurveyID" SERIAL PRIMARY KEY,
    "Title" VARCHAR(255) NOT NULL,
    "Description" TEXT,
    "CreatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "UpdatedDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "CreatedBy" VARCHAR(100),
    "Status" VARCHAR(50) DEFAULT 'Draft'
);

-- INSTAT-specific surveys table
CREATE TABLE IF NOT EXISTS "INSTATSurveys" (
    "SurveyID" SERIAL PRIMARY KEY,
    "Title" VARCHAR(255) NOT NULL,
    "Description" TEXT,
    "Domain" VARCHAR(50) NOT NULL,
    "Category" VARCHAR(50) NOT NULL,
    "CreatedDate" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "UpdatedDate" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "Status" VARCHAR(50) DEFAULT 'draft',
    "FiscalYear" INTEGER,
    "ReportingCycle" VARCHAR(50),
    "CreatedBy" VARCHAR(100),
    "ReviewedBy" VARCHAR(100),
    "ApprovedBy" VARCHAR(100),
    "PublishedBy" VARCHAR(100),
    "ImplementingUnit" VARCHAR(100),
    "ReviewDate" TIMESTAMP WITH TIME ZONE,
    "ApprovalDate" TIMESTAMP WITH TIME ZONE,
    "PublicationDate" TIMESTAMP WITH TIME ZONE,
    "Language" VARCHAR(10) DEFAULT 'fr',
    "Version" VARCHAR(20) DEFAULT '1.0.0',
    "IsTemplate" BOOLEAN DEFAULT FALSE,
    "TargetAudience" JSONB,
    "GeographicScope" JSONB,
    "ComplianceFramework" JSONB,
    "InternationalStandards" JSONB,
    "RequiredSkills" JSONB,
    "BudgetCategory" VARCHAR(100),
    "EstimatedDuration" INTEGER,
    "DomainSpecificFields" JSONB
);

-- Survey Templates table
CREATE TABLE IF NOT EXISTS "SurveyTemplates" (
    "TemplateID" SERIAL PRIMARY KEY,
    "TemplateName" VARCHAR(255) NOT NULL,
    "Domain" VARCHAR(50) NOT NULL,
    "Category" VARCHAR(50) NOT NULL,
    "Version" VARCHAR(20) DEFAULT '1.0.0',
    "CreatedBy" VARCHAR(100),
    "CreatedDate" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "LastModified" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "ApprovedBy" VARCHAR(100),
    "ApprovalDate" TIMESTAMP WITH TIME ZONE,
    "Sections" JSONB,
    "DefaultQuestions" JSONB,
    "UsageCount" INTEGER DEFAULT 0,
    "LastUsed" TIMESTAMP WITH TIME ZONE,
    "UsageGuidelines" TEXT,
    "ExampleImplementations" JSONB,
    "IsActive" BOOLEAN DEFAULT TRUE
);

-- Sections table
CREATE TABLE IF NOT EXISTS "Sections" (
    "SectionID" SERIAL PRIMARY KEY,
    "SurveyID" INTEGER NOT NULL,
    "Title" VARCHAR(255) NOT NULL,
    "Description" TEXT,
    "OrderIndex" INTEGER DEFAULT 0,
    "SchemaName" VARCHAR(100),
    FOREIGN KEY ("SurveyID") REFERENCES "Surveys" ("SurveyID") ON DELETE CASCADE
);

-- Subsections table
CREATE TABLE IF NOT EXISTS "Subsections" (
    "SubsectionID" SERIAL PRIMARY KEY,
    "SectionID" INTEGER NOT NULL,
    "Title" VARCHAR(255) NOT NULL,
    "Description" TEXT,
    "OrderIndex" INTEGER DEFAULT 0,
    FOREIGN KEY ("SectionID") REFERENCES "Sections" ("SectionID") ON DELETE CASCADE
);

-- Questions table
CREATE TABLE IF NOT EXISTS "Questions" (
    "QuestionID" SERIAL PRIMARY KEY,
    "SurveyID" INTEGER,
    "SectionID" INTEGER,
    "SubsectionID" INTEGER,
    "QuestionText" TEXT NOT NULL,
    "QuestionType" VARCHAR(50) DEFAULT 'text',
    "IsRequired" BOOLEAN DEFAULT FALSE,
    "OrderIndex" INTEGER DEFAULT 0,
    "ValidationRules" TEXT,
    "SchemaName" VARCHAR(100)
);

-- Enhanced Questions table (INSTAT-specific)
CREATE TABLE IF NOT EXISTS "INSTATQuestions" (
    "QuestionID" SERIAL PRIMARY KEY,
    "SurveyID" INTEGER NOT NULL,
    "SectionID" INTEGER,
    "SubsectionID" INTEGER,
    "QuestionText" TEXT NOT NULL,
    "QuestionType" VARCHAR(50) DEFAULT 'text',
    "IsRequired" BOOLEAN DEFAULT FALSE,
    "OrderIndex" INTEGER DEFAULT 0,
    "ValidationRules" JSONB,
    "ConditionalLogic" JSONB,
    "TableReference" VARCHAR(50),
    "ReferenceFilter" JSONB,
    "HelpText" TEXT,
    "PlaceholderText" VARCHAR(255),
    "DefaultValue" TEXT,
    "MinLength" INTEGER,
    "MaxLength" INTEGER,
    "MinValue" NUMERIC,
    "MaxValue" NUMERIC,
    "AcceptedFormats" JSONB,
    "IsCalculated" BOOLEAN DEFAULT FALSE,
    "CalculationFormula" TEXT,
    "DependsOn" JSONB,
    "Tags" JSONB,
    "Metadata" JSONB
);

-- Answer Options table
CREATE TABLE IF NOT EXISTS "AnswerOptions" (
    "OptionID" SERIAL PRIMARY KEY,
    "QuestionID" INTEGER NOT NULL,
    "OptionText" VARCHAR(500) NOT NULL,
    "OptionValue" VARCHAR(255),
    "OrderIndex" INTEGER DEFAULT 0,
    "IsDefault" BOOLEAN DEFAULT FALSE,
    FOREIGN KEY ("QuestionID") REFERENCES "Questions" ("QuestionID") ON DELETE CASCADE
);

-- Responses table
CREATE TABLE IF NOT EXISTS "Responses" (
    "ResponseID" SERIAL PRIMARY KEY,
    "SurveyID" INTEGER NOT NULL,
    "QuestionID" INTEGER NOT NULL,
    "ResponseValue" TEXT,
    "RespondentID" VARCHAR(100),
    "SubmissionDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "SchemaName" VARCHAR(100)
);

-- Response Details table
CREATE TABLE IF NOT EXISTS "ResponseDetails" (
    "DetailID" SERIAL PRIMARY KEY,
    "ResponseID" INTEGER NOT NULL,
    "FieldName" VARCHAR(100),
    "FieldValue" TEXT,
    "DataType" VARCHAR(50),
    FOREIGN KEY ("ResponseID") REFERENCES "Responses" ("ResponseID") ON DELETE CASCADE
);

-- Workflow Actions table
CREATE TABLE IF NOT EXISTS "WorkflowActions" (
    "ActionID" SERIAL PRIMARY KEY,
    "SurveyID" INTEGER NOT NULL,
    "SchemaName" VARCHAR(100),
    "UserID" INTEGER,
    "ActionType" VARCHAR(100),
    "FromStatus" VARCHAR(50),
    "ToStatus" VARCHAR(50),
    "Comment" TEXT,
    "Timestamp" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- SECURITY AND AUDIT TABLES
-- =====================================================================

-- Audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    "LogID" SERIAL PRIMARY KEY,
    "UserID" INTEGER NOT NULL,
    "Username" VARCHAR(100) NOT NULL,
    "Action" VARCHAR(100) NOT NULL,
    "Resource" VARCHAR(100) NOT NULL,
    "ResourceID" VARCHAR(50),
    "Details" JSONB,
    "IPAddress" VARCHAR(45),
    "UserAgent" TEXT,
    "Timestamp" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "Success" BOOLEAN NOT NULL DEFAULT TRUE,
    "ErrorMessage" TEXT
);

-- Parsing results table with rolling retention
CREATE TABLE IF NOT EXISTS parsing_results (
    "ResultID" SERIAL PRIMARY KEY,
    "FileName" VARCHAR(255) NOT NULL,
    "FileSize" INTEGER,
    "FileHash" VARCHAR(64),
    "UserID" INTEGER NOT NULL,
    "Username" VARCHAR(100) NOT NULL,
    "ParsedStructure" JSONB NOT NULL,
    "ParsingMethod" VARCHAR(50) NOT NULL,
    "SurveyCreated" BOOLEAN DEFAULT FALSE,
    "TemplateCreated" BOOLEAN DEFAULT FALSE,
    "SurveyID" INTEGER,
    "TemplateID" INTEGER,
    "Domain" VARCHAR(50),
    "Category" VARCHAR(50),
    "SectionsCount" INTEGER DEFAULT 0,
    "SubsectionsCount" INTEGER DEFAULT 0,
    "QuestionsCount" INTEGER DEFAULT 0,
    "Status" VARCHAR(20) DEFAULT 'completed',
    "ProcessingTimeMs" FLOAT,
    "ErrorMessage" TEXT,
    "ValidationIssues" JSONB,
    "UploadedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "ProcessedAt" TIMESTAMP WITH TIME ZONE
);

-- Parsing statistics table
CREATE TABLE IF NOT EXISTS parsing_statistics (
    "StatID" SERIAL PRIMARY KEY,
    "Date" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "TotalUploads" INTEGER DEFAULT 0,
    "SuccessfulParses" INTEGER DEFAULT 0,
    "FailedParses" INTEGER DEFAULT 0,
    "StructuredParses" INTEGER DEFAULT 0,
    "BasicParses" INTEGER DEFAULT 0,
    "SurveysCreated" INTEGER DEFAULT 0,
    "TemplatesCreated" INTEGER DEFAULT 0,
    "AverageProcessingTime" FLOAT
);

-- =====================================================================
-- MALI REFERENCE TABLES (TableRef 01-09)
-- =====================================================================

-- TableRef 01: Strategic Axis Results
CREATE TABLE IF NOT EXISTS strategic_axis_results (
    id SERIAL PRIMARY KEY,
    result_id VARCHAR(50) UNIQUE NOT NULL,
    strategic_axis TEXT NOT NULL,
    operational_objective TEXT NOT NULL,
    expected_result TEXT NOT NULL,
    activity TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TableRef 02: INSTAT Structures
CREATE TABLE IF NOT EXISTS instat_structures (
    id SERIAL PRIMARY KEY,
    structure_id VARCHAR(20) UNIQUE NOT NULL,
    structure_name VARCHAR(255) NOT NULL,
    abbreviation VARCHAR(50),
    structure_type VARCHAR(100),
    responsible_for_collection BOOLEAN DEFAULT FALSE,
    contact_info JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TableRef 03: CMR Indicators
CREATE TABLE IF NOT EXISTS cmr_indicators (
    id SERIAL PRIMARY KEY,
    indicator_id VARCHAR(50) UNIQUE NOT NULL,
    indicator_name TEXT NOT NULL,
    category VARCHAR(100),
    measurement_unit VARCHAR(100),
    data_source VARCHAR(255),
    collection_frequency VARCHAR(50),
    responsible_structure VARCHAR(100),
    baseline_value VARCHAR(100),
    target_value VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TableRef 04: Operational Results
CREATE TABLE IF NOT EXISTS operational_results (
    id SERIAL PRIMARY KEY,
    result_code VARCHAR(50) UNIQUE NOT NULL,
    axis_code VARCHAR(20),
    objective_code VARCHAR(20),
    result_description TEXT NOT NULL,
    performance_indicators JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TableRef 05: Participating Structures
CREATE TABLE IF NOT EXISTS participating_structures (
    id SERIAL PRIMARY KEY,
    structure_code VARCHAR(20) UNIQUE NOT NULL,
    structure_name VARCHAR(255) NOT NULL,
    participation_type VARCHAR(100),
    role TEXT,
    contact_info TEXT,
    expertise_areas JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TableRef 06: Monitoring Indicators
CREATE TABLE IF NOT EXISTS monitoring_indicators (
    id SERIAL PRIMARY KEY,
    indicator_code VARCHAR(50) UNIQUE NOT NULL,
    indicator_name TEXT NOT NULL,
    category VARCHAR(100),
    measurement_method TEXT,
    reporting_frequency VARCHAR(50),
    target_value VARCHAR(100),
    data_collection_method TEXT,
    responsible_unit VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TableRef 07: Financing Sources
CREATE TABLE IF NOT EXISTS financing_sources (
    id SERIAL PRIMARY KEY,
    source_code VARCHAR(20) UNIQUE NOT NULL,
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(100),
    currency VARCHAR(10) DEFAULT 'FCFA',
    min_amount FLOAT,
    max_amount FLOAT,
    financing_conditions TEXT,
    contact_info JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TableRef 08: Mali Regions
CREATE TABLE IF NOT EXISTS mali_regions (
    id SERIAL PRIMARY KEY,
    region_code VARCHAR(10) UNIQUE NOT NULL,
    region_name VARCHAR(100) NOT NULL,
    region_capital VARCHAR(100),
    population INTEGER,
    surface FLOAT,
    status VARCHAR(20) DEFAULT 'active',
    coordinates JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- TableRef 09: Mali Cercles
CREATE TABLE IF NOT EXISTS mali_cercles (
    id SERIAL PRIMARY KEY,
    cercle_code VARCHAR(10) UNIQUE NOT NULL,
    cercle_name VARCHAR(100) NOT NULL,
    region_code VARCHAR(10),
    cercle_capital VARCHAR(100),
    population INTEGER,
    surface FLOAT,
    status VARCHAR(20) DEFAULT 'active',
    coordinates JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_code) REFERENCES mali_regions(region_code)
);

-- Survey responses with table references
CREATE TABLE IF NOT EXISTS survey_responses (
    id SERIAL PRIMARY KEY,
    survey_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    response_value TEXT,
    table_reference VARCHAR(50),
    reference_code VARCHAR(50),
    respondent_id VARCHAR(100),
    response_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_validated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- SDS Activity Survey model
CREATE TABLE IF NOT EXISTS sds_activity_surveys (
    id SERIAL PRIMARY KEY,
    fiche_number VARCHAR(50) NOT NULL,
    order_number INTEGER NOT NULL,
    total_fiches INTEGER NOT NULL,
    region_code VARCHAR(10),
    cercle_code VARCHAR(10),
    implementing_structure VARCHAR(20),
    data_collection_structure VARCHAR(20),
    activity_title TEXT,
    is_data_disaggregatable BOOLEAN,
    disaggregation_by_gender BOOLEAN,
    disaggregation_by_age BOOLEAN,
    disaggregation_by_sex BOOLEAN,
    disaggregation_by_disability BOOLEAN,
    disaggregation_by_decision_participation BOOLEAN,
    disaggregation_by_territory BOOLEAN,
    disaggregation_by_residence_area BOOLEAN,
    region_level BOOLEAN,
    cercle_level BOOLEAN,
    arrondissement_level BOOLEAN,
    commune_level BOOLEAN,
    urban_area BOOLEAN,
    rural_area BOOLEAN,
    financing_sources JSONB,
    activity_cost FLOAT,
    monitoring_indicators JSONB,
    completion_result VARCHAR(10),
    created_by VARCHAR(100),
    reviewed_by VARCHAR(100),
    approved_by VARCHAR(100),
    review_date TIMESTAMP WITH TIME ZONE,
    approval_date TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region_code) REFERENCES mali_regions(region_code),
    FOREIGN KEY (cercle_code) REFERENCES mali_cercles(cercle_code),
    FOREIGN KEY (implementing_structure) REFERENCES instat_structures(structure_id),
    FOREIGN KEY (data_collection_structure) REFERENCES instat_structures(structure_id)
);

-- Table reference mappings
CREATE TABLE IF NOT EXISTS table_reference_mappings (
    id SERIAL PRIMARY KEY,
    table_ref VARCHAR(20) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    model_class VARCHAR(100) NOT NULL,
    description TEXT,
    display_fields JSONB,
    search_fields JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================================

-- Audit logs indexes
CREATE INDEX IF NOT EXISTS idx_audit_logs_userid ON audit_logs ("UserID");
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs ("Action");
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs ("Timestamp");
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource ON audit_logs ("Resource");

-- Parsing results indexes
CREATE INDEX IF NOT EXISTS idx_parsing_results_userid ON parsing_results ("UserID");
CREATE INDEX IF NOT EXISTS idx_parsing_results_uploadedat ON parsing_results ("UploadedAt");
CREATE INDEX IF NOT EXISTS idx_parsing_results_status ON parsing_results ("Status");
CREATE INDEX IF NOT EXISTS idx_parsing_results_filename ON parsing_results ("FileName");

-- Parsing statistics index
CREATE INDEX IF NOT EXISTS idx_parsing_statistics_date ON parsing_statistics ("Date");

-- Survey system indexes
CREATE INDEX IF NOT EXISTS idx_surveys_status ON "Surveys" ("Status");
CREATE INDEX IF NOT EXISTS idx_instat_surveys_domain ON "INSTATSurveys" ("Domain");
CREATE INDEX IF NOT EXISTS idx_instat_surveys_category ON "INSTATSurveys" ("Category");
CREATE INDEX IF NOT EXISTS idx_instat_surveys_status ON "INSTATSurveys" ("Status");
CREATE INDEX IF NOT EXISTS idx_templates_domain_category ON "SurveyTemplates" ("Domain", "Category");

-- Users indexes
CREATE INDEX IF NOT EXISTS idx_users_status ON "Users" ("Status");
CREATE INDEX IF NOT EXISTS idx_users_role ON "Users" ("Role");
CREATE INDEX IF NOT EXISTS idx_users_department ON "Users" ("Department");

-- Mali reference data indexes
CREATE INDEX IF NOT EXISTS idx_mali_regions_code ON mali_regions (region_code);
CREATE INDEX IF NOT EXISTS idx_mali_cercles_code ON mali_cercles (cercle_code);
CREATE INDEX IF NOT EXISTS idx_mali_cercles_region ON mali_cercles (region_code);
CREATE INDEX IF NOT EXISTS idx_instat_structures_id ON instat_structures (structure_id);

-- =====================================================================
-- TRIGGERS AND FUNCTIONS
-- =====================================================================

-- Function to cleanup old parsing results (rolling retention - keep last 100)
CREATE OR REPLACE FUNCTION cleanup_parsing_results()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM parsing_results
    WHERE "ResultID" IN (
        SELECT "ResultID"
        FROM parsing_results
        ORDER BY "UploadedAt" DESC
        OFFSET 100
    );
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger for automatic cleanup of parsing results
DROP TRIGGER IF EXISTS trigger_cleanup_parsing_results ON parsing_results;
CREATE TRIGGER trigger_cleanup_parsing_results
    AFTER INSERT ON parsing_results
    FOR EACH STATEMENT
    EXECUTE FUNCTION cleanup_parsing_results();

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at timestamps
CREATE OR REPLACE TRIGGER update_strategic_axis_results_updated_at
    BEFORE UPDATE ON strategic_axis_results
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_instat_structures_updated_at
    BEFORE UPDATE ON instat_structures
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_mali_regions_updated_at
    BEFORE UPDATE ON mali_regions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE TRIGGER update_mali_cercles_updated_at
    BEFORE UPDATE ON mali_cercles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================================
-- INITIAL DATA SETUP
-- =====================================================================

-- Insert initial admin user if not exists (password: admin123!)
INSERT INTO "Users" ("Username", "Email", "FirstName", "LastName", "Role", "HashedPassword", "Status", "Department", "CreatedAt")
SELECT 'admin@instat.gov.ml', 'admin@instat.gov.ml', 'Admin', 'User', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj0kzOcQPQvO', 'active', 'IT', CURRENT_TIMESTAMP
WHERE NOT EXISTS (SELECT 1 FROM "Users" WHERE "Username" = 'admin@instat.gov.ml');

-- Insert default roles
INSERT INTO "Roles" ("RoleName", "Description", "Permissions") VALUES
    ('admin', 'Administrator with full access', '["admin", "upload:write", "templates:write", "context:write", "context:read", "users:admin", "surveys:read", "surveys:write", "surveys:delete"]'),
    ('manager', 'Manager with management permissions', '["upload:write", "templates:write", "context:write", "context:read", "surveys:read", "surveys:write"]'),
    ('data_scientist', 'Data scientist with analysis permissions', '["context:read", "surveys:read", "upload:write"]'),
    ('readonly', 'Read-only access', '["context:read", "surveys:read"]'),
    ('write', 'Write access user', '["upload:write", "templates:write", "surveys:write", "context:read", "surveys:read"]')
ON CONFLICT ("RoleName") DO NOTHING;

-- Insert table reference mappings
INSERT INTO table_reference_mappings (table_ref, table_name, model_class, description, display_fields, search_fields) VALUES
    ('TableRef:01', 'strategic_axis_results', 'StrategicAxisResultModel', 'Axe stratégique/Objectifs opérationnel/Résultats attendus du SDS', '["result_id", "strategic_axis", "operational_objective"]', '["strategic_axis", "operational_objective", "expected_result"]'),
    ('TableRef:02', 'instat_structures', 'INSTATStructureModel', 'Liste des Structures pour les revues SDS', '["structure_id", "structure_name", "abbreviation"]', '["structure_name", "abbreviation"]'),
    ('TableRef:03', 'cmr_indicators', 'CMRIndicatorModel', 'Indicateurs CMR', '["indicator_id", "indicator_name", "category"]', '["indicator_name", "category"]'),
    ('TableRef:04', 'operational_results', 'OperationalResultModel', 'Résultat attendu par Objectif opérationnel et Axe', '["result_code", "result_description"]', '["result_description"]'),
    ('TableRef:05', 'participating_structures', 'ParticipatingStructureModel', 'Autres structures devant participer à l''activité', '["structure_code", "structure_name", "participation_type"]', '["structure_name", "participation_type"]'),
    ('TableRef:06', 'monitoring_indicators', 'MonitoringIndicatorModel', 'Indicateur de Suivi-évaluation', '["indicator_code", "indicator_name", "category"]', '["indicator_name", "category"]'),
    ('TableRef:07', 'financing_sources', 'FinancingSourceModel', 'Sources de financement', '["source_code", "source_name", "source_type"]', '["source_name", "source_type"]'),
    ('TableRef:08', 'mali_regions', 'MaliRegionModel', 'Liste des régions selon le découpage administratif du Mali', '["region_code", "region_name", "region_capital"]', '["region_name", "region_capital"]'),
    ('TableRef:09', 'mali_cercles', 'MaliCercleModel', 'Liste des cercles selon le découpage administratif du Mali', '["cercle_code", "cercle_name", "region_code"]', '["cercle_name", "cercle_capital"]')
ON CONFLICT DO NOTHING;

-- =====================================================================
-- PERMISSIONS SETUP
-- =====================================================================

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Additional grants for specific tables
GRANT SELECT, INSERT, UPDATE, DELETE ON audit_logs TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON parsing_results TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON parsing_statistics TO postgres;
GRANT USAGE ON SEQUENCE audit_logs_LogID_seq TO postgres;
GRANT USAGE ON SEQUENCE parsing_results_ResultID_seq TO postgres;
GRANT USAGE ON SEQUENCE parsing_statistics_StatID_seq TO postgres;

-- =====================================================================
-- COMPLETION MESSAGE
-- =====================================================================

DO $$
BEGIN
    RAISE NOTICE 'INSTAT Survey Platform database migration completed successfully!';
    RAISE NOTICE 'Created tables: Users, Roles, Surveys, INSTATSurveys, SurveyTemplates, and all Mali reference tables';
    RAISE NOTICE 'Initial admin user created: username=admin, password=admin123!';
    RAISE NOTICE 'OAuth2 security, audit logging, and parsing results tracking enabled';
    RAISE NOTICE 'Ready for Mali reference data population script';
END $$;
