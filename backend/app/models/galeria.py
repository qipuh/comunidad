"""
Modelos para Galerías (Álbumes) y Fotografías de la Comunidad.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.configuracion import Base
from datetime import datetime


class Galeria(Base):
    __tablename__ = "galerias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=False, default="comunidad")
    categoria_label = Column(String(100), nullable=False, default="Comunidad")
    portada = Column(String(500), nullable=True)
    fecha = Column(String(100), nullable=True)
    lugar = Column(String(200), nullable=True)
    destacada = Column(Boolean, default=False)
    orden = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación 1 a muchos con fotos
    fotos = relationship("FotoGaleria", back_populates="galeria", cascade="all, delete-orphan", order_by="FotoGaleria.orden.asc()")


class FotoGaleria(Base):
    __tablename__ = "galeria_fotos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    galeria_id = Column(Integer, ForeignKey("galerias.id", ondelete="CASCADE"), nullable=True, index=True)
    titulo = Column(String(255), nullable=False)
    desc = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=False, default="comunidad")
    categoria_label = Column(String(100), nullable=False, default="Comunidad")
    img = Column(String(500), nullable=False)
    grande = Column(Boolean, default=False)
    orden = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    galeria = relationship("Galeria", back_populates="fotos")
