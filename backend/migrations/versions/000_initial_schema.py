"""Initial schema creation for dynamic configuration system

Revision ID: 001
Revises:
Create Date: 2026-04-25

This migration creates the initial schema with all tables for the dynamic
configuration system. Since we're using SQLAlchemy ORM and Base.metadata.create_all(),
this migration documents the schema that was auto-created.

Tables:
- usuarios
- configuracion_campos
- integraciones_api
- consultas_externas
- campos_usuario
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """This migration is informational. The actual schema is created by
    app.db.database.init_db() via SQLAlchemy's Base.metadata.create_all()"""
    pass


def downgrade() -> None:
    """Drop all tables in reverse order of creation"""
    pass
