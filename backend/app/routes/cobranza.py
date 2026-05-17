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
from dateutil.relativedelta import relativedelta

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
    activo: bool = True


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
        fecha_fin=datos.fecha_fin,
        activo=datos.activo
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


@router.put("/conceptos/{concepto_id}")
async def actualizar_concepto(concepto_id: int, datos: ConceptoPagoCreate, db: Session = Depends(get_db)):
    """Actualizar un concepto de pago"""
    concepto = db.query(ConceptoPago).filter(ConceptoPago.id == concepto_id).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")

    concepto.nombre = datos.nombre
    concepto.descripcion = datos.descripcion
    concepto.monto = datos.monto
    concepto.tipo = datos.tipo
    concepto.recurrencia = datos.recurrencia
    concepto.dia_cobro = datos.dia_cobro
    concepto.cada_n_periodos = datos.cada_n_periodos
    concepto.fecha_inicio = datos.fecha_inicio
    concepto.fecha_fin = datos.fecha_fin
    concepto.activo = datos.activo

    db.commit()
    return {"success": True, "message": "Concepto actualizado"}


@router.delete("/conceptos/{concepto_id}")
async def eliminar_concepto(concepto_id: int, db: Session = Depends(get_db)):
    """Eliminar un concepto de pago"""
    concepto = db.query(ConceptoPago).filter(ConceptoPago.id == concepto_id).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")

    db.delete(concepto)
    db.commit()
    return {"success": True, "message": "Concepto eliminado"}


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


class AsignacionesRequest(BaseModel):
    fecha_inicio_cobranza: datetime
    conceptos_multas_derechos: List[int] = []


def siguiente_fecha_cuota(fecha_base: datetime, recurrencia: Recurrencia, cada_n: int) -> datetime:
    """Calcula la siguiente fecha de cuota dado una base y recurrencia"""
    if recurrencia == Recurrencia.DIARIO:
        return fecha_base + relativedelta(days=cada_n)
    elif recurrencia == Recurrencia.SEMANAL:
        return fecha_base + relativedelta(weeks=cada_n)
    elif recurrencia == Recurrencia.MENSUAL:
        return fecha_base + relativedelta(months=cada_n)
    elif recurrencia == Recurrencia.BIMESTRAL:
        return fecha_base + relativedelta(months=cada_n * 2)
    elif recurrencia == Recurrencia.TRIMESTRAL:
        return fecha_base + relativedelta(months=3 * cada_n)
    elif recurrencia == Recurrencia.SEMESTRAL:
        return fecha_base + relativedelta(months=6 * cada_n)
    elif recurrencia == Recurrencia.ANUAL:
        return fecha_base + relativedelta(years=cada_n)
    return fecha_base


def generar_cuotas_usuario(db: Session, usuario_id: int, concepto_id: int, fecha_inicio: datetime):
    """Generar cuotas para un usuario desde fecha_inicio hasta hoy + 1 periodo adelante."""
    concepto = db.query(ConceptoPago).filter(ConceptoPago.id == concepto_id).first()
    if not concepto or concepto.tipo != TipoConcepto.CUOTA:
        return

    cada_n = concepto.cada_n_periodos or 1
    # Fecha hasta la que generar: hoy + 1 periodo adelante
    fecha_limite = siguiente_fecha_cuota(datetime.utcnow(), concepto.recurrencia, cada_n)

    numero_cuota = 1
    fecha_cuota = fecha_inicio

    while fecha_cuota <= fecha_limite:
        # Calcular fecha de vencimiento
        if concepto.recurrencia == Recurrencia.MENSUAL:
            dia = concepto.dia_cobro or 1
            if dia == 0:
                fecha_vencimiento = fecha_cuota + relativedelta(months=1, day=1) - relativedelta(days=1)
            else:
                fecha_vencimiento = fecha_cuota.replace(day=min(dia, 28))
        else:
            fecha_vencimiento = siguiente_fecha_cuota(fecha_cuota, concepto.recurrencia, cada_n)

        # Verificar si la cuota ya existe
        cuota_existe = db.query(Cuota).filter(
            Cuota.usuario_id == usuario_id,
            Cuota.concepto_id == concepto_id,
            Cuota.numero_cuota == numero_cuota
        ).first()

        if not cuota_existe:
            cuota = Cuota(
                concepto_id=concepto_id,
                usuario_id=usuario_id,
                numero_cuota=numero_cuota,
                monto=concepto.monto,
                fecha_vencimiento=fecha_vencimiento,
                estado=EstadoCuota.PENDIENTE
            )
            db.add(cuota)

        fecha_cuota = siguiente_fecha_cuota(fecha_cuota, concepto.recurrencia, cada_n)
        numero_cuota += 1

    db.commit()


