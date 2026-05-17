"""
Modelos para el sistema de elecciones y votación.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float,
    ForeignKey, Boolean, UniqueConstraint, Enum
)
from sqlalchemy.orm import relationship
from app.models.configuracion import Base
from datetime import datetime
import enum


class TipoEleccionEnum(str, enum.Enum):
    CARGO = "cargo"       # Elección de cargos - candidatos son usuarios
    ACUERDO = "acuerdo"   # Elección de acuerdos - opciones libres


class EstadoEleccionEnum(str, enum.Enum):
    BORRADOR = "borrador"
    ACTIVO = "activo"
    CERRADO = "cerrado"


class MetodoValidacionEnum(str, enum.Enum):
    FACIAL = "facial"
    MANUAL = "manual"


class Eleccion(Base):
    __tablename__ = "elecciones"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=False)  # "cargo" | "acuerdo"
    estado = Column(String(50), default="borrador", nullable=False)  # borrador | activo | cerrado
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    electores = Column(String(50), default="todos", nullable=False)  # "todos" o id de grupo
    resultados_publicos = Column(Boolean, default=False)  # mostrar resultados mientras está activa
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    opciones = relationship("OpcionEleccion", back_populates="eleccion", cascade="all, delete-orphan")
    votos = relationship("Voto", back_populates="eleccion", cascade="all, delete-orphan")
    padron = relationship("PadronEleccion", back_populates="eleccion", cascade="all, delete-orphan")

    def to_dict(self, incluir_votos=False):
        data = {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "tipo": self.tipo,
            "estado": self.estado,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "resultados_publicos": self.resultados_publicos,
            "creado_por": self.creado_por,
            "created_at": self.created_at.isoformat(),
        }
        if incluir_votos:
            data["votos"] = [v.to_dict() for v in self.votos]
        return data


class OpcionEleccion(Base):
    __tablename__ = "opciones_eleccion"

    id = Column(Integer, primary_key=True)
    eleccion_id = Column(Integer, ForeignKey("elecciones.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # solo para cargo
    orden = Column(Integer, default=0)
    foto_url = Column(String(500), nullable=True)  # foto de candidato
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    eleccion = relationship("Eleccion", back_populates="opciones")
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    votos = relationship("Voto", back_populates="opcion")

    def to_dict(self, incluir_votos=False):
        data = {
            "id": self.id,
            "eleccion_id": self.eleccion_id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "usuario_id": self.usuario_id,
            "orden": self.orden,
            "foto_url": self.foto_url,
            "votos": 0,  # será poblado desde resultados
        }
        return data


class Voto(Base):
    __tablename__ = "votos"
    __table_args__ = (
        UniqueConstraint("usuario_id", "eleccion_id", name="uq_usuario_eleccion"),
    )

    id = Column(Integer, primary_key=True)
    eleccion_id = Column(Integer, ForeignKey("elecciones.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    opcion_id = Column(Integer, ForeignKey("opciones_eleccion.id"), nullable=False)
    metodo_validacion = Column(String(20), nullable=False)  # "facial" | "manual"
    foto_validacion = Column(String(500), nullable=True)  # ruta archivo (manual only)
    latitud = Column(Float, nullable=True)  # GPS (manual only)
    longitud = Column(Float, nullable=True)  # GPS (manual only)
    ip_address = Column(String(45), nullable=True)  # audit
    impugnado = Column(Boolean, default=False)
    motivo_impugnacion = Column(Text, nullable=True)
    impugnado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    impugnado_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    eleccion = relationship("Eleccion", back_populates="votos")
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    opcion = relationship("OpcionEleccion", back_populates="votos")

    def to_dict(self):
        return {
            "id": self.id,
            "eleccion_id": self.eleccion_id,
            "usuario_id": self.usuario_id,  # nunca exponemos esto en results
            "opcion_id": self.opcion_id,
            "metodo_validacion": self.metodo_validacion,
            "foto_validacion": self.foto_validacion,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "impugnado": self.impugnado,
            "motivo_impugnacion": self.motivo_impugnacion,
            "created_at": self.created_at.isoformat(),
        }


class PadronEleccion(Base):
    __tablename__ = "padron_eleccion"
    __table_args__ = (UniqueConstraint("eleccion_id", "usuario_id", name="uq_padron_elector"),)

    id = Column(Integer, primary_key=True)
    eleccion_id = Column(Integer, ForeignKey("elecciones.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    eleccion = relationship("Eleccion", back_populates="padron")
    usuario = relationship("Usuario", foreign_keys=[usuario_id])

    def to_dict(self):
        return {
            "id": self.id,
            "eleccion_id": self.eleccion_id,
            "usuario_id": self.usuario_id,
            "created_at": self.created_at.isoformat(),
        }
