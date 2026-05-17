"""
Modelos de Usuario.
Versión simplificada para soporte de campos dinámicos.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.configuracion import Base


class RolEnum(str, enum.Enum):
    """Roles de usuario"""
    ADMIN = "admin"
    USER = "user"
    USUARIO = "usuario"
    MODERATOR = "moderator"


class EstadoEnum(str, enum.Enum):
    """Estados de usuario"""
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    PENDIENTE = "pendiente"
    FALLECIDO = "fallecido"


class Usuario(Base):
    """
    Modelo de usuario base.
    Los campos personalizados se almacenan en la tabla campos_usuario.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    # Identidad
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    numero_dni = Column(String(20), unique=True, nullable=True, index=True)

    # Perfil - Nombres y Apellidos
    nombres = Column(String(255), nullable=True)
    apellido_paterno = Column(String(255), nullable=True)
    apellido_materno = Column(String(255), nullable=True)

    # Autenticación
    password_hash = Column(String(255), nullable=False)

    # Datos Personales
    telefono = Column(String(20), nullable=True)
    fecha_nacimiento = Column(String(10), nullable=True)
    sexo = Column(String(50), nullable=True)
    estado_civil = Column(String(50), nullable=True)
    direccion = Column(String(500), nullable=True)
    departamento = Column(String(100), nullable=True)
    provincia = Column(String(100), nullable=True)
    distrito = Column(String(100), nullable=True)
    anexo = Column(String(100), nullable=True)

    # Fotos para reconocimiento facial
    foto_url = Column(String(500), nullable=True)
    foto_frontal = Column(String(500), nullable=True)
    foto_lateral_izq = Column(String(500), nullable=True)
    foto_lateral_der = Column(String(500), nullable=True)

    # Autenticación biométrica
    usar_reconocimiento_facial = Column(Boolean, default=False)

    # Estado
    rol = Column(String(50), default="user")
    estado = Column(String(50), default="activo")

    # Cobranza
    fecha_inicio_cobranza = Column(DateTime, nullable=True)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    campos_personalizados = relationship(
        "CampoUsuario",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    consultas_externas = relationship(
        "ConsultaExterna",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    campos_creados = relationship(
        "ConfiguracionCampo",
        foreign_keys="ConfiguracionCampo.creado_por",
        back_populates=None
    )

    @property
    def nombre_completo(self):
        partes = [self.nombres, self.apellido_paterno, self.apellido_materno]
        return ' '.join(p for p in partes if p and p.strip()).upper()