def generar_siguiente_cuota_si_todas_pagadas(db: Session, usuario_id: int, concepto_id: int):
    """
    Si todas las cuotas del usuario para este concepto están pagadas,
    genera automáticamente la siguiente cuota futura si no existe ya.
    """
    cuotas = db.query(Cuota).filter(
        Cuota.usuario_id == usuario_id,
        Cuota.concepto_id == concepto_id
    ).order_by(Cuota.numero_cuota).all()

    if not cuotas:
        return

    # Verificar si todas están pagadas
    todas_pagadas = all(c.estado == EstadoCuota.PAGADA for c in cuotas)
    if not todas_pagadas:
        return

    concepto = db.query(ConceptoPago).filter(ConceptoPago.id == concepto_id).first()
    if not concepto or concepto.tipo != TipoConcepto.CUOTA:
        return

    ultima_cuota = cuotas[-1]
    nuevo_numero = ultima_cuota.numero_cuota + 1
    cada_n = concepto.cada_n_periodos or 1
    nueva_fecha = siguiente_fecha_cuota(ultima_cuota.fecha_vencimiento, concepto.recurrencia, cada_n)

    # Verificar si ya existe una cuota con ese número o fecha para evitar duplicados
    existe = db.query(Cuota).filter(
        Cuota.usuario_id == usuario_id,
        Cuota.concepto_id == concepto_id,
        Cuota.numero_cuota == nuevo_numero
    ).first()

    if not existe:
        nueva_cuota = Cuota(
            concepto_id=concepto_id,
            usuario_id=usuario_id,
            numero_cuota=nuevo_numero,
            monto=concepto.monto,
            fecha_vencimiento=nueva_fecha,
            estado=EstadoCuota.PENDIENTE
        )
        db.add(nueva_cuota)
        db.commit()


