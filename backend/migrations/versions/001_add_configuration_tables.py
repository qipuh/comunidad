"""Add configuration and API integration tables.

Revision ID: 001
Revises:
Create Date: 2026-04-25 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = '000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crear nuevas tablas"""

    # Crear ENUM types
    op.execute("CREATE TYPE tipodatoenum AS ENUM ('string', 'number', 'date', 'enum', 'boolean', 'email', 'phone', 'url')")
    op.execute("CREATE TYPE tipoapienum AS ENUM ('reniec', 'facturiza', 'sunat', 'custom')")
    op.execute("CREATE TYPE authtypeenum AS ENUM ('bearer', 'api_key', 'oauth2', 'basic')")

    # Crear tabla integraciones_api
    op.create_table(
        'integraciones_api',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False, unique=True),
        sa.Column('descripcion', sa.String(500), nullable=True),
        sa.Column('tipo', sa.Enum('reniec', 'facturiza', 'sunat', 'custom', name='tipoapienum'), nullable=False),
        sa.Column('endpoint_url', sa.String(500), nullable=False),
        sa.Column('auth_type', sa.Enum('bearer', 'api_key', 'oauth2', 'basic', name='authtypeenum'), nullable=False),
        sa.Column('auth_token', sa.String(500), nullable=False),
        sa.Column('activa', sa.Boolean(), default=True),
        sa.Column('timeout_segundos', sa.Integer(), default=30),
        sa.Column('max_reintentos', sa.Integer(), default=3),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_integraciones_api_nombre', 'nombre')
    )

    # Crear tabla configuracion_campos
    op.create_table(
        'configuracion_campos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre_campo', sa.String(100), nullable=False, unique=True),
        sa.Column('etiqueta', sa.String(255), nullable=False),
        sa.Column('descripcion', sa.String(500), nullable=True),
        sa.Column('tipo_dato', sa.Enum('string', 'number', 'date', 'enum', 'boolean', 'email', 'phone', 'url', name='tipodatoenum'), nullable=False),
        sa.Column('es_obligatorio', sa.Boolean(), default=False),
        sa.Column('expresion_regex', sa.String(500), nullable=True),
        sa.Column('valores_enum', sa.JSON(), nullable=True),
        sa.Column('posicion', sa.Integer(), default=0),
        sa.Column('api_integracion_id', sa.Integer(), sa.ForeignKey('integraciones_api.id'), nullable=True),
        sa.Column('campo_mapa_api', sa.String(100), nullable=True),
        sa.Column('mostrar_en_registro', sa.Boolean(), default=True),
        sa.Column('mostrar_en_perfil', sa.Boolean(), default=True),
        sa.Column('mostrar_en_reportes', sa.Boolean(), default=True),
        sa.Column('creado_por', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_configuracion_campos_nombre_campo', 'nombre_campo')
    )

    # Crear tabla consultas_externas
    op.create_table(
        'consultas_externas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('integracion_api_id', sa.Integer(), sa.ForeignKey('integraciones_api.id'), nullable=False),
        sa.Column('tipo_consulta', sa.String(50), nullable=False),
        sa.Column('parametro_busqueda', sa.String(255), nullable=False),
        sa.Column('respuesta_json', sa.JSON(), nullable=True),
        sa.Column('campos_mapeados', sa.JSON(), nullable=True),
        sa.Column('estado', sa.String(50), default='pendiente'),
        sa.Column('mensaje_error', sa.String(500), nullable=True),
        sa.Column('timestamp', sa.DateTime(), default=sa.func.now()),
        sa.Column('ip_origen', sa.String(45), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_consultas_externas_usuario_id', 'usuario_id'),
        sa.Index('ix_consultas_externas_integracion_api_id', 'integracion_api_id'),
        sa.Index('ix_consultas_externas_timestamp', 'timestamp')
    )

    # Crear tabla campos_usuario
    op.create_table(
        'campos_usuario',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('configuracion_campo_id', sa.Integer(), sa.ForeignKey('configuracion_campos.id'), nullable=False),
        sa.Column('valor', sa.String(1000), nullable=True),
        sa.Column('fue_validado_externamente', sa.Boolean(), default=False),
        sa.Column('consulta_externa_id', sa.Integer(), sa.ForeignKey('consultas_externas.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_campos_usuario_usuario_id', 'usuario_id'),
        sa.Index('ix_campos_usuario_configuracion_campo_id', 'configuracion_campo_id')
    )


def downgrade() -> None:
    """Eliminar nuevas tablas"""
    op.drop_table('campos_usuario')
    op.drop_table('consultas_externas')
    op.drop_table('configuracion_campos')
    op.drop_table('integraciones_api')
    op.execute("DROP TYPE IF EXISTS authtypeenum")
    op.execute("DROP TYPE IF EXISTS tipoapienum")
    op.execute("DROP TYPE IF EXISTS tipodatoenum")
