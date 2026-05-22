"""Add cobranza tables and fecha_inicio_cobranza to usuarios

Revision ID: 003
Revises: 002_add_usuario_biometric_fields
Create Date: 2026-04-25

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Add fecha_inicio_cobranza to usuarios
    op.add_column('usuarios', sa.Column('fecha_inicio_cobranza', sa.DateTime(), nullable=True))

    # Create conceptos_pago table
    op.create_table('conceptos_pago',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('monto', sa.Float(), nullable=False),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('recurrencia', sa.String(50), nullable=False),
        sa.Column('dia_cobro', sa.Integer(), nullable=True),
        sa.Column('cada_n_periodos', sa.Integer(), default=1),
        sa.Column('fecha_inicio', sa.DateTime(), nullable=False),
        sa.Column('fecha_fin', sa.DateTime(), nullable=True),
        sa.Column('activo', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_tipo', 'tipo'),
        sa.Index('idx_activo', 'activo')
    )

    # Create asignaciones_concepto table
    op.create_table('asignaciones_concepto',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('concepto_id', sa.Integer(), nullable=False),
        sa.Column('fecha_inicio', sa.DateTime(), nullable=False),
        sa.Column('fecha_fin', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['concepto_id'], ['conceptos_pago.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_usuario', 'usuario_id'),
        sa.Index('idx_concepto', 'concepto_id'),
        sa.UniqueConstraint('usuario_id', 'concepto_id', name='unique_usuario_concepto')
    )

    # Create cuotas table
    op.create_table('cuotas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('concepto_id', sa.Integer(), nullable=False),
        sa.Column('numero_cuota', sa.Integer(), nullable=False),
        sa.Column('monto', sa.Float(), nullable=False),
        sa.Column('fecha_vencimiento', sa.DateTime(), nullable=False),
        sa.Column('fecha_pagada', sa.DateTime(), nullable=True),
        sa.Column('estado', sa.String(50), default='pendiente'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['concepto_id'], ['conceptos_pago.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_usuario', 'usuario_id'),
        sa.Index('idx_estado', 'estado'),
        sa.Index('idx_fecha_vencimiento', 'fecha_vencimiento')
    )

    # Create pagos table
    op.create_table('pagos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cuota_id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('monto', sa.Float(), nullable=False),
        sa.Column('metodo_pago', sa.String(50), nullable=False),
        sa.Column('referencia', sa.String(255), nullable=True),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('estado', sa.String(50), default='pendiente_aprobacion'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['cuota_id'], ['cuotas.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_usuario', 'usuario_id'),
        sa.Index('idx_estado', 'estado'),
        sa.Index('idx_created_at', 'created_at')
    )


def downgrade():
    op.drop_table('pagos')
    op.drop_table('cuotas')
    op.drop_table('asignaciones_concepto')
    op.drop_table('conceptos_pago')
    op.drop_column('usuarios', 'fecha_inicio_cobranza')
