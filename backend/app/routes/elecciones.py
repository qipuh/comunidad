"""
Rutas para el sistema de elecciones y votación.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.usuario import Usuario
from app.models.eleccion import Eleccion, OpcionEleccion, Voto, PadronEleccion, TipoEleccionEnum, EstadoEleccionEnum
from app.utils.auth import get_current_user
from app.utils.reconocimiento_facial import validar_rostro_contra_usuario
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import base64

router = APIRouter(prefix="/api/elecciones", tags=["Elecciones"])

# Evitar redirects de FastAPI por trailing slash
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# ==================== Schemas ====================

class EleccionCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    tipo: str  # "cargo" | "acuerdo"
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    resultados_publicos: bool = False


class OpcionCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    usuario_id: Optional[int] = None  # para cargo
    orden: int = 0


class EstadoUpdate(BaseModel):
    estado: str  # solo "borrador", "activo", "cerrado"


class VotoCreate(BaseModel):
    opcion_id: int
    metodo_validacion: str  # "facial" | "manual"
    foto_base64: Optional[str] = None  # ambos métodos
    latitud: Optional[float] = None  # manual only
    longitud: Optional[float] = None  # manual only


# Response schemas
class OpcionResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    usuario_id: Optional[int]
    orden: int
    foto_url: Optional[str]
    votos: int = 0

    class Config:
        from_attributes = True


class EleccionResponse(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    tipo: str
    estado: str
    fecha_inicio: Optional[datetime]
    fecha_fin: Optional[datetime]
    resultados_publicos: bool
    opciones: List[OpcionResponse] = []
    ya_vote: bool = False
    total_votos: int = 0

    class Config:
        from_attributes = True


# ==================== Endpoints ====================

@router.get("/")
async def listar_elecciones(
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista elecciones.
    - Admin: ve todas en cualquier estado
    - Usuario: ve solo elecciones activas
    """
    query = db.query(Eleccion)

    # Filtro de rol
    if usuario.rol != "admin":
        query = query.filter(Eleccion.estado == "activo")

    # Filtros opcionales
    if estado:
        query = query.filter(Eleccion.estado == estado)
    if tipo:
        query = query.filter(Eleccion.tipo == tipo)

    elecciones = query.order_by(Eleccion.created_at.desc()).all()

    resultado = []
    for eleccion in elecciones:
        opciones = [
            OpcionResponse(
                id=op.id,
                nombre=op.nombre,
                descripcion=op.descripcion,
                usuario_id=op.usuario_id,
                orden=op.orden,
                foto_url=op.foto_url,
                votos=0
            ) for op in eleccion.opciones
        ]

        # Verificar si usuario ya votó
        ya_vote = db.query(Voto).filter(
            Voto.usuario_id == usuario.id,
            Voto.eleccion_id == eleccion.id
        ).first() is not None

        resultado.append(EleccionResponse(
            id=eleccion.id,
            titulo=eleccion.titulo,
            descripcion=eleccion.descripcion,
            tipo=eleccion.tipo,
            estado=eleccion.estado,
            fecha_inicio=eleccion.fecha_inicio,
            fecha_fin=eleccion.fecha_fin,
            resultados_publicos=eleccion.resultados_publicos,
            opciones=opciones,
            ya_vote=ya_vote,
            total_votos=len(eleccion.votos)
        ))

    return resultado


