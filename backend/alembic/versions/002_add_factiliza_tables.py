"""Add Factiliza integration tables

Revision ID: 002
Revises: 001
Create Date: 2026-04-25 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Create factiliza_configuracion table
    op.create_table(
        'factiliza_configuracion',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('endpoint_url', sa.String(255), nullable=False),
        sa.Column('auth_token', sa.String(500), nullable=False),
        sa.Column('timeout_segundos', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('max_reintentos', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('activa', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    # Create factiliza_facturas table
    op.create_table(
        'factiliza_facturas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numero_factura', sa.String(50), nullable=False, unique=True),
        sa.Column('numero_documento_cliente', sa.String(20), nullable=False),
        sa.Column('tipo_documento', sa.String(20), nullable=False),
        sa.Column('monto_total', sa.Float(), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('detalles_json', sa.JSON(), nullable=True),
        sa.Column('respuesta_api', sa.JSON(), nullable=True),
        sa.Column('estado', sa.String(50), nullable=False, server_default='Emitida'),
        sa.Column('error_mensaje', sa.Text(), nullable=True),
        sa.Column('pdf_url', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero_factura', name='uq_numero_factura')
    )

    # Create index on numero_factura
    op.create_index(
        'ix_factiliza_facturas_numero_factura',
        'factiliza_facturas',
        ['numero_factura']
    )

    # Create factiliza_logs table
    op.create_table(
        'factiliza_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tipo_operacion', sa.String(50), nullable=True),
        sa.Column('numero_factura', sa.String(50), nullable=True),
        sa.Column('estado', sa.String(50), nullable=True),
        sa.Column('mensaje', sa.Text(), nullable=True),
        sa.Column('tiempo_respuesta_ms', sa.Integer(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_index('ix_factiliza_facturas_numero_factura', table_name='factiliza_facturas')
    op.drop_table('factiliza_logs')
    op.drop_table('factiliza_facturas')
    op.drop_table('factiliza_configuracion')
