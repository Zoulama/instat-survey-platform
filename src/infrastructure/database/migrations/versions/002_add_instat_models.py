"""Add INSTAT-specific models

Revision ID: 002
Revises: 001
Create Date: 2024-12-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_instat_models'
down_revision = 'add_enhanced_survey_fields'
branch_labels = None
depends_on = None


def upgrade():
    # Create INSTATSurveys table
    op.create_table('INSTATSurveys',
        sa.Column('SurveyID', sa.Integer(), nullable=False),
        sa.Column('Title', sa.String(length=255), nullable=False),
        sa.Column('Description', sa.Text(), nullable=True),
        sa.Column('Domain', sa.String(length=50), nullable=False),
        sa.Column('Category', sa.String(length=50), nullable=False),
        sa.Column('CreatedDate', sa.DateTime(), nullable=True),
        sa.Column('UpdatedDate', sa.DateTime(), nullable=True),
        sa.Column('Status', sa.String(length=50), nullable=True),
        sa.Column('FiscalYear', sa.Integer(), nullable=True),
        sa.Column('ReportingCycle', sa.String(length=50), nullable=True),
        sa.Column('CreatedBy', sa.String(length=100), nullable=True),
        sa.Column('ReviewedBy', sa.String(length=100), nullable=True),
        sa.Column('ApprovedBy', sa.String(length=100), nullable=True),
        sa.Column('PublishedBy', sa.String(length=100), nullable=True),
        sa.Column('ImplementingUnit', sa.String(length=100), nullable=True),
        sa.Column('ReviewDate', sa.DateTime(), nullable=True),
        sa.Column('ApprovalDate', sa.DateTime(), nullable=True),
        sa.Column('PublicationDate', sa.DateTime(), nullable=True),
        sa.Column('Language', sa.String(length=10), nullable=True),
        sa.Column('Version', sa.String(length=20), nullable=True),
        sa.Column('IsTemplate', sa.Boolean(), nullable=True),
        sa.Column('TargetAudience', sa.JSON(), nullable=True),
        sa.Column('GeographicScope', sa.JSON(), nullable=True),
        sa.Column('ComplianceFramework', sa.JSON(), nullable=True),
        sa.Column('InternationalStandards', sa.JSON(), nullable=True),
        sa.Column('RequiredSkills', sa.JSON(), nullable=True),
        sa.Column('BudgetCategory', sa.String(length=100), nullable=True),
        sa.Column('EstimatedDuration', sa.Integer(), nullable=True),
        sa.Column('DomainSpecificFields', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('SurveyID'),
        schema='public'
    )
    op.create_index(op.f('ix_public_INSTATSurveys_SurveyID'), 'INSTATSurveys', ['SurveyID'], unique=False, schema='public')

    # Create SurveyTemplates table
    op.create_table('SurveyTemplates',
        sa.Column('TemplateID', sa.Integer(), nullable=False),
        sa.Column('TemplateName', sa.String(length=255), nullable=False),
        sa.Column('Domain', sa.String(length=50), nullable=False),
        sa.Column('Category', sa.String(length=50), nullable=False),
        sa.Column('Version', sa.String(length=20), nullable=True),
        sa.Column('CreatedBy', sa.String(length=100), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=True),
        sa.Column('LastModified', sa.DateTime(), nullable=True),
        sa.Column('ApprovedBy', sa.String(length=100), nullable=True),
        sa.Column('ApprovalDate', sa.DateTime(), nullable=True),
        sa.Column('Sections', sa.JSON(), nullable=True),
        sa.Column('DefaultQuestions', sa.JSON(), nullable=True),
        sa.Column('UsageCount', sa.Integer(), nullable=True),
        sa.Column('LastUsed', sa.DateTime(), nullable=True),
        sa.Column('UsageGuidelines', sa.Text(), nullable=True),
        sa.Column('ExampleImplementations', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('TemplateID'),
        schema='public'
    )
    op.create_index(op.f('ix_public_SurveyTemplates_TemplateID'), 'SurveyTemplates', ['TemplateID'], unique=False, schema='public')

    # Create INSTATQuestions table
    op.create_table('INSTATQuestions',
        sa.Column('QuestionID', sa.Integer(), nullable=False),
        sa.Column('SurveyID', sa.Integer(), nullable=False),
        sa.Column('SectionID', sa.Integer(), nullable=True),
        sa.Column('SubsectionID', sa.Integer(), nullable=True),
        sa.Column('QuestionText', sa.Text(), nullable=False),
        sa.Column('QuestionType', sa.String(length=50), nullable=False),
        sa.Column('IsRequired', sa.Boolean(), nullable=True),
        sa.Column('IndicatorCode', sa.String(length=100), nullable=True),
        sa.Column('DataSource', sa.String(length=255), nullable=True),
        sa.Column('CollectionMethod', sa.String(length=100), nullable=True),
        sa.Column('QualityRequirements', sa.JSON(), nullable=True),
        sa.Column('ValidationRules', sa.JSON(), nullable=True),
        sa.Column('DependsOnQuestion', sa.Integer(), nullable=True),
        sa.Column('QuestionTextEN', sa.Text(), nullable=True),
        sa.Column('QuestionTextFR', sa.Text(), nullable=True),
        sa.Column('Tags', sa.JSON(), nullable=True),
        sa.Column('Priority', sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint('QuestionID'),
        schema='public'
    )
    op.create_index(op.f('ix_public_INSTATQuestions_QuestionID'), 'INSTATQuestions', ['QuestionID'], unique=False, schema='public')

    # Create SurveyMetrics table
    op.create_table('SurveyMetrics',
        sa.Column('MetricID', sa.Integer(), nullable=False),
        sa.Column('SurveyID', sa.Integer(), nullable=False),
        sa.Column('TotalResponses', sa.Integer(), nullable=True),
        sa.Column('CompletionRate', sa.Float(), nullable=True),
        sa.Column('AverageCompletionTime', sa.Float(), nullable=True),
        sa.Column('DataQualityScore', sa.Float(), nullable=True),
        sa.Column('ValidationErrorRate', sa.Float(), nullable=True),
        sa.Column('IncompleteResponses', sa.Integer(), nullable=True),
        sa.Column('ResponseByRegion', sa.JSON(), nullable=True),
        sa.Column('ResponseTrend', sa.JSON(), nullable=True),
        sa.Column('DataCollectionCost', sa.Float(), nullable=True),
        sa.Column('TimeToComplete', sa.Integer(), nullable=True),
        sa.Column('CoverageRate', sa.Float(), nullable=True),
        sa.Column('LastUpdated', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('MetricID'),
        schema='public'
    )
    op.create_index(op.f('ix_public_SurveyMetrics_MetricID'), 'SurveyMetrics', ['MetricID'], unique=False, schema='public')

    # Create DataExports table
    op.create_table('DataExports',
        sa.Column('ExportID', sa.Integer(), nullable=False),
        sa.Column('SurveyID', sa.Integer(), nullable=False),
        sa.Column('ExportFormat', sa.String(length=20), nullable=False),
        sa.Column('ExportType', sa.String(length=50), nullable=False),
        sa.Column('ExportConfig', sa.JSON(), nullable=True),
        sa.Column('IsScheduled', sa.Boolean(), nullable=True),
        sa.Column('ScheduleFrequency', sa.String(length=50), nullable=True),
        sa.Column('NextExport', sa.DateTime(), nullable=True),
        sa.Column('DeliveryMethod', sa.String(length=50), nullable=True),
        sa.Column('Recipients', sa.JSON(), nullable=True),
        sa.Column('CreatedBy', sa.String(length=100), nullable=True),
        sa.Column('CreatedDate', sa.DateTime(), nullable=True),
        sa.Column('LastExported', sa.DateTime(), nullable=True),
        sa.Column('ExportCount', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('ExportID'),
        schema='public'
    )
    op.create_index(op.f('ix_public_DataExports_ExportID'), 'DataExports', ['ExportID'], unique=False, schema='public')


def downgrade():
    # Drop indexes first
    op.drop_index(op.f('ix_public_DataExports_ExportID'), table_name='DataExports', schema='public')
    op.drop_index(op.f('ix_public_SurveyMetrics_MetricID'), table_name='SurveyMetrics', schema='public')
    op.drop_index(op.f('ix_public_INSTATQuestions_QuestionID'), table_name='INSTATQuestions', schema='public')
    op.drop_index(op.f('ix_public_SurveyTemplates_TemplateID'), table_name='SurveyTemplates', schema='public')
    op.drop_index(op.f('ix_public_INSTATSurveys_SurveyID'), table_name='INSTATSurveys', schema='public')
    
    # Drop tables
    op.drop_table('DataExports', schema='public')
    op.drop_table('SurveyMetrics', schema='public')
    op.drop_table('INSTATQuestions', schema='public')
    op.drop_table('SurveyTemplates', schema='public')
    op.drop_table('INSTATSurveys', schema='public')
