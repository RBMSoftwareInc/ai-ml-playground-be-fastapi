"""increase industry icon column size

Revision ID: increase_industry_icon_size
Revises: add_industry_is_active
Create Date: 2025-01-07

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'increase_industry_icon_size'
down_revision = 'add_industry_is_active'
branch_labels = None
depends_on = None


def upgrade():
    # Increase icon column size from 10 to 50 characters
    op.alter_column('industries', 'icon',
                    existing_type=sa.String(length=10),
                    type_=sa.String(length=50),
                    existing_nullable=True)


def downgrade():
    # Revert icon column size back to 10 characters
    op.alter_column('industries', 'icon',
                    existing_type=sa.String(length=50),
                    type_=sa.String(length=10),
                    existing_nullable=True)

