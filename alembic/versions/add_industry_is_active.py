"""add is_active to industries

Revision ID: add_industry_is_active
Revises: add_admin_cms_auth
Create Date: 2025-01-XX

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_industry_is_active'
down_revision = 'add_admin_cms_auth'  # Chains from xxx_add_admin_cms_models.py
branch_labels = None
depends_on = None


def upgrade():
    # Add is_active column to industries table
    op.add_column('industries', sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'))
    # Create index for better query performance
    op.create_index('ix_industries_is_active', 'industries', ['is_active'])
    # Update all existing records to be active by default
    op.execute("UPDATE industries SET is_active = true WHERE is_active IS NULL")


def downgrade():
    # Drop index
    op.drop_index('ix_industries_is_active', table_name='industries')
    # Drop column
    op.drop_column('industries', 'is_active')

