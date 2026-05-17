"""
Modelos para el sistema de reuniones y asistencia.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, UniqueConstraint, Enum
)
from sqlalchemy.orm import relationship
from app.models.configuracion import Base
from datetime import datetime
import enum


class TipoReunionEnum(str, enum.Enum):
    ASAMBLEA = "asamblea"
    REUNION = "reunion"
    ORDINARIA = "ordinaria"
    EXTRAORDINARIA = "extraordinaria"
    SESION = "sesion"


class EstadoReunionEnum(str, enum.Enum):
    PROGRAMADA = "programada"
    EN_CURSO = "en_curso"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


class Reunion(Base):
    __tablename__ = "reuniones"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    lugar = Column(String(255), nullable=True)
    tipo = Column(String(50), nullable=False)  # asamblea, reunion, ordinaria, extraordinaria, sesion
    estado = Column(String(50), default="programada", nullable=False)  # programada | en_curso | finalizada | cancelada
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    estados_usuario_permitidos = Column(String(255), default="activo", nullable=False)  # CSV: "activo,inactivo"
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    asistencias = relationship("AsistenciaReunion", back_populates="reunion", cascade="all, delete-orphan")
    creador = relationship("Usuario", foreign_keys=[creado_por])

    def to_dict(self, incluir_asistentes=False):
        data = {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "lugar": self.lugar,
            "tipo": self.tipo,
            "estado": self.estado,
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat(),
            "estados_usuario_permitidos": self.estados_usuario_permitidos.split(","),
            "creado_por": self.creado_por,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "total_asistentes": len(self.asistencias) if self.asistencias else 0,
        }
        if incluir_asistentes:
            data["asistentes"] = [a.to_dict(incluir_usuario=True) for a in self.asistencias]
        return data


class AsistenciaReunion(Base):
    __tablename__ = "asistencia_reuniones"
    __table_args__ = (
        UniqueConstraint("reunion_id", "usuario_id", name="uq_reunion_usuario"),
    )

    id = Column(Integer, primary_key=True)
    reunion_id = Column(Integer, ForeignKey("reuniones.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    fecha_hora_registro = Column(DateTime, default=datetime.utcnow, nullable=False)
    metodo_registro = Column(String(50), nullable=False)  # qr, facial, manual
    foto_validacion = Column(Text, nullable=True)  # base64 para facial

    # Relaciones
    reunion = relationship("Reunion", back_populates="asistencias")
    usuario = relationship("Usuario", foreign_keys=[usuario_id])

    def to_dict(self, incluir_usuario=False):
        data = {
            "id": self.id,
            "reunion_id": self.reunion_id,
            "usuario_id": self.usuario_id,
            "fecha_hora_registro": self.fecha_hora_registro.isoformat(),
            "metodo_registro": self.metodo_registro,
        }
        if incluir_usuario and self.usuario:
            data["usuario"] = {
                "id": self.usuario.id,
                "nombre_completo": self.usuario.nombre_completo,
                "numero_dni": self.usuario.numero_dni,
                "email": self.usuario.email,
                "estado": self.usuario.estado,
                "foto_url": self.usuario.foto_url,
            }
        return data
