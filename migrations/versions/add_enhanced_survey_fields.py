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
    """Add enhanced survey fields and workflow support"""
    
    # Create WorkflowActions table if it doesn't exist
    try:
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
    except Exception:
        pass  # Table already exists
    
    # Add enhanced fields to public.Survey using try/except approach
    survey_columns_to_add = [
        ('UpdatedDate', sa.Column('UpdatedDate', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'))),
        ('CreatedBy', sa.Column('CreatedBy', sa.String(100))),
        ('ReviewedBy', sa.Column('ReviewedBy', sa.String(100))),
        ('ApprovedBy', sa.Column('ApprovedBy', sa.String(100))),
        ('PublishedBy', sa.Column('PublishedBy', sa.String(100))),
        ('ReviewDate', sa.Column('ReviewDate', sa.DateTime(timezone=True))),
        ('ApprovalDate', sa.Column('ApprovalDate', sa.DateTime(timezone=True))),
        ('PublicationDate', sa.Column('PublicationDate', sa.DateTime(timezone=True))),
        ('Language', sa.Column('Language', sa.String(10), server_default='fr')),
        ('Version', sa.Column('Version', sa.Integer(), server_default='1')),
        ('IsTemplate', sa.Column('IsTemplate', sa.Boolean(), server_default='false'))
    ]
    
    for col_name, col_def in survey_columns_to_add:
        try:
            op.add_column('Survey', col_def)
        except Exception:
            pass  # Column already exists
    
    # Update existing Status column to have default value
    try:
        op.alter_column('Survey', 'Status', server_default='draft')
    except Exception:
        pass  # Column might not exist or already have default
    
    # Create indexes if they don't exist
    try:
        op.create_index(op.f('ix_public_Users_UserID'), 'Users', ['UserID'], unique=False)
    except Exception:
        pass  # Index might already exist
        
    try:
        op.create_index(op.f('ix_public_Roles_RoleID'), 'Roles', ['RoleID'], unique=False)
    except Exception:
        pass  # Index might already exist


def downgrade() -> None:
    """Remove enhanced survey fields and workflow action table"""
    
    # Drop indexes if they exist
    try:
        op.drop_index(op.f('ix_public_Users_UserID'), table_name='Users')
    except Exception:
        pass
        
    try:
        op.drop_index(op.f('ix_public_Roles_RoleID'), table_name='Roles')
    except Exception:
        pass
    
    # Check what columns exist in Survey table
    conn = op.get_bind()
    survey_columns = conn.execute(
        sa.text("SELECT column_name FROM information_schema.columns WHERE table_name = 'Survey' AND table_schema = 'public'")
    ).fetchall()
    existing_columns = [row[0] for row in survey_columns]
    
    # Remove enhanced fields from public.Survey if they exist
    if 'IsTemplate' in existing_columns:
        op.drop_column('Survey', 'IsTemplate')
    if 'Version' in existing_columns:
        op.drop_column('Survey', 'Version')
    if 'Language' in existing_columns:
        op.drop_column('Survey', 'Language')
    if 'PublicationDate' in existing_columns:
        op.drop_column('Survey', 'PublicationDate')
    if 'ApprovalDate' in existing_columns:
        op.drop_column('Survey', 'ApprovalDate')
    if 'ReviewDate' in existing_columns:
        op.drop_column('Survey', 'ReviewDate')
    if 'PublishedBy' in existing_columns:
        op.drop_column('Survey', 'PublishedBy')
    if 'ApprovedBy' in existing_columns:
        op.drop_column('Survey', 'ApprovedBy')
    if 'ReviewedBy' in existing_columns:
        op.drop_column('Survey', 'ReviewedBy')
    if 'CreatedBy' in existing_columns:
        op.drop_column('Survey', 'CreatedBy')
    if 'UpdatedDate' in existing_columns:
        op.drop_column('Survey', 'UpdatedDate')
    
    # Check if WorkflowActions table exists and drop it
    result = conn.execute(
        sa.text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'WorkflowActions')")
    ).scalar()
    
    if result:
        op.drop_table('WorkflowActions')
    
    # Remove default value from Status column if it exists
    if 'Status' in existing_columns:
        op.alter_column('Survey', 'Status', server_default=None)
