"""Add fecha_inicio_cobranza to usuarios table

Revision ID: 003
Revises: 002_add_factiliza_tables
Create Date: 2026-04-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002_add_factiliza_tables'
branch_labels = None
depends_on = None


def upgrade():
    # Add fecha_inicio_cobranza column to usuarios table
    op.add_column('usuarios', sa.Column('fecha_inicio_cobranza', sa.DateTime(), nullable=True))


def downgrade():
    # Remove fecha_inicio_cobranza column from usuarios table
    op.drop_column('usuarios', 'fecha_inicio_cobranza')
