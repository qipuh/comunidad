"""Add biometric and DNI fields to usuario table

Revision ID: 002
Revises: 001
Create Date: 2026-04-25

This migration adds support for:
- DNI authentication (numero_dni)
- Factiliza data (fecha_nacimiento, sexo, estado_civil, direccion, departamento, provincia, distrito)
- Phone field (telefono)
- Facial recognition photos (foto_frontal, foto_lateral_izq, foto_lateral_der)
- Facial recognition flag (usar_reconocimiento_facial)
"""
from alembic import op
import sqlalchemy as sa


revision = '002'
down_revision = '000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add biometric and DNI fields to usuarios table"""
    op.add_column('usuarios', sa.Column('numero_dni', sa.String(20), nullable=True, unique=True, index=True))
    op.add_column('usuarios', sa.Column('telefono', sa.String(20), nullable=True))
    op.add_column('usuarios', sa.Column('fecha_nacimiento', sa.String(10), nullable=True))
    op.add_column('usuarios', sa.Column('sexo', sa.String(50), nullable=True))
    op.add_column('usuarios', sa.Column('estado_civil', sa.String(50), nullable=True))
    op.add_column('usuarios', sa.Column('direccion', sa.String(500), nullable=True))
    op.add_column('usuarios', sa.Column('departamento', sa.String(100), nullable=True))
    op.add_column('usuarios', sa.Column('provincia', sa.String(100), nullable=True))
    op.add_column('usuarios', sa.Column('distrito', sa.String(100), nullable=True))
    op.add_column('usuarios', sa.Column('foto_frontal', sa.String(500), nullable=True))
    op.add_column('usuarios', sa.Column('foto_lateral_izq', sa.String(500), nullable=True))
    op.add_column('usuarios', sa.Column('foto_lateral_der', sa.String(500), nullable=True))
    op.add_column('usuarios', sa.Column('usar_reconocimiento_facial', sa.Boolean(), default=False, nullable=False))


def downgrade() -> None:
    """Remove biometric and DNI fields from usuarios table"""
    op.drop_column('usuarios', 'numero_dni')
    op.drop_column('usuarios', 'telefono')
    op.drop_column('usuarios', 'fecha_nacimiento')
    op.drop_column('usuarios', 'sexo')
    op.drop_column('usuarios', 'estado_civil')
    op.drop_column('usuarios', 'direccion')
    op.drop_column('usuarios', 'departamento')
    op.drop_column('usuarios', 'provincia')
    op.drop_column('usuarios', 'distrito')
    op.drop_column('usuarios', 'foto_frontal')
    op.drop_column('usuarios', 'foto_lateral_izq')
    op.drop_column('usuarios', 'foto_lateral_der')
    op.drop_column('usuarios', 'usar_reconocimiento_facial')
