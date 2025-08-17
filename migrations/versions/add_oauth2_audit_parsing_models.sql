-- Add OAuth2, audit logging, and parsing results models
-- Migration: Add new tables for enhanced security and tracking

-- Create audit_logs table
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

-- Create indexes for audit_logs
CREATE INDEX IF NOT EXISTS "idx_audit_logs_userid" ON audit_logs ("UserID");
CREATE INDEX IF NOT EXISTS "idx_audit_logs_action" ON audit_logs ("Action");
CREATE INDEX IF NOT EXISTS "idx_audit_logs_timestamp" ON audit_logs ("Timestamp");
CREATE INDEX IF NOT EXISTS "idx_audit_logs_resource" ON audit_logs ("Resource");

-- Create parsing_results table
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

-- Create indexes for parsing_results
CREATE INDEX IF NOT EXISTS "idx_parsing_results_userid" ON parsing_results ("UserID");
CREATE INDEX IF NOT EXISTS "idx_parsing_results_uploadedat" ON parsing_results ("UploadedAt");
CREATE INDEX IF NOT EXISTS "idx_parsing_results_status" ON parsing_results ("Status");
CREATE INDEX IF NOT EXISTS "idx_parsing_results_filename" ON parsing_results ("FileName");

-- Create parsing_statistics table
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

-- Create index for parsing_statistics
CREATE INDEX IF NOT EXISTS "idx_parsing_statistics_date" ON parsing_statistics ("Date");

-- Update Users table to ensure proper password hashing support
ALTER TABLE "Users" ADD COLUMN IF NOT EXISTS "HashedPassword" VARCHAR(255);

-- Create function to cleanup old parsing results (rolling retention - keep last 100)
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

-- Create trigger for automatic cleanup
DROP TRIGGER IF EXISTS trigger_cleanup_parsing_results ON parsing_results;
CREATE TRIGGER trigger_cleanup_parsing_results
    AFTER INSERT ON parsing_results
    FOR EACH STATEMENT
    EXECUTE FUNCTION cleanup_parsing_results();

-- Insert initial admin user if not exists (password: admin123!)
-- Password hash for 'admin123!' using bcrypt
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "Users" WHERE "Username" = 'admin') THEN
        INSERT INTO "Users" ("Username", "Email", "Role", "HashedPassword", "CreatedAt")
        VALUES (
            'admin',
            'admin@instat.gov.ml',
            'admin',
            '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj0kzOcQPQvO', -- admin123!
            CURRENT_TIMESTAMP
        );
    END IF;
END $$;

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON audit_logs TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON parsing_results TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON parsing_statistics TO postgres;
GRANT USAGE ON SEQUENCE audit_logs_LogID_seq TO postgres;
GRANT USAGE ON SEQUENCE parsing_results_ResultID_seq TO postgres;
GRANT USAGE ON SEQUENCE parsing_statistics_StatID_seq TO postgres;
