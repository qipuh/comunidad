"""
Rutas para gestión de cobranza y conceptos de pago.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.cobranza import (
    ConceptoPago, AsignacionConcepto, Cuota, Pago,
    TipoConcepto, Recurrencia, MetodoPago, EstadoCuota, EstadoPago
)
from app.models.usuario import Usuario
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/cobranza", tags=["cobranza"])


# Schemas Pydantic
class ConceptoPagoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    monto: float
    tipo: TipoConcepto
    recurrencia: Recurrencia
    dia_cobro: Optional[int] = None
    cada_n_periodos: int = 1
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None


class ConceptoPagoResponse(BaseModel):
    id: int
    nombre: str
    monto: float
    tipo: str
    recurrencia: str
    activo: bool

    class Config:
        from_attributes = True


class CuotaResponse(BaseModel):
    id: int
    numero_cuota: int
    monto: float
    fecha_vencimiento: datetime
    estado: str
    concepto_id: int

    class Config:
        from_attributes = True


class PagoCreate(BaseModel):
    cuota_id: int
    monto: float
    metodo_pago: MetodoPago
    referencia: Optional[str] = None
    observaciones: Optional[str] = None


class PagoResponse(BaseModel):
    id: int
    cuota_id: int
    monto: float
    metodo_pago: str
    estado: str
    created_at: datetime

    class Config:
        from_attributes = True


# Endpoints Conceptos de Pago
@router.get("/conceptos")
async def listar_conceptos(db: Session = Depends(get_db)):
    """Listar todos los conceptos de pago"""
    conceptos = db.query(ConceptoPago).order_by(ConceptoPago.created_at.desc()).all()
    return {
        "success": True,
        "data": [
            {
                "id": c.id,
                "nombre": c.nombre,
                "monto": c.monto,
                "tipo": c.tipo.value,
                "recurrencia": c.recurrencia.value,
                "activo": c.activo,
                "created_at": c.created_at.isoformat()
            }
            for c in conceptos
        ]
    }


@router.post("/conceptos")
async def crear_concepto(datos: ConceptoPagoCreate, db: Session = Depends(get_db)):
    """Crear nuevo concepto de pago"""
    concepto = ConceptoPago(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        monto=datos.monto,
        tipo=datos.tipo,
        recurrencia=datos.recurrencia,
        dia_cobro=datos.dia_cobro,
        cada_n_periodos=datos.cada_n_periodos,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin
    )
    db.add(concepto)
    db.commit()
    db.refresh(concepto)
    return {
        "success": True,
        "data": {
            "id": concepto.id,
            "nombre": concepto.nombre,
            "monto": concepto.monto
        }
    }


@router.get("/conceptos/{concepto_id}")
async def obtener_concepto(concepto_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un concepto"""
    concepto = db.query(ConceptoPago).filter(ConceptoPago.id == concepto_id).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")
    return {
        "success": True,
        "data": {
            "id": concepto.id,
            "nombre": concepto.nombre,
            "monto": concepto.monto,
            "tipo": concepto.tipo.value,
            "recurrencia": concepto.recurrencia.value,
            "dia_cobro": concepto.dia_cobro,
            "activo": concepto.activo
        }
    }


# Endpoints Asignación de Conceptos
@router.post("/asignar/{usuario_id}/{concepto_id}")
async def asignar_concepto(usuario_id: int, concepto_id: int, db: Session = Depends(get_db)):
    """Asignar un concepto (multa/derecho) a un usuario manualmente"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    concepto = db.query(ConceptoPago).filter(ConceptoPago.id == concepto_id).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")

    asignacion = AsignacionConcepto(
        concepto_id=concepto_id,
        usuario_id=usuario_id,
        fecha_inicio=datetime.utcnow()
    )
    db.add(asignacion)
    db.commit()
    return {
        "success": True,
        "message": "Concepto asignado al usuario"
    }


# Endpoints Cuotas
@router.get("/cuotas/{usuario_id}")
async def listar_cuotas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Listar todas las cuotas de un usuario"""
    cuotas = db.query(Cuota).filter(Cuota.usuario_id == usuario_id).order_by(Cuota.fecha_vencimiento).all()
    return {
        "success": True,
        "count": len(cuotas),
        "data": [
            {
                "id": c.id,
                "numero_cuota": c.numero_cuota,
                "monto": c.monto,
                "fecha_vencimiento": c.fecha_vencimiento.isoformat(),
                "estado": c.estado.value,
                "concepto": c.concepto.nombre
            }
            for c in cuotas
        ]
    }


# Endpoints Pagos
@router.post("/pagos")
async def registrar_pago(datos: PagoCreate, db: Session = Depends(get_db)):
    """Registrar un pago propuesto por usuario"""
    cuota = db.query(Cuota).filter(Cuota.id == datos.cuota_id).first()
    if not cuota:
        raise HTTPException(status_code=404, detail="Cuota no encontrada")

    pago = Pago(
        cuota_id=datos.cuota_id,
        usuario_id=cuota.usuario_id,
        monto=datos.monto,
        metodo_pago=datos.metodo_pago,
        referencia=datos.referencia,
        observaciones=datos.observaciones
    )
    db.add(pago)
    db.commit()
    db.refresh(pago)
    return {
        "success": True,
        "message": "Pago registrado, pendiente de aprobación",
        "data": {"id": pago.id}
    }


@router.get("/pagos/{usuario_id}")
async def listar_pagos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Listar pagos de un usuario"""
    pagos = db.query(Pago).filter(Pago.usuario_id == usuario_id).order_by(Pago.created_at.desc()).all()
    return {
        "success": True,
        "count": len(pagos),
        "data": [
            {
                "id": p.id,
                "cuota_id": p.cuota_id,
                "monto": p.monto,
                "metodo_pago": p.metodo_pago.value,
                "estado": p.estado.value,
                "created_at": p.created_at.isoformat()
            }
            for p in pagos
        ]
    }


@router.put("/pagos/{pago_id}/aprobar")
async def aprobar_pago(pago_id: int, db: Session = Depends(get_db)):
    """Aprobar un pago (admin)"""
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    pago.estado = EstadoPago.APROBADO
    pago.fecha_aprobacion = datetime.utcnow()
    pago.cuota.estado = EstadoCuota.PAGADA
    pago.cuota.fecha_pagada = datetime.utcnow()

    db.commit()
    return {
        "success": True,
        "message": "Pago aprobado"
    }


@router.put("/pagos/{pago_id}/rechazar")
async def rechazar_pago(pago_id: int, motivo: str, db: Session = Depends(get_db)):
    """Rechazar un pago (admin)"""
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    pago.estado = EstadoPago.RECHAZADO
    pago.motivo_rechazo = motivo
    db.commit()
    return {
        "success": True,
        "message": "Pago rechazado"
    }
