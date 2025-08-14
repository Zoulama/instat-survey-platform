"""Add enhanced survey fields and workflow support

Revision ID: add_enhanced_survey_fields
Revises: 
Create Date: 2025-08-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_enhanced_survey_fields'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add enhanced survey fields and workflow action table"""
    
    # Create WorkflowActions table in public schema
    op.create_table('WorkflowActions',
        sa.Column('ActionID', sa.Integer(), primary_key=True),
        sa.Column('SurveyID', sa.Integer(), nullable=False),
        sa.Column('SchemaName', sa.String(50), nullable=False),
        sa.Column('UserID', sa.String(100)),
        sa.Column('ActionType', sa.String(50), nullable=False),
        sa.Column('FromStatus', sa.String(50)),
        sa.Column('ToStatus', sa.String(50)),
        sa.Column('Comment', sa.Text()),
        sa.Column('Timestamp', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        schema='public'
    )
    
    # Add enhanced fields to survey_program.Survey
    op.add_column('Survey', sa.Column('UpdatedDate', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')), schema='survey_program')
    op.add_column('Survey', sa.Column('CreatedBy', sa.String(100)), schema='survey_program')
    op.add_column('Survey', sa.Column('ReviewedBy', sa.String(100)), schema='survey_program')
    op.add_column('Survey', sa.Column('ApprovedBy', sa.String(100)), schema='survey_program')
    op.add_column('Survey', sa.Column('PublishedBy', sa.String(100)), schema='survey_program')
    op.add_column('Survey', sa.Column('ReviewDate', sa.DateTime(timezone=True)), schema='survey_program')
    op.add_column('Survey', sa.Column('ApprovalDate', sa.DateTime(timezone=True)), schema='survey_program')
    op.add_column('Survey', sa.Column('PublicationDate', sa.DateTime(timezone=True)), schema='survey_program')
    op.add_column('Survey', sa.Column('Language', sa.String(10), server_default='fr'), schema='survey_program')
    op.add_column('Survey', sa.Column('Version', sa.Integer(), server_default='1'), schema='survey_program')
    op.add_column('Survey', sa.Column('IsTemplate', sa.Boolean(), server_default='false'), schema='survey_program')
    
    # Add enhanced fields to survey_balance.Survey
    op.add_column('Survey', sa.Column('UpdatedDate', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')), schema='survey_balance')
    op.add_column('Survey', sa.Column('CreatedBy', sa.String(100)), schema='survey_balance')
    op.add_column('Survey', sa.Column('ReviewedBy', sa.String(100)), schema='survey_balance')
    op.add_column('Survey', sa.Column('ApprovedBy', sa.String(100)), schema='survey_balance')
    op.add_column('Survey', sa.Column('PublishedBy', sa.String(100)), schema='survey_balance')
    op.add_column('Survey', sa.Column('ReviewDate', sa.DateTime(timezone=True)), schema='survey_balance')
    op.add_column('Survey', sa.Column('ApprovalDate', sa.DateTime(timezone=True)), schema='survey_balance')
    op.add_column('Survey', sa.Column('PublicationDate', sa.DateTime(timezone=True)), schema='survey_balance')
    op.add_column('Survey', sa.Column('Language', sa.String(10), server_default='fr'), schema='survey_balance')
    op.add_column('Survey', sa.Column('Version', sa.Integer(), server_default='1'), schema='survey_balance')
    op.add_column('Survey', sa.Column('IsTemplate', sa.Boolean(), server_default='false'), schema='survey_balance')
    
    # Add enhanced fields to survey_diagnostic.Survey
    op.add_column('Survey', sa.Column('UpdatedDate', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('CreatedBy', sa.String(100)), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('ReviewedBy', sa.String(100)), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('ApprovedBy', sa.String(100)), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('PublishedBy', sa.String(100)), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('ReviewDate', sa.DateTime(timezone=True)), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('ApprovalDate', sa.DateTime(timezone=True)), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('PublicationDate', sa.DateTime(timezone=True)), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('Language', sa.String(10), server_default='fr'), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('Version', sa.Integer(), server_default='1'), schema='survey_diagnostic')
    op.add_column('Survey', sa.Column('IsTemplate', sa.Boolean(), server_default='false'), schema='survey_diagnostic')
    
    # Update existing Status columns to have default values
    op.alter_column('Survey', 'Status', server_default='draft', schema='survey_program')
    op.alter_column('Survey', 'Status', server_default='draft', schema='survey_balance')
    op.alter_column('Survey', 'Status', server_default='draft', schema='survey_diagnostic')
    
    # Create indexes for Users and Roles tables
    op.create_index(op.f('ix_public_Users_UserID'), 'Users', ['UserID'], unique=False, schema='public')
    op.create_index(op.f('ix_public_Roles_RoleID'), 'Roles', ['RoleID'], unique=False, schema='public')


def downgrade() -> None:
    """Remove enhanced survey fields and workflow action table"""
    
    # Drop indexes
    op.drop_index(op.f('ix_public_Users_UserID'), table_name='Users', schema='public')
    op.drop_index(op.f('ix_public_Roles_RoleID'), table_name='Roles', schema='public')
    
    # Remove enhanced fields from survey_program.Survey
    op.drop_column('Survey', 'IsTemplate', schema='survey_program')
    op.drop_column('Survey', 'Version', schema='survey_program')
    op.drop_column('Survey', 'Language', schema='survey_program')
    op.drop_column('Survey', 'PublicationDate', schema='survey_program')
    op.drop_column('Survey', 'ApprovalDate', schema='survey_program')
    op.drop_column('Survey', 'ReviewDate', schema='survey_program')
    op.drop_column('Survey', 'PublishedBy', schema='survey_program')
    op.drop_column('Survey', 'ApprovedBy', schema='survey_program')
    op.drop_column('Survey', 'ReviewedBy', schema='survey_program')
    op.drop_column('Survey', 'CreatedBy', schema='survey_program')
    op.drop_column('Survey', 'UpdatedDate', schema='survey_program')
    
    # Remove enhanced fields from survey_balance.Survey
    op.drop_column('Survey', 'IsTemplate', schema='survey_balance')
    op.drop_column('Survey', 'Version', schema='survey_balance')
    op.drop_column('Survey', 'Language', schema='survey_balance')
    op.drop_column('Survey', 'PublicationDate', schema='survey_balance')
    op.drop_column('Survey', 'ApprovalDate', schema='survey_balance')
    op.drop_column('Survey', 'ReviewDate', schema='survey_balance')
    op.drop_column('Survey', 'PublishedBy', schema='survey_balance')
    op.drop_column('Survey', 'ApprovedBy', schema='survey_balance')
    op.drop_column('Survey', 'ReviewedBy', schema='survey_balance')
    op.drop_column('Survey', 'CreatedBy', schema='survey_balance')
    op.drop_column('Survey', 'UpdatedDate', schema='survey_balance')
    
    # Remove enhanced fields from survey_diagnostic.Survey
    op.drop_column('Survey', 'IsTemplate', schema='survey_diagnostic')
    op.drop_column('Survey', 'Version', schema='survey_diagnostic')
    op.drop_column('Survey', 'Language', schema='survey_diagnostic')
    op.drop_column('Survey', 'PublicationDate', schema='survey_diagnostic')
    op.drop_column('Survey', 'ApprovalDate', schema='survey_diagnostic')
    op.drop_column('Survey', 'ReviewDate', schema='survey_diagnostic')
    op.drop_column('Survey', 'PublishedBy', schema='survey_diagnostic')
    op.drop_column('Survey', 'ApprovedBy', schema='survey_diagnostic')
    op.drop_column('Survey', 'ReviewedBy', schema='survey_diagnostic')
    op.drop_column('Survey', 'CreatedBy', schema='survey_diagnostic')
    op.drop_column('Survey', 'UpdatedDate', schema='survey_diagnostic')
    
    # Drop WorkflowActions table
    op.drop_table('WorkflowActions', schema='public')
    
    # Remove default values from Status columns
    op.alter_column('Survey', 'Status', server_default=None, schema='survey_program')
    op.alter_column('Survey', 'Status', server_default=None, schema='survey_balance')
    op.alter_column('Survey', 'Status', server_default=None, schema='survey_diagnostic')
