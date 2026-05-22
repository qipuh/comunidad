"""Add num_padron to usuarios table

Revision ID: 004
Revises: 003
Create Date: 2026-05-21

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Add num_padron column to usuarios table
    op.add_column('usuarios', sa.Column('num_padron', sa.String(50), nullable=True, index=True))


def downgrade():
    # Remove num_padron column from usuarios table
    op.drop_column('usuarios', 'num_padron')