@router.post("/asignar-conceptos/{usuario_id}")
async def asignar_conceptos_usuario(usuario_id: int, datos: AsignacionesRequest, db: Session = Depends(get_db)):
    """Asignar conceptos a un usuario con fecha retroactiva"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Asignar cuotas automáticamente (todas las activas)
    cuotas_conceptos = db.query(ConceptoPago).filter(
        ConceptoPago.tipo == TipoConcepto.CUOTA,
        ConceptoPago.activo == True,
        ConceptoPago.fecha_inicio <= datos.fecha_inicio_cobranza
    ).all()

    for concepto in cuotas_conceptos:
        # Crear asignación
        asignacion_existe = db.query(AsignacionConcepto).filter(
            AsignacionConcepto.usuario_id == usuario_id,
            AsignacionConcepto.concepto_id == concepto.id
        ).first()

        if not asignacion_existe:
            asignacion = AsignacionConcepto(
                concepto_id=concepto.id,
                usuario_id=usuario_id,
                fecha_inicio=datos.fecha_inicio_cobranza
            )
            db.add(asignacion)
            db.flush()

        # Generar cuotas desde fecha_inicio hasta hoy
        generar_cuotas_usuario(db, usuario_id, concepto.id, datos.fecha_inicio_cobranza)

    # Asignar multas y derechos manualmente seleccionados
    for concepto_id in datos.conceptos_multas_derechos:
        concepto = db.query(ConceptoPago).filter(ConceptoPago.id == concepto_id).first()
        if not concepto:
            continue

        asignacion_existe = db.query(AsignacionConcepto).filter(
            AsignacionConcepto.usuario_id == usuario_id,
            AsignacionConcepto.concepto_id == concepto_id
        ).first()

        if not asignacion_existe:
            asignacion = AsignacionConcepto(
                concepto_id=concepto_id,
                usuario_id=usuario_id,
                fecha_inicio=datetime.utcnow()
            )
            db.add(asignacion)
            db.flush()

        # Crear una cuota única para multa/derecho
        cuota_existe = db.query(Cuota).filter(
            Cuota.usuario_id == usuario_id,
            Cuota.concepto_id == concepto_id
        ).first()

        if not cuota_existe:
            cuota = Cuota(
                concepto_id=concepto_id,
                usuario_id=usuario_id,
                numero_cuota=1,
                monto=concepto.monto,
                fecha_vencimiento=datetime.utcnow() + relativedelta(days=15),
                estado=EstadoCuota.PENDIENTE
            )
            db.add(cuota)

    db.commit()
    return {
        "success": True,
        "message": "Conceptos asignados correctamente. Las cuotas se han generado automáticamente."
    }

class AsignacionMasivaRequest(BaseModel):
    fecha_inicio_cobranza: datetime

@router.post("/asignar-masivo")
async def asignar_masivo(datos: AsignacionMasivaRequest, db: Session = Depends(get_db)):
    """
    Asigna cuotas activas a TODOS los usuarios activos desde una fecha de inicio específica.
    """
    usuarios = db.query(Usuario).filter(Usuario.estado == "activo").all()
    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios activos")

    cuotas_conceptos = db.query(ConceptoPago).filter(
        ConceptoPago.tipo == TipoConcepto.CUOTA,
        ConceptoPago.activo == True
    ).all()

    if not cuotas_conceptos:
        raise HTTPException(status_code=400, detail="No hay conceptos de tipo CUOTA activos")

    usuarios_actualizados = 0

    for usuario in usuarios:
        usuario.fecha_inicio_cobranza = datos.fecha_inicio_cobranza
        
        for concepto in cuotas_conceptos:
            # Crear asignación
            asignacion_existe = db.query(AsignacionConcepto).filter(
                AsignacionConcepto.usuario_id == usuario.id,
                AsignacionConcepto.concepto_id == concepto.id
            ).first()

            if not asignacion_existe:
                asignacion = AsignacionConcepto(
                    concepto_id=concepto.id,
                    usuario_id=usuario.id,
                    fecha_inicio=datos.fecha_inicio_cobranza
                )
                db.add(asignacion)
                db.flush()
            else:
                # Si ya existe, actualizamos su fecha de inicio para que sincronice
                asignacion.fecha_inicio = datos.fecha_inicio_cobranza
                db.flush()

            # Generar cuotas desde fecha_inicio hasta hoy
            generar_cuotas_usuario(db, usuario.id, concepto.id, datos.fecha_inicio_cobranza)
        
        usuarios_actualizados += 1

    db.commit()
    
    return {
        "success": True,
        "message": f"Se han asignado las cuotas a {usuarios_actualizados} usuarios desde {datos.fecha_inicio_cobranza.strftime('%Y-%m-%d')}."
    }

# Endpoints Cuotas
@router.get("/cuotas")
async def listar_todas_cuotas(db: Session = Depends(get_db)):
    """Listar todas las cuotas del sistema (con sincronización automática)"""
    # 1. Sincronizar cuotas para usuarios con asignaciones activas
    # Esto asegura que aparezcan automáticamente si la fecha actual lo necesita
    asignaciones = db.query(AsignacionConcepto).filter(
        AsignacionConcepto.activa == True
    ).all()
    
    for asig in asignaciones:
        concepto = asig.concepto
        if concepto and concepto.tipo == TipoConcepto.CUOTA:
            # generar_cuotas_usuario genera hasta hoy + 1 periodo
            generar_cuotas_usuario(db, asig.usuario_id, concepto.id, asig.fecha_inicio)

    # 2. Retornar todas las cuotas
    cuotas = db.query(Cuota).order_by(Cuota.fecha_vencimiento).all()
    return {
        "success": True,
        "count": len(cuotas),
        "data": [
            {
                "id": c.id,
                "usuario_id": c.usuario_id,
                "numero_cuota": c.numero_cuota,
                "monto": c.monto,
                "fecha_vencimiento": c.fecha_vencimiento.isoformat(),
                "fecha_pagada": c.fecha_pagada.isoformat() if c.fecha_pagada else None,
                "estado": c.estado.value,
                "concepto": c.concepto.nombre
            }
            for c in cuotas
        ]
    }


@router.get("/cuotas/{usuario_id}")
async def listar_cuotas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Listar todas las cuotas de un usuario (y generar las que falten)"""
    # 1. Asegurarse de que el usuario tiene sus cuotas al día según la fecha actual
    asignaciones = db.query(AsignacionConcepto).filter(
        AsignacionConcepto.usuario_id == usuario_id,
        AsignacionConcepto.activa == True
    ).all()

    for asig in asignaciones:
        concepto = asig.concepto
        if concepto and concepto.tipo == TipoConcepto.CUOTA:
            generar_cuotas_usuario(db, usuario_id, concepto.id, asig.fecha_inicio)

    # 2. Retornar las cuotas (incluyendo las recién generadas si las hubiera)
    cuotas = db.query(Cuota).filter(Cuota.usuario_id == usuario_id).order_by(Cuota.fecha_vencimiento).all()
    return {
        "success": True,
        "count": len(cuotas),
        "data": [
            {
                "id": c.id,
                "usuario_id": c.usuario_id,
                "numero_cuota": c.numero_cuota,
                "monto": c.monto,
                "fecha_vencimiento": c.fecha_vencimiento.isoformat(),
                "fecha_pagada": c.fecha_pagada.isoformat() if c.fecha_pagada else None,
                "estado": c.estado.value,
                "concepto": c.concepto.nombre
            }
            for c in cuotas
        ]
    }


