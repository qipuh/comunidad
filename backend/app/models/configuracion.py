"""
Modelos para configuración dinámmica de campos e integraciones API.

Tablas:
- ConfiguracionCampo: Define qué campos se usan en registro
- IntegracionAPI: Credenciales y config de APIs externas
- ConsultaExterna: Auditoría de consultas a APIs
- CampoUsuario: Valores de campos personalizados por usuario
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

# Use declarative_base directly to avoid circular imports
Base = declarative_base()


class TipoDatoEnum(str, enum.Enum):
    """Tipos de datos soportados para campos"""
    STRING = "string"
    NUMBER = "number"
    DATE = "date"
    ENUM = "enum"
    BOOLEAN = "boolean"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"


class TipoAPIEnum(str, enum.Enum):
    """Tipos de integraciones API soportadas"""
    RENIEC = "reniec"
    FACTURIZA = "facturiza"
    SUNAT = "sunat"
    CUSTOM = "custom"


class AuthTypeEnum(str, enum.Enum):
    """Tipos de autenticación para APIs"""
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BASIC = "basic"


class ConfiguracionCampo(Base):
    """
    Define qué campos se mostrarán en el formulario de registro.

    Permite configurar dinámicamente:
    - Qué campos aparecen
    - Orden en formulario
    - Tipo de dato y validaciones
    - Integración con APIs (opcional)
    """
    __tablename__ = "configuracion_campos"

    id = Column(Integer, primary_key=True, index=True)

    # Identidad del campo
    nombre_campo = Column(String(100), unique=True, nullable=False, index=True)
    etiqueta = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)

    # Tipo y validación
    tipo_dato = Column(Enum(TipoDatoEnum), nullable=False)
    es_obligatorio = Column(Boolean, default=False)
    expresion_regex = Column(String(500), nullable=True)

    # Para campos enum: valores posibles
    valores_enum = Column(JSON, nullable=True)  # List[str]: ["opción1", "opción2"]

    # Orden en formulario
    posicion = Column(Integer, default=0)

    # Integración con API externa (opcional)
    api_integracion_id = Column(Integer, ForeignKey("integraciones_api.id"), nullable=True)
    campo_mapa_api = Column(String(100), nullable=True)  # Campo en la API remota

    # Visibilidad
    mostrar_en_registro = Column(Boolean, default=True)
    mostrar_en_perfil = Column(Boolean, default=True)
    mostrar_en_reportes = Column(Boolean, default=True)

    # Auditoría
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    api_integracion = relationship(
        "IntegracionAPI",
        back_populates="campos_configurados",
        foreign_keys=[api_integracion_id]
    )
    campos_usuario = relationship(
        "CampoUsuario",
        back_populates="configuracion",
        cascade="all, delete-orphan"
    )


class IntegracionAPI(Base):
    """
    Credenciales y configuración de integraciones con APIs externas.

    Soporta:
    - RENIEC: Consulta de DNI (Perú)
    - Facturiza: Consulta de RUC
    - SUNAT: Contribuyentes (Perú)
    - Custom: API personalizada
    """
    __tablename__ = "integraciones_api"

    id = Column(Integer, primary_key=True, index=True)

    # Identidad
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(500), nullable=True)
    tipo = Column(Enum(TipoAPIEnum), nullable=False)

    # Conectividad
    endpoint_url = Column(String(500), nullable=False)
    auth_type = Column(Enum(AuthTypeEnum), nullable=False)
    auth_token = Column(String(500), nullable=False)  # Encriptado en servicio

    # Comportamiento
    activa = Column(Boolean, default=True)
    timeout_segundos = Column(Integer, default=30)
    max_reintentos = Column(Integer, default=3)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    campos_configurados = relationship(
        "ConfiguracionCampo",
        back_populates="api_integracion",
        foreign_keys="ConfiguracionCampo.api_integracion_id"
    )
    consultas = relationship(
        "ConsultaExterna",
        back_populates="integracion",
        cascade="all, delete-orphan"
    )


class ConsultaExterna(Base):
    """
    Auditoría de todas las consultas realizadas a APIs externas.

    Registra:
    - Quién consultó
    - Qué consultó
    - Resultado
    - IP de origen
    - Timestamp
    """
    __tablename__ = "consultas_externas"

    id = Column(Integer, primary_key=True, index=True)

    # Identificación
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)
    integracion_api_id = Column(Integer, ForeignKey("integraciones_api.id"), nullable=False, index=True)

    # Detalles de la consulta
    tipo_consulta = Column(String(50), nullable=False)  # "documento", "empresa", "domicilio", etc.
    parametro_busqueda = Column(String(255), nullable=False)  # DNI, RUC, etc.

    # Respuesta
    respuesta_json = Column(JSON, nullable=True)  # Respuesta completa de la API
    campos_mapeados = Column(JSON, nullable=True)  # Campos que se auto-llenaron

    # Estado
    estado = Column(String(50), default="pendiente")  # "exitosa", "fallida", "pendiente"
    mensaje_error = Column(String(500), nullable=True)  # Si falló

    # Auditoría
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_origen = Column(String(45), nullable=True)  # IPv4 o IPv6

    # Relaciones
    usuario = relationship(
        "Usuario",
        back_populates="consultas_externas",
        foreign_keys=[usuario_id]
    )
    integracion = relationship(
        "IntegracionAPI",
        back_populates="consultas",
        foreign_keys=[integracion_api_id]
    )


class CampoUsuario(Base):
    """
    Almacena valores de campos personalizados para cada usuario.

    Permite:
    - Almacenar valores de campos dinámicos
    - Rastrear si fue validado externamente (de API)
    - Vincular con consulta externa que auto-llenó el dato
    """
    __tablename__ = "campos_usuario"

    id = Column(Integer, primary_key=True, index=True)

    # Identidad
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    configuracion_campo_id = Column(
        Integer,
        ForeignKey("configuracion_campos.id"),
        nullable=False,
        index=True
    )

    # Valor
    valor = Column(String(1000), nullable=True)  # El valor del campo (como string)

    # Validación externa
    fue_validado_externamente = Column(Boolean, default=False)
    consulta_externa_id = Column(Integer, ForeignKey("consultas_externas.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    configuracion = relationship(
        "ConfiguracionCampo",
        back_populates="campos_usuario",
        foreign_keys=[configuracion_campo_id]
    )
    consulta_externa = relationship(
        "ConsultaExterna",
        foreign_keys=[consulta_externa_id]
    )
