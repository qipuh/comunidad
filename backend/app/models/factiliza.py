from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from app.models.configuracion import Base


class FactilizaConfiguracion(Base):
    __tablename__ = "factiliza_configuracion"

    id = Column(Integer, primary_key=True, index=True)
    endpoint_url = Column(String(255), nullable=False)
    auth_token = Column(String(500), nullable=False)
    timeout_segundos = Column(Integer, default=30)
    max_reintentos = Column(Integer, default=3)
    activa = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class FactilizaConsultaDNI(Base):
    __tablename__ = "factiliza_consultas_dni"

    id = Column(Integer, primary_key=True, index=True)
    numero_dni = Column(String(8), nullable=False, index=True)
    nombre_completo = Column(String(255))
    fecha_nacimiento = Column(String(10))
    sexo = Column(String(1))
    direccion = Column(Text)
    departamento = Column(String(100))
    provincia = Column(String(100))
    distrito = Column(String(100))
    estado_civil = Column(String(50))
    edad = Column(Integer)
    respuesta_api = Column(JSON)
    estado = Column(String(50), default='Exitosa')
    error_mensaje = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class FactilizaLog(Base):
    __tablename__ = "factiliza_logs"

    id = Column(Integer, primary_key=True, index=True)
    tipo_operacion = Column(String(50))
    numero_dni = Column(String(8))
    estado = Column(String(50))
    mensaje = Column(Text)
    tiempo_respuesta_ms = Column(Integer)
    error = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
