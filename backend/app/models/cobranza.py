"""
Modelos para gestión de cobranza y conceptos de pago.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.configuracion import Base


class TipoConcepto(str, enum.Enum):
    """Tipos de conceptos de pago"""
    CUOTA = "cuota"
    MULTA = "multa"
    DERECHO = "derecho"


class Recurrencia(str, enum.Enum):
    """Tipos de recurrencia"""
    DIARIO = "diario"
    SEMANAL = "semanal"
    MENSUAL = "mensual"
    BIMESTRAL = "bimestral"
    TRIMESTRAL = "trimestral"
    SEMESTRAL = "semestral"
    ANUAL = "anual"


class MetodoPago(str, enum.Enum):
    """Métodos de pago disponibles"""
    EFECTIVO = "efectivo"
    TRANSFERENCIA = "transferencia"
    DEPOSITO = "deposito"
    BILLETERA_DIGITAL = "billetera_digital"


class EstadoCuota(str, enum.Enum):
    """Estados de una cuota"""
    PENDIENTE = "pendiente"
    PAGADA = "pagada"
    VENCIDA = "vencida"
    ANULADA = "anulada"


class EstadoPago(str, enum.Enum):
    """Estados de un pago"""
    PENDIENTE_APROBACION = "pendiente_aprobacion"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


class ConceptoPago(Base):
    """Concepto de pago (plantilla)"""
    __tablename__ = "conceptos_pago"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    monto = Column(Float, nullable=False)
    tipo = Column(SQLEnum(TipoConcepto), nullable=False)
    recurrencia = Column(SQLEnum(Recurrencia), nullable=False)

    # Para cuotas: día del mes (1-31, 0 = último día)
    dia_cobro = Column(Integer, nullable=True)

    # Para recurrencias personalizadas (ej: cada 2 meses)
    cada_n_periodos = Column(Integer, default=1)

    # Fechas de vigencia
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)

    # Estado
    activo = Column(Boolean, default=True)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    cuotas = relationship("Cuota", back_populates="concepto", cascade="all, delete-orphan")
    asignaciones = relationship("AsignacionConcepto", back_populates="concepto", cascade="all, delete-orphan")


class AsignacionConcepto(Base):
    """Asignación de un concepto a un usuario"""
    __tablename__ = "asignaciones_concepto"

    id = Column(Integer, primary_key=True, index=True)
    concepto_id = Column(Integer, ForeignKey("conceptos_pago.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Fechas de vigencia para este usuario
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)

    # Estado
    activa = Column(Boolean, default=True)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    concepto = relationship("ConceptoPago", back_populates="asignaciones")


class Cuota(Base):
    """Cuota generada de un concepto para un usuario"""
    __tablename__ = "cuotas"

    id = Column(Integer, primary_key=True, index=True)
    concepto_id = Column(Integer, ForeignKey("conceptos_pago.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)

    # Información
    numero_cuota = Column(Integer, nullable=False)  # 1, 2, 3... o único para multas/derechos
    monto = Column(Float, nullable=False)
    descripcion = Column(String(255), nullable=True)

    # Fechas
    fecha_vencimiento = Column(DateTime, nullable=False)
    fecha_pagada = Column(DateTime, nullable=True)

    # Estado
    estado = Column(SQLEnum(EstadoCuota), default=EstadoCuota.PENDIENTE)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    concepto = relationship("ConceptoPago", back_populates="cuotas")
    pagos = relationship("Pago", back_populates="cuota", cascade="all, delete-orphan")


class Pago(Base):
    """Registro de un pago de una cuota"""
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    cuota_id = Column(Integer, ForeignKey("cuotas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)

    # Información de pago
    monto = Column(Float, nullable=False)
    metodo_pago = Column(SQLEnum(MetodoPago), nullable=False)
    referencia = Column(String(255), nullable=True)  # número de transferencia, cheque, etc.
    observaciones = Column(Text, nullable=True)

    # Estado
    estado = Column(SQLEnum(EstadoPago), default=EstadoPago.PENDIENTE_APROBACION)

    # Usuario que aprueba/rechaza
    aprobado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_aprobacion = Column(DateTime, nullable=True)
    motivo_rechazo = Column(Text, nullable=True)

    # Comprobante
    comprobante_pdf = Column(String(500), nullable=True)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    cuota = relationship("Cuota", back_populates="pagos")
