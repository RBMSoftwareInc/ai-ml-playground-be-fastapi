"""add_content_projects_table

Revision ID: e159ce96208a
Revises: increase_use_case_icon_size
Create Date: 2026-01-08 13:17:37.303303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e159ce96208a'
down_revision: Union[str, None] = 'increase_use_case_icon_size'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if contentstatus enum exists
    conn = op.get_bind()
    result = conn.execute(sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM pg_type WHERE typname = 'contentstatus'
        )
    """))
    enum_exists = result.scalar()
    
    if not enum_exists:
        # Create ContentStatus enum
        op.execute("CREATE TYPE contentstatus AS ENUM ('draft', 'pending_review', 'approved', 'published', 'rejected', 'archived')")
    
    # Create content_projects table
    op.create_table(
        'content_projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('workspace_type', sa.String(length=50), nullable=False),
        sa.Column('workspace_id', sa.String(length=100), nullable=False),
        sa.Column('status', postgresql.ENUM('draft', 'pending_review', 'approved', 'published', 'rejected', 'archived', name='contentstatus', create_type=False), nullable=False, server_default='draft'),
        sa.Column('content_changes', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('change_summary', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('submitted_for_review_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('review_comments', sa.Text(), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('published_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['published_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    
    # Create indexes
    op.create_index('ix_content_projects_project_id', 'content_projects', ['project_id'], unique=True)
    op.create_index('ix_content_projects_status', 'content_projects', ['status'])
    op.create_index('ix_content_projects_workspace_type', 'content_projects', ['workspace_type'])
    op.create_index('ix_content_projects_workspace_id', 'content_projects', ['workspace_id'])
    op.create_index('ix_content_projects_created_at', 'content_projects', ['created_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_content_projects_created_at', table_name='content_projects')
    op.drop_index('ix_content_projects_workspace_id', table_name='content_projects')
    op.drop_index('ix_content_projects_workspace_type', table_name='content_projects')
    op.drop_index('ix_content_projects_status', table_name='content_projects')
    op.drop_index('ix_content_projects_project_id', table_name='content_projects')
    
    # Drop table
    op.drop_table('content_projects')
    
    # Note: We don't drop the enum as it might be used by other tables
