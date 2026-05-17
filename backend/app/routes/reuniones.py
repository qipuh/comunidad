"""
Rutas para el sistema de reuniones y asistencia.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.usuario import Usuario, EstadoEnum
from app.models.reunion import Reunion, AsistenciaReunion, TipoReunionEnum, EstadoReunionEnum
from app.utils.auth import get_current_user
from app.utils.reconocimiento_facial import validar_rostro_contra_usuario
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import base64

router = APIRouter(prefix="/api/reuniones", tags=["Reuniones"])

# ==================== Schemas ====================

class ReunionCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    lugar: Optional[str] = None
    tipo: str  # asamblea, reunion, ordinaria, extraordinaria, sesion
    fecha_inicio: datetime
    fecha_fin: datetime
    estados_usuario_permitidos: List[str] = ["activo"]  # estados permitidos


class ReunionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    lugar: Optional[str] = None
    tipo: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estados_usuario_permitidos: Optional[List[str]] = None


class EstadoUpdate(BaseModel):
    estado: str  # programada, en_curso, finalizada, cancelada


class RegistroAsistenciaQR(BaseModel):
    dni: str


class RegistroAsistenciaFacial(BaseModel):
    foto_base64: str


class RegistroAsistenciaManual(BaseModel):
    usuario_id: int


class AsistenciaResponse(BaseModel):
    id: int
    usuario_id: int
    nombre_completo: str
    numero_dni: str
    estado: str
    fecha_hora_registro: datetime
    metodo_registro: str
    foto_url: Optional[str] = None

    class Config:
        from_attributes = True


class ReunionResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    lugar: Optional[str]
    tipo: str
    estado: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estados_usuario_permitidos: List[str]
    creado_por: int
    total_asistentes: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Endpoints ====================

@router.get("/")
async def listar_reuniones(
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista reuniones. Solo admin ve todas, usuarios solo ven las propias."""
    query = db.query(Reunion)

    # Filtro de rol
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede ver reuniones")

    # Filtros opcionales
    if estado:
        query = query.filter(Reunion.estado == estado)
    if tipo:
        query = query.filter(Reunion.tipo == tipo)

    reuniones = query.order_by(Reunion.created_at.desc()).all()

    return [
        ReunionResponse(
            id=r.id,
            nombre=r.nombre,
            descripcion=r.descripcion,
            lugar=r.lugar,
            tipo=r.tipo,
            estado=r.estado,
            fecha_inicio=r.fecha_inicio,
            fecha_fin=r.fecha_fin,
            estados_usuario_permitidos=r.estados_usuario_permitidos.split(","),
            creado_por=r.creado_por,
            total_asistentes=len(r.asistencias),
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in reuniones
    ]


@router.post("/")
async def crear_reunion(
    datos: ReunionCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin crea una nueva reunión (inicia en estado programada)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede crear reuniones")

    reunion = Reunion(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        lugar=datos.lugar,
        tipo=datos.tipo,
        estado="programada",
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        estados_usuario_permitidos=",".join(datos.estados_usuario_permitidos),
        creado_por=usuario.id,
    )
    db.add(reunion)
    db.commit()
    db.refresh(reunion)

    return ReunionResponse(
        id=reunion.id,
        nombre=reunion.nombre,
        descripcion=reunion.descripcion,
        lugar=reunion.lugar,
        tipo=reunion.tipo,
        estado=reunion.estado,
        fecha_inicio=reunion.fecha_inicio,
        fecha_fin=reunion.fecha_fin,
        estados_usuario_permitidos=reunion.estados_usuario_permitidos.split(","),
        creado_por=reunion.creado_por,
        total_asistentes=0,
        created_at=reunion.created_at,
        updated_at=reunion.updated_at,
    )


@router.get("/{reunion_id}")
async def obtener_reunion(
    reunion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene detalles de una reunión"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede ver reuniones")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    return ReunionResponse(
        id=reunion.id,
        nombre=reunion.nombre,
        descripcion=reunion.descripcion,
        lugar=reunion.lugar,
        tipo=reunion.tipo,
        estado=reunion.estado,
        fecha_inicio=reunion.fecha_inicio,
        fecha_fin=reunion.fecha_fin,
        estados_usuario_permitidos=reunion.estados_usuario_permitidos.split(","),
        creado_por=reunion.creado_por,
        total_asistentes=len(reunion.asistencias),
        created_at=reunion.created_at,
        updated_at=reunion.updated_at,
    )


@router.put("/{reunion_id}")
async def actualizar_reunion(
    reunion_id: int,
    datos: ReunionUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin actualiza una reunión"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede actualizar reuniones")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    if datos.nombre is not None:
        reunion.nombre = datos.nombre
    if datos.descripcion is not None:
        reunion.descripcion = datos.descripcion
    if datos.lugar is not None:
        reunion.lugar = datos.lugar
    if datos.tipo is not None:
        reunion.tipo = datos.tipo
    if datos.fecha_inicio is not None:
        reunion.fecha_inicio = datos.fecha_inicio
    if datos.fecha_fin is not None:
        reunion.fecha_fin = datos.fecha_fin
    if datos.estados_usuario_permitidos is not None:
        reunion.estados_usuario_permitidos = ",".join(datos.estados_usuario_permitidos)

    reunion.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(reunion)

    return ReunionResponse(
        id=reunion.id,
        nombre=reunion.nombre,
        descripcion=reunion.descripcion,
        lugar=reunion.lugar,
        tipo=reunion.tipo,
        estado=reunion.estado,
        fecha_inicio=reunion.fecha_inicio,
        fecha_fin=reunion.fecha_fin,
        estados_usuario_permitidos=reunion.estados_usuario_permitidos.split(","),
        creado_por=reunion.creado_por,
        total_asistentes=len(reunion.asistencias),
        created_at=reunion.created_at,
        updated_at=reunion.updated_at,
    )


@router.delete("/{reunion_id}")
async def eliminar_reunion(
    reunion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin elimina una reunión (solo si no hay asistentes)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede eliminar reuniones")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    if len(reunion.asistencias) > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar una reunión con asistentes")

    db.delete(reunion)
    db.commit()

    return {"message": "Reunión eliminada"}


@router.put("/{reunion_id}/estado")
async def cambiar_estado_reunion(
    reunion_id: int,
    datos: EstadoUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin cambia el estado de una reunión"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede cambiar estados")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    # Validar estado
    estados_validos = ["programada", "en_curso", "finalizada", "cancelada"]
    if datos.estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Debe ser uno de {estados_validos}")

    reunion.estado = datos.estado
    reunion.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(reunion)

    return ReunionResponse(
        id=reunion.id,
        nombre=reunion.nombre,
        descripcion=reunion.descripcion,
        lugar=reunion.lugar,
        tipo=reunion.tipo,
        estado=reunion.estado,
        fecha_inicio=reunion.fecha_inicio,
        fecha_fin=reunion.fecha_fin,
        estados_usuario_permitidos=reunion.estados_usuario_permitidos.split(","),
        creado_por=reunion.creado_por,
        total_asistentes=len(reunion.asistencias),
        created_at=reunion.created_at,
        updated_at=reunion.updated_at,
    )


@router.post("/{reunion_id}/asistencia/qr")
async def registrar_asistencia_qr(
    reunion_id: int,
    datos: RegistroAsistenciaQR,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Registra asistencia escaneando QR del carnet"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede registrar asistencia")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    # Verificar que la reunión esté en_curso
    if reunion.estado != "en_curso":
        raise HTTPException(status_code=400, detail="La reunión debe estar en estado 'en_curso'")

    # Buscar usuario por DNI
    usuario_registro = db.query(Usuario).filter_by(numero_dni=datos.dni).first()
    if not usuario_registro:
        raise HTTPException(status_code=404, detail="Usuario con ese DNI no encontrado")

    # Verificar que el estado del usuario está permitido
    estados_permitidos = reunion.estados_usuario_permitidos.split(",")
    if usuario_registro.estado not in estados_permitidos:
        raise HTTPException(
            status_code=400,
            detail=f"El estado del usuario '{usuario_registro.estado}' no está permitido en esta reunión"
        )

    # Verificar si ya está registrado (UniqueConstraint lo evita en DB, pero mejor validar)
    ya_asistio = db.query(AsistenciaReunion).filter(
        AsistenciaReunion.reunion_id == reunion_id,
        AsistenciaReunion.usuario_id == usuario_registro.id
    ).first()

    if ya_asistio:
        raise HTTPException(status_code=400, detail="Este usuario ya está registrado en esta reunión")

    # Registrar asistencia
    asistencia = AsistenciaReunion(
        reunion_id=reunion_id,
        usuario_id=usuario_registro.id,
        metodo_registro="qr",
    )
    db.add(asistencia)
    db.commit()
    db.refresh(asistencia)

    return {
        "success": True,
        "asistencia": {
            "id": asistencia.id,
            "usuario_id": usuario_registro.id,
            "nombre_completo": usuario_registro.nombre_completo,
            "numero_dni": usuario_registro.numero_dni,
            "fecha_hora_registro": asistencia.fecha_hora_registro.isoformat(),
            "metodo_registro": "qr",
        }
    }


@router.post("/{reunion_id}/asistencia/facial")
async def registrar_asistencia_facial(
    reunion_id: int,
    datos: RegistroAsistenciaFacial,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Registra asistencia mediante reconocimiento facial"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede registrar asistencia")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    # Verificar que la reunión esté en_curso
    if reunion.estado != "en_curso":
        raise HTTPException(status_code=400, detail="La reunión debe estar en estado 'en_curso'")

    # Decodificar foto
    try:
        foto_bytes = base64.b64decode(datos.foto_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Foto base64 inválida: {str(e)}")

    # Obtener usuarios con estado permitido y reconocimiento facial habilitado
    estados_permitidos = reunion.estados_usuario_permitidos.split(",")
    usuarios_validos = db.query(Usuario).filter(
        Usuario.estado.in_(estados_permitidos),
        Usuario.usar_reconocimiento_facial == True
    ).all()

    if not usuarios_validos:
        raise HTTPException(status_code=400, detail="No hay usuarios con reconocimiento facial habilitado")

    # Buscar match de rostro (1-a-N)
    usuario_match = None
    for u in usuarios_validos:
        try:
            if validar_rostro_contra_usuario(foto_bytes, u):
                usuario_match = u
                break
        except Exception:
            continue

    if not usuario_match:
        raise HTTPException(status_code=400, detail="Rostro no reconocido")

    # Verificar si ya está registrado
    ya_asistio = db.query(AsistenciaReunion).filter(
        AsistenciaReunion.reunion_id == reunion_id,
        AsistenciaReunion.usuario_id == usuario_match.id
    ).first()

    if ya_asistio:
        raise HTTPException(status_code=400, detail="Este usuario ya está registrado en esta reunión")

    # Registrar asistencia
    asistencia = AsistenciaReunion(
        reunion_id=reunion_id,
        usuario_id=usuario_match.id,
        metodo_registro="facial",
        foto_validacion=datos.foto_base64,  # guardar foto para auditoría
    )
    db.add(asistencia)
    db.commit()
    db.refresh(asistencia)

    return {
        "success": True,
        "asistencia": {
            "id": asistencia.id,
            "usuario_id": usuario_match.id,
            "nombre_completo": usuario_match.nombre_completo,
            "numero_dni": usuario_match.numero_dni,
            "fecha_hora_registro": asistencia.fecha_hora_registro.isoformat(),
            "metodo_registro": "facial",
        }
    }


@router.post("/{reunion_id}/asistencia/manual")
async def registrar_asistencia_manual(
    reunion_id: int,
    datos: RegistroAsistenciaManual,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Registra asistencia manualmente seleccionando un usuario"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede registrar asistencia")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    # Verificar que la reunión esté en_curso
    if reunion.estado != "en_curso":
        raise HTTPException(status_code=400, detail="La reunión debe estar en estado 'en_curso'")

    # Buscar usuario por ID
    usuario_registro = db.query(Usuario).filter_by(id=datos.usuario_id).first()
    if not usuario_registro:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar que el estado del usuario está permitido
    estados_permitidos = reunion.estados_usuario_permitidos.split(",")
    if usuario_registro.estado not in estados_permitidos:
        raise HTTPException(
            status_code=400,
            detail=f"El estado del usuario '{usuario_registro.estado}' no está permitido en esta reunión"
        )

    # Verificar si ya está registrado
    ya_asistio = db.query(AsistenciaReunion).filter(
        AsistenciaReunion.reunion_id == reunion_id,
        AsistenciaReunion.usuario_id == usuario_registro.id
    ).first()

    if ya_asistio:
        raise HTTPException(status_code=400, detail="Este usuario ya está registrado en esta reunión")

    # Registrar asistencia
    asistencia = AsistenciaReunion(
        reunion_id=reunion_id,
        usuario_id=usuario_registro.id,
        metodo_registro="manual",
    )
    db.add(asistencia)
    db.commit()
    db.refresh(asistencia)

    return {
        "success": True,
        "asistencia": {
            "id": asistencia.id,
            "usuario_id": usuario_registro.id,
            "nombre_completo": usuario_registro.nombre_completo,
            "numero_dni": usuario_registro.numero_dni,
            "fecha_hora_registro": asistencia.fecha_hora_registro.isoformat(),
            "metodo_registro": "manual",
        }
    }


@router.get("/{reunion_id}/asistentes")
async def listar_asistentes(
    reunion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista los asistentes registrados de una reunión"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede ver asistentes")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    asistencias = db.query(AsistenciaReunion).filter_by(reunion_id=reunion_id).order_by(
        AsistenciaReunion.fecha_hora_registro
    ).all()

    return [
        {
            "id": a.id,
            "usuario_id": a.usuario_id,
            "nombre_completo": a.usuario.nombre_completo,
            "numero_dni": a.usuario.numero_dni,
            "estado": a.usuario.estado,
            "email": a.usuario.email,
            "foto_url": a.usuario.foto_url,
            "fecha_hora_registro": a.fecha_hora_registro.isoformat(),
            "metodo_registro": a.metodo_registro,
        }
        for a in asistencias
    ]


@router.delete("/{reunion_id}/asistentes/{usuario_id}")
async def remover_asistente(
    reunion_id: int,
    usuario_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin remueve un asistente registrado"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede remover asistentes")

    asistencia = db.query(AsistenciaReunion).filter(
        AsistenciaReunion.reunion_id == reunion_id,
        AsistenciaReunion.usuario_id == usuario_id
    ).first()

    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")

    db.delete(asistencia)
    db.commit()

    return {"message": "Asistente removido"}


@router.get("/{reunion_id}/reporte")
async def obtener_reporte(
    reunion_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene reporte completo de asistencia (asistentes + inasistentes)"""
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede ver reportes")

    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")

    # Obtener usuarios con estado permitido
    estados_permitidos = reunion.estados_usuario_permitidos.split(",")
    usuarios_permitidos = db.query(Usuario).filter(
        Usuario.estado.in_(estados_permitidos)
    ).all()

    # Obtener asistentes registrados
    asistencias = db.query(AsistenciaReunion).filter_by(reunion_id=reunion_id).all()
    usuarios_asistieron_ids = {a.usuario_id for a in asistencias}

    # Preparar datos de asistentes
    asistentes = []
    for a in asistencias:
        asistentes.append({
            "nombre_completo": a.usuario.nombre_completo,
            "numero_dni": a.usuario.numero_dni,
            "email": a.usuario.email,
            "estado": a.usuario.estado,
            "fecha_hora_registro": a.fecha_hora_registro.isoformat(),
            "metodo_registro": a.metodo_registro,
        })

    # Preparar datos de inasistentes
    inasistentes = []
    for u in usuarios_permitidos:
        if u.id not in usuarios_asistieron_ids:
            inasistentes.append({
                "nombre_completo": u.nombre_completo,
                "numero_dni": u.numero_dni,
                "email": u.email,
                "estado": u.estado,
            })

    return {
        "reunion": {
            "id": reunion.id,
            "nombre": reunion.nombre,
            "tipo": reunion.tipo,
            "fecha": reunion.fecha_inicio.isoformat(),
            "lugar": reunion.lugar,
        },
        "asistentes": asistentes,
        "inasistentes": inasistentes,
        "estadisticas": {
            "total_permitidos": len(usuarios_permitidos),
            "total_asistentes": len(asistentes),
            "total_inasistentes": len(inasistentes),
            "porcentaje_asistencia": round(len(asistentes) / len(usuarios_permitidos) * 100, 2) if usuarios_permitidos else 0,
        }
    }
