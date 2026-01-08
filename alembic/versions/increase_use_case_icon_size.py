"""increase use case icon column sizes

Revision ID: increase_use_case_icon_size
Revises: increase_industry_icon_size
Create Date: 2025-01-07

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'increase_use_case_icon_size'
down_revision = 'increase_industry_icon_size'
branch_labels = None
depends_on = None


def upgrade():
    # Increase icon column size from 10 to 50 characters for use_case_categories
    op.alter_column('use_case_categories', 'icon',
                    existing_type=sa.String(length=10),
                    type_=sa.String(length=50),
                    existing_nullable=True)
    
    # Increase icon column size from 10 to 50 characters for use_cases
    op.alter_column('use_cases', 'icon',
                    existing_type=sa.String(length=10),
                    type_=sa.String(length=50),
                    existing_nullable=True)
    
    # Make updated_at nullable for use_case_categories (if not already)
    op.alter_column('use_case_categories', 'updated_at',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    existing_nullable=True)
    
    # Make updated_at nullable for use_cases (if not already)
    op.alter_column('use_cases', 'updated_at',
                    existing_type=sa.DateTime(timezone=True),
                    nullable=True,
                    existing_nullable=True)


def downgrade():
    # Revert icon column sizes back to 10 characters
    op.alter_column('use_cases', 'icon',
                    existing_type=sa.String(length=50),
                    type_=sa.String(length=10),
                    existing_nullable=True)
    
    op.alter_column('use_case_categories', 'icon',
                    existing_type=sa.String(length=50),
                    type_=sa.String(length=10),
                    existing_nullable=True)