# Endpoint Generar próxima cuota recurrente
@router.post("/cuotas/{usuario_id}/generar-siguiente")
async def generar_siguiente_cuota(usuario_id: int, db: Session = Depends(get_db)):
    """Genera la siguiente cuota recurrente para un usuario"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener todas las cuotas del usuario, ordenadas por fecha
    cuotas = db.query(Cuota).filter(Cuota.usuario_id == usuario_id).order_by(Cuota.numero_cuota.desc()).all()
    if not cuotas:
        raise HTTPException(status_code=400, detail="El usuario no tiene cuotas para generar recurrencia")

    ultima_cuota = cuotas[0]
    concepto = ultima_cuota.concepto

    if not concepto or concepto.tipo != TipoConcepto.CUOTA:
        raise HTTPException(status_code=400, detail="El concepto no es válido para generar recurrencia")

    cada_n = concepto.cada_n_periodos or 1
    nueva_fecha_vencimiento = siguiente_fecha_cuota(ultima_cuota.fecha_vencimiento, concepto.recurrencia, cada_n)

    # Verificar si la cuota ya existe
    cuota_existe = db.query(Cuota).filter(
        Cuota.usuario_id == usuario_id,
        Cuota.concepto_id == concepto.id,
        Cuota.numero_cuota == ultima_cuota.numero_cuota + 1
    ).first()

    if cuota_existe:
        raise HTTPException(status_code=400, detail="La próxima cuota ya existe")

    # Crear la nueva cuota
    nueva_cuota = Cuota(
        concepto_id=concepto.id,
        usuario_id = usuario_id,
        numero_cuota=ultima_cuota.numero_cuota + 1,
        monto=concepto.monto,
        fecha_vencimiento=nueva_fecha_vencimiento,
        estado=EstadoCuota.PENDIENTE
    )
    db.add(nueva_cuota)
    db.commit()
    db.refresh(nueva_cuota)

    return {
        "success": True,
        "message": f"Cuota de {concepto.nombre} generada para {nueva_fecha_vencimiento.strftime('%Y-%m-%d')}",
        "data": {
            "id": nueva_cuota.id,
            "numero_cuota": nueva_cuota.numero_cuota,
            "monto": nueva_cuota.monto,
            "fecha_vencimiento": nueva_cuota.fecha_vencimiento.isoformat(),
            "concepto": concepto.nombre
        }
    }


# Endpoints Pagos
@router.post("/pagos")
async def registrar_pago(datos: PagoCreate, db: Session = Depends(get_db)):
    """Registrar un pago. Cash payments auto-approve, others need manual approval"""
    cuota = db.query(Cuota).filter(Cuota.id == datos.cuota_id).first()
    if not cuota:
        raise HTTPException(status_code=404, detail="Cuota no encontrada")

    # Auto-approve if cash payment
    if datos.metodo_pago == MetodoPago.EFECTIVO:
        estado = EstadoPago.APROBADO
        fecha_aprobacion = datetime.utcnow()
        cuota.estado = EstadoCuota.PAGADA
        cuota.fecha_pagada = datetime.utcnow()
    else:
        estado = EstadoPago.PENDIENTE_APROBACION
        fecha_aprobacion = None

    pago = Pago(
        cuota_id=datos.cuota_id,
        usuario_id=cuota.usuario_id,
        monto=datos.monto,
        metodo_pago=datos.metodo_pago,
        referencia=datos.referencia,
        observaciones=datos.observaciones,
        estado=estado,
        fecha_aprobacion=fecha_aprobacion
    )
    db.add(pago)
    db.commit()
    db.refresh(pago)

    # Si pago aprobado inmediatamente (efectivo), verificar si generar siguiente cuota
    if estado == EstadoPago.APROBADO:
        generar_siguiente_cuota_si_todas_pagadas(db, cuota.usuario_id, cuota.concepto_id)

    return {
        "success": True,
        "message": "Pago registrado" + (" y aprobado automáticamente" if estado == EstadoPago.APROBADO else ", pendiente de aprobación"),
        "data": {"id": pago.id, "estado": estado.value}
    }


@router.get("/pagos/pendientes/aprobacion")
async def listar_pagos_pendientes(db: Session = Depends(get_db)):
    """Listar pagos pendientes de aprobación"""
    pagos = db.query(Pago).filter(
        Pago.estado == EstadoPago.PENDIENTE_APROBACION
    ).order_by(Pago.created_at.desc()).all()

    data = []
    for p in pagos:
        usuario = db.query(Usuario).filter(Usuario.id == p.usuario_id).first()
        data.append({
            "id": p.id,
            "cuota_id": p.cuota_id,
            "usuario_id": p.usuario_id,
            "usuario_nombre": usuario.nombre_completo if usuario else "Desconocido",
            "monto": p.monto,
            "metodo_pago": p.metodo_pago.value,
            "referencia": p.referencia,
            "observaciones": p.observaciones,
            "estado": p.estado.value,
            "created_at": p.created_at.isoformat(),
            "concepto": p.cuota.concepto.nombre if p.cuota else None
        })

    return {
        "success": True,
        "count": len(data),
        "data": data
    }


@router.get("/pagos")
async def listar_todos_pagos(db: Session = Depends(get_db)):
    """Listar todos los pagos del sistema"""
    pagos = db.query(Pago).order_by(Pago.created_at.desc()).all()

    data = []
    for p in pagos:
        usuario = db.query(Usuario).filter(Usuario.id == p.usuario_id).first()
        data.append({
            "id": p.id,
            "cuota_id": p.cuota_id,
            "usuario_id": p.usuario_id,
            "usuario_nombre": usuario.nombre_completo if usuario else "Desconocido",
            "monto": p.monto,
            "metodo_pago": p.metodo_pago.value,
            "referencia": p.referencia,
            "observaciones": p.observaciones,
            "estado": p.estado.value,
            "created_at": p.created_at.isoformat(),
            "concepto": p.cuota.concepto.nombre if p.cuota else None,
            "fecha_pagada": p.cuota.fecha_pagada.isoformat() if p.cuota and p.cuota.fecha_pagada else None
        })

    return {
        "success": True,
        "count": len(data),
        "data": data
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
                "referencia": p.referencia,
                "estado": p.estado.value,
                "created_at": p.created_at.isoformat(),
                "concepto": p.cuota.concepto.nombre if p.cuota else None,
                "fecha_pagada": p.cuota.fecha_pagada.isoformat() if p.cuota and p.cuota.fecha_pagada else None
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

    usuario_id = pago.cuota.usuario_id
    concepto_id = pago.cuota.concepto_id

    db.commit()

    # Verificar si generar la siguiente cuota automáticamente
    generar_siguiente_cuota_si_todas_pagadas(db, usuario_id, concepto_id)

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


# ── Cuotas manuales / futuras ──────────────────────────────────────────────

class CuotaManualCreate(BaseModel):
    usuario_id: int
    concepto_id: int
    monto: Optional[float] = None          # Si None usa el monto del concepto
    fecha_vencimiento: datetime
    descripcion: Optional[str] = None


@router.post("/cuotas")
async def crear_cuota_manual(datos: CuotaManualCreate, db: Session = Depends(get_db)):
    """
    Crear una cuota manual/futura para un usuario.
    Útil para agregar cuotas adelantadas o cuotas especiales.
    """
    usuario = db.query(Usuario).filter(Usuario.id == datos.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    concepto = db.query(ConceptoPago).filter(ConceptoPago.id == datos.concepto_id).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto no encontrado")

    # Calcular número de cuota (siguiente al máximo existente para este usuario/concepto)
    ultima = db.query(Cuota).filter(
        Cuota.usuario_id == datos.usuario_id,
        Cuota.concepto_id == datos.concepto_id
    ).order_by(Cuota.numero_cuota.desc()).first()

    numero_siguiente = (ultima.numero_cuota + 1) if ultima else 1

    cuota = Cuota(
        concepto_id=datos.concepto_id,
        usuario_id=datos.usuario_id,
        numero_cuota=numero_siguiente,
        monto=datos.monto if datos.monto is not None else concepto.monto,
        fecha_vencimiento=datos.fecha_vencimiento,
        descripcion=datos.descripcion,
        estado=EstadoCuota.PENDIENTE
    )
    db.add(cuota)
    db.commit()
    db.refresh(cuota)

    return {
        "success": True,
        "message": f"Cuota #{numero_siguiente} creada para {usuario.nombre_completo}",
        "data": {
            "id": cuota.id,
            "numero_cuota": cuota.numero_cuota,
            "monto": cuota.monto,
            "fecha_vencimiento": cuota.fecha_vencimiento.isoformat(),
            "concepto": concepto.nombre
        }
    }


@router.delete("/cuotas/{cuota_id}")
async def eliminar_cuota(cuota_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una cuota pendiente.
    Solo se pueden eliminar cuotas que no hayan sido pagadas.
    """
    cuota = db.query(Cuota).filter(Cuota.id == cuota_id).first()
    if not cuota:
        raise HTTPException(status_code=404, detail="Cuota no encontrada")

    if cuota.estado != EstadoCuota.PENDIENTE:
        raise HTTPException(status_code=400, detail="Solo se pueden eliminar cuotas pendientes")

    db.delete(cuota)
    db.commit()

    return {
        "success": True,
        "message": "Cuota eliminada correctamente"
    }


@router.get("/conceptos-usuario/{usuario_id}")
async def conceptos_de_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Retorna los conceptos de cuota asignados a un usuario
    (para el modal de nueva cuota futura).
    """
    asignaciones = db.query(AsignacionConcepto).filter(
        AsignacionConcepto.usuario_id == usuario_id,
        AsignacionConcepto.activa == True
    ).all()

    conceptos_ids = {a.concepto_id for a in asignaciones}

    # También incluir conceptos que tengan cuotas existentes para este usuario
    cuotas_conceptos = db.query(Cuota.concepto_id).filter(
        Cuota.usuario_id == usuario_id
    ).distinct().all()
    conceptos_ids.update(c[0] for c in cuotas_conceptos)

    conceptos = db.query(ConceptoPago).filter(
        ConceptoPago.id.in_(conceptos_ids),
        ConceptoPago.activo == True
    ).all()

    return {
        "success": True,
        "data": [
            {
                "id": c.id,
                "nombre": c.nombre,
                "monto": c.monto,
                "recurrencia": c.recurrencia.value
            }
            for c in conceptos
        ]
    }