@router.post("/")
async def crear_eleccion(
    datos: EleccionCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin crea una nueva elección (inicia en estado borrador)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede crear elecciones")

    eleccion = Eleccion(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        tipo=datos.tipo,
        estado="borrador",
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        resultados_publicos=datos.resultados_publicos,
        creado_por=usuario.id
    )
    db.add(eleccion)
    db.commit()
    db.refresh(eleccion)

    return EleccionResponse(
        id=eleccion.id,
        titulo=eleccion.titulo,
        descripcion=eleccion.descripcion,
        tipo=eleccion.tipo,
        estado=eleccion.estado,
        fecha_inicio=eleccion.fecha_inicio,
        fecha_fin=eleccion.fecha_fin,
        resultados_publicos=eleccion.resultados_publicos,
        opciones=[]
    )


@router.get("/{eleccion_id}")
async def obtener_eleccion(
    eleccion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene detalles de una elección"""
    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    # Control de acceso
    if usuario.rol != "admin" and eleccion.estado != "activo":
        raise HTTPException(status_code=403, detail="No puedes ver elecciones inactivas")

    # Calcular votos por opción
    votos_por_opcion = db.query(
        Voto.opcion_id,
        func.count(Voto.id).label("count")
    ).filter(Voto.eleccion_id == eleccion_id).group_by(Voto.opcion_id).all()

    votos_dict = {v[0]: v[1] for v in votos_por_opcion}

    # Determinar si mostrar votos
    muestra_votos = usuario.rol == "admin" or eleccion.estado == "cerrado" or eleccion.resultados_publicos

    opciones = []
    for op in eleccion.opciones:
        votos_opcion = votos_dict.get(op.id, 0) if muestra_votos else 0
        opciones.append(OpcionResponse(
            id=op.id,
            nombre=op.nombre,
            descripcion=op.descripcion,
            usuario_id=op.usuario_id,
            orden=op.orden,
            foto_url=op.foto_url,
            votos=votos_opcion
        ))

    # Ordenar por orden
    opciones.sort(key=lambda x: x.orden)

    # Verificar si usuario ya votó
    ya_vote = db.query(Voto).filter(
        Voto.usuario_id == usuario.id,
        Voto.eleccion_id == eleccion_id
    ).first() is not None

    total_votos = len(eleccion.votos)

    return EleccionResponse(
        id=eleccion.id,
        titulo=eleccion.titulo,
        descripcion=eleccion.descripcion,
        tipo=eleccion.tipo,
        estado=eleccion.estado,
        fecha_inicio=eleccion.fecha_inicio,
        fecha_fin=eleccion.fecha_fin,
        resultados_publicos=eleccion.resultados_publicos,
        opciones=opciones,
        ya_vote=ya_vote,
        total_votos=total_votos
    )


@router.put("/{eleccion_id}/estado")
async def cambiar_estado(
    eleccion_id: int,
    datos: EstadoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin cambia estado de elección (solo transiciones hacia adelante: borrador→activo→cerrado)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede cambiar estado")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    # Validar transición
    estados_validos = ["borrador", "activo", "cerrado"]
    if datos.estado not in estados_validos:
        raise HTTPException(status_code=400, detail="Estado inválido")

    orden_estados = {"borrador": 0, "activo": 1, "cerrado": 2}
    if orden_estados[datos.estado] <= orden_estados[eleccion.estado]:
        raise HTTPException(status_code=400, detail="Solo puedes avanzar el estado, no retroceder")

    # Si activando, verificar que hay opciones
    if datos.estado == "activo" and not eleccion.opciones:
        raise HTTPException(status_code=400, detail="Debe agregar opciones antes de activar")

    eleccion.estado = datos.estado

    # Si está activando, agregar "VOTO EN BLANCO" si no existe
    if datos.estado == "activo":
        voto_blanco_existe = db.query(OpcionEleccion).filter_by(
            eleccion_id=eleccion_id,
            nombre="VOTO EN BLANCO"
        ).first()
        if not voto_blanco_existe:
            max_orden = db.query(func.max(OpcionEleccion.orden)).filter_by(
                eleccion_id=eleccion_id
            ).scalar() or 0
            voto_blanco = OpcionEleccion(
                eleccion_id=eleccion_id,
                nombre="VOTO EN BLANCO",
                descripcion="Abstención de voto",
                orden=max_orden + 1
            )
            db.add(voto_blanco)

    db.commit()
    db.refresh(eleccion)

    opciones = [OpcionResponse(
        id=op.id,
        nombre=op.nombre,
        descripcion=op.descripcion,
        usuario_id=op.usuario_id,
        orden=op.orden,
        foto_url=op.foto_url,
        votos=0
    ) for op in eleccion.opciones]

    return EleccionResponse(
        id=eleccion.id,
        titulo=eleccion.titulo,
        descripcion=eleccion.descripcion,
        tipo=eleccion.tipo,
        estado=eleccion.estado,
        fecha_inicio=eleccion.fecha_inicio,
        fecha_fin=eleccion.fecha_fin,
        resultados_publicos=eleccion.resultados_publicos,
        opciones=opciones
    )


@router.post("/{eleccion_id}/opciones")
async def agregar_opcion(
    eleccion_id: int,
    datos: OpcionCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin agrega candidato u opción (solo en estado borrador)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede agregar opciones")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    if eleccion.estado != "borrador":
        raise HTTPException(status_code=400, detail="Solo puedes agregar opciones en estado borrador")

    opcion = OpcionEleccion(
        eleccion_id=eleccion_id,
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        usuario_id=datos.usuario_id,
        orden=datos.orden
    )
    db.add(opcion)
    db.commit()
    db.refresh(opcion)

    return OpcionResponse(
        id=opcion.id,
        nombre=opcion.nombre,
        descripcion=opcion.descripcion,
        usuario_id=opcion.usuario_id,
        orden=opcion.orden,
        foto_url=opcion.foto_url,
        votos=0
    )


@router.delete("/{eleccion_id}/opciones/{opcion_id}")
async def eliminar_opcion(
    eleccion_id: int,
    opcion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin elimina opción (solo en estado borrador)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede eliminar opciones")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    if eleccion.estado != "borrador":
        raise HTTPException(status_code=400, detail="Solo puedes eliminar opciones en estado borrador")

    opcion = db.query(OpcionEleccion).filter_by(id=opcion_id, eleccion_id=eleccion_id).first()
    if not opcion:
        raise HTTPException(status_code=404, detail="Opción no encontrada")

    db.delete(opcion)
    db.commit()

    return {"success": True, "message": "Opción eliminada"}


@router.post("/{eleccion_id}/votar")
async def votar(
    eleccion_id: int,
    datos: VotoCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Usuario vota en una elección activa.
    Valida identidad por facial o manual, registra voto (una sola vez por usuario).
    """
    # Cargar elección
    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    # Verificar estado
    if eleccion.estado != "activo":
        raise HTTPException(status_code=400, detail="Elección no está activa")

    # Verificar fechas
    ahora = datetime.utcnow()
    if eleccion.fecha_inicio and ahora < eleccion.fecha_inicio:
        raise HTTPException(status_code=400, detail="Elección aún no ha iniciado")
    if eleccion.fecha_fin and ahora > eleccion.fecha_fin:
        raise HTTPException(status_code=400, detail="Elección ha terminado")

    # Verificar usuario activo
    if usuario.estado != "activo":
        raise HTTPException(status_code=401, detail="Usuario inactivo")

    # Verificar doble voto
    voto_existente = db.query(Voto).filter(
        Voto.usuario_id == usuario.id,
        Voto.eleccion_id == eleccion_id
    ).first()
    if voto_existente:
        raise HTTPException(status_code=409, detail="Ya has votado en esta elección")

    # Verificar opción pertenece a esta elección
    opcion = db.query(OpcionEleccion).filter_by(id=datos.opcion_id, eleccion_id=eleccion_id).first()
    if not opcion:
        raise HTTPException(status_code=400, detail="Opción no válida para esta elección")

    # Validar identidad
    foto_validacion_path = None
    if datos.metodo_validacion == "facial":
        if not datos.foto_base64:
            raise HTTPException(status_code=400, detail="Foto requerida para validación facial")

        match, error_msg = validar_rostro_contra_usuario(datos.foto_base64, usuario)
        if not match:
            raise HTTPException(status_code=401, detail="Rostro no reconocido")

    elif datos.metodo_validacion == "manual":
        if not datos.foto_base64:
            raise HTTPException(status_code=400, detail="Foto requerida para validación manual")
        if datos.latitud is None or datos.longitud is None:
            raise HTTPException(status_code=400, detail="Ubicación requerida para validación manual")

        # Guardar foto
        try:
            os.makedirs("uploads/elecciones/votos", exist_ok=True)
            if "," in datos.foto_base64:
                foto_data = datos.foto_base64.split(",")[1]
            else:
                foto_data = datos.foto_base64
            foto_bytes = base64.b64decode(foto_data)
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"voto_{eleccion_id}_{usuario.id}_{timestamp}.jpg"
            filepath = os.path.join("uploads/elecciones/votos", filename)
            with open(filepath, "wb") as f:
                f.write(foto_bytes)
            foto_validacion_path = filepath
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error guardando foto: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Método de validación inválido")

    # Crear voto
    try:
        voto = Voto(
            eleccion_id=eleccion_id,
            usuario_id=usuario.id,
            opcion_id=datos.opcion_id,
            metodo_validacion=datos.metodo_validacion,
            foto_validacion=foto_validacion_path,
            latitud=datos.latitud if datos.metodo_validacion == "manual" else None,
            longitud=datos.longitud if datos.metodo_validacion == "manual" else None,
            ip_address=None  # en producción: request.client.host
        )
        db.add(voto)
        db.commit()
        db.refresh(voto)
    except Exception as e:
        # Atrapar UniqueConstraint error (doble voto simultáneo)
        db.rollback()
        if "uq_usuario_eleccion" in str(e):
            raise HTTPException(status_code=409, detail="Ya has votado en esta elección")
        raise HTTPException(status_code=500, detail=f"Error registrando voto: {str(e)}")

    return {
        "success": True,
        "message": "Voto registrado exitosamente",
        "voto_id": voto.id
    }


@router.get("/{eleccion_id}/resultados")
async def obtener_resultados(
    eleccion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene resultados agregados de una elección.
    Admin: siempre accesible
    Usuario: solo si resultados_publicos=True o estado=cerrado
    """
    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    # Control de acceso
    if usuario.rol != "admin":
        if not (eleccion.resultados_publicos or eleccion.estado == "cerrado"):
            raise HTTPException(status_code=403, detail="Resultados no disponibles aún")

    # Contar votos por opción
    votos_por_opcion = db.query(
        Voto.opcion_id,
        func.count(Voto.id).label("count")
    ).filter(Voto.eleccion_id == eleccion_id).group_by(Voto.opcion_id).all()

    votos_dict = {v[0]: v[1] for v in votos_por_opcion}
    total_votos = sum(votos_dict.values())

    opciones_resultado = []
    for opcion in eleccion.opciones:
        votos = votos_dict.get(opcion.id, 0)
        porcentaje = (votos / total_votos * 100) if total_votos > 0 else 0
        opciones_resultado.append({
            "id": opcion.id,
            "nombre": opcion.nombre,
            "votos": votos,
            "porcentaje": round(porcentaje, 2)
        })

    # Ordenar por votos descending
    opciones_resultado.sort(key=lambda x: x["votos"], reverse=True)

    # Calcular padron stats
    total_padron = db.query(func.count(PadronEleccion.id)).filter(
        PadronEleccion.eleccion_id == eleccion_id
    ).scalar() or 0

    total_no_votaron = total_padron - total_votos
    participacion_pct = (total_votos / total_padron * 100) if total_padron > 0 else 0

    total_impugnados = db.query(func.count(Voto.id)).filter(
        Voto.eleccion_id == eleccion_id,
        Voto.impugnado == True
    ).scalar() or 0

    return {
        "eleccion_id": eleccion.id,
        "titulo": eleccion.titulo,
        "estado": eleccion.estado,
        "tipo": eleccion.tipo,
        "total_padron": total_padron,
        "total_votaron": total_votos,
        "total_no_votaron": total_no_votaron,
        "total_impugnados": total_impugnados,
        "participacion_pct": round(participacion_pct, 2),
        "opciones": opciones_resultado
    }


# ==================== PADRÓN DE ELECTORES ====================

@router.get("/{eleccion_id}/padron")
async def obtener_padron(
    eleccion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin obtiene el padrón de electores con estado de voto"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    # Obtener padrón con info de voto
    padron = db.query(PadronEleccion).filter_by(eleccion_id=eleccion_id).all()
    usuarios_votaron = db.query(Voto.usuario_id).filter_by(eleccion_id=eleccion_id).all()
    votaron_ids = {v[0] for v in usuarios_votaron}

    resultado = []
    for p in padron:
        resultado.append({
            "id": p.id,
            "usuario_id": p.usuario_id,
            "nombres": p.usuario.nombres,
            "apellido_paterno": p.usuario.apellido_paterno,
            "apellido_materno": p.usuario.apellido_materno,
            "numero_dni": p.usuario.numero_dni,
            "votó": p.usuario_id in votaron_ids,
            "created_at": p.created_at.isoformat()
        })

    return {"success": True, "count": len(resultado), "data": resultado}


@router.post("/{eleccion_id}/padron")
async def agregar_al_padron(
    eleccion_id: int,
    usuarios_ids: List[int],
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin agrega uno o varios usuarios al padrón (solo en borrador)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    if eleccion.estado != "borrador":
        raise HTTPException(status_code=400, detail="Solo en estado borrador")

    agregados = 0
    duplicados = 0
    for uid in usuarios_ids:
        existe_usuario = db.query(Usuario).filter_by(id=uid).first()
        if not existe_usuario:
            continue

        existe_padron = db.query(PadronEleccion).filter_by(
            eleccion_id=eleccion_id, usuario_id=uid
        ).first()
        if existe_padron:
            duplicados += 1
            continue

        db.add(PadronEleccion(eleccion_id=eleccion_id, usuario_id=uid))
        agregados += 1

    db.commit()
    return {
        "success": True,
        "agregados": agregados,
        "duplicados": duplicados,
        "message": f"Agregados {agregados} usuarios, {duplicados} duplicados"
    }


@router.post("/{eleccion_id}/padron/importar-todos")
async def importar_todos_padron(
    eleccion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin importa todos los usuarios activos al padrón"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    usuarios_activos = db.query(Usuario).filter_by(estado="activo").all()

    agregados = 0
    for u in usuarios_activos:
        existe = db.query(PadronEleccion).filter_by(
            eleccion_id=eleccion_id, usuario_id=u.id
        ).first()
        if not existe:
            db.add(PadronEleccion(eleccion_id=eleccion_id, usuario_id=u.id))
            agregados += 1

    db.commit()
    return {
        "success": True,
        "importados": agregados,
        "message": f"Importados {agregados} usuarios activos"
    }


@router.delete("/{eleccion_id}/padron/{usuario_id}")
async def remover_del_padron(
    eleccion_id: int,
    usuario_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin remueve usuario del padrón (solo en borrador)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    if eleccion.estado != "borrador":
        raise HTTPException(status_code=400, detail="Solo en estado borrador")

    padron = db.query(PadronEleccion).filter_by(
        eleccion_id=eleccion_id, usuario_id=usuario_id
    ).first()
    if not padron:
        raise HTTPException(status_code=404, detail="Usuario no en padrón")

    db.delete(padron)
    db.commit()
    return {"success": True, "message": "Usuario removido del padrón"}


# ==================== VOTOS Y IMPUGNACIÓN ====================

@router.get("/{eleccion_id}/votos")
async def obtener_votos(
    eleccion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin obtiene listado detallado de votos individuales"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    votos = db.query(Voto).filter_by(eleccion_id=eleccion_id).all()

    resultado = []
    for v in votos:
        resultado.append({
            "id": v.id,
            "usuario_id": v.usuario_id,
            "nombres": v.usuario.nombres,
            "apellido_paterno": v.usuario.apellido_paterno,
            "apellido_materno": v.usuario.apellido_materno,
            "numero_dni": v.usuario.numero_dni,
            "opcion_nombre": v.opcion.nombre,
            "metodo_validacion": v.metodo_validacion,
            "impugnado": v.impugnado,
            "motivo_impugnacion": v.motivo_impugnacion,
            "created_at": v.created_at.isoformat()
        })

    return {"success": True, "count": len(resultado), "data": resultado}


class ImpugnarRequest(BaseModel):
    impugnado: bool
    motivo: Optional[str] = None


@router.post("/{eleccion_id}/votos/{voto_id}/impugnar")
async def impugnar_voto(
    eleccion_id: int,
    voto_id: int,
    request: ImpugnarRequest,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin marca/desmarcar voto como impugnado"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")

    voto = db.query(Voto).filter_by(id=voto_id, eleccion_id=eleccion_id).first()
    if not voto:
        raise HTTPException(status_code=404, detail="Voto no encontrado")

    voto.impugnado = request.impugnado
    voto.motivo_impugnacion = request.motivo if request.impugnado else None
    voto.impugnado_por = usuario.id if request.impugnado else None
    voto.impugnado_at = datetime.utcnow() if request.impugnado else None

    db.commit()
    return {
        "success": True,
        "message": f"Voto {'impugnado' if request.impugnado else 'desimpugnado'}"
    }
