from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
from pathlib import Path

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

UPLOAD_DIR = Path("uploads/usuarios")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Schemas
class UsuarioCreateSchema(BaseModel):
    email: str
    username: str
    password: str
    nombre_completo: str
    numero_dni: str
    telefono: str
    rol: str = "usuario"

    class Config:
        from_attributes = True


class UsuarioUpdateSchema(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    nombre_completo: Optional[str] = None
    numero_dni: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    direccion: Optional[str] = None
    departamento: Optional[str] = None
    provincia: Optional[str] = None
    distrito: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None
    usar_reconocimiento_facial: Optional[bool] = None

    class Config:
        from_attributes = True


class UsuarioResponseSchema(BaseModel):
    id: int
    email: str
    username: str
    nombre_completo: str
    numero_dni: Optional[str] = None
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    direccion: Optional[str] = None
    departamento: Optional[str] = None
    provincia: Optional[str] = None
    distrito: Optional[str] = None
    foto_url: Optional[str] = None
    foto_frontal: Optional[str] = None
    foto_lateral_izq: Optional[str] = None
    foto_lateral_der: Optional[str] = None
    usar_reconocimiento_facial: bool = False
    rol: str
    estado: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


def save_upload_file(file: UploadFile, filename_prefix: str, usuario_id: int) -> str:
    """Save uploaded file and return the path."""
    if not file or not file.filename:
        return None

    content = file.file.read()
    if not content:
        return None

    file_extension = Path(file.filename).suffix if file.filename else ".jpg"
    filename = f"{filename_prefix}_{usuario_id}_{int(datetime.now().timestamp())}{file_extension}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)


# Rutas CRUD
@router.get("/")
async def listar_usuarios(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Listar todos los usuarios"""
    usuarios = db.query(Usuario).order_by(Usuario.created_at.desc()).limit(limit).offset(offset).all()
    total = db.query(Usuario).count()

    return {
        "success": True,
        "count": len(usuarios),
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": [
            {
                "id": u.id,
                "email": u.email,
                "username": u.username,
                "nombre_completo": u.nombre_completo,
                "numero_dni": u.numero_dni,
                "telefono": u.telefono,
                "fecha_nacimiento": u.fecha_nacimiento,
                "sexo": u.sexo,
                "estado_civil": u.estado_civil,
                "direccion": u.direccion,
                "departamento": u.departamento,
                "provincia": u.provincia,
                "distrito": u.distrito,
                "foto_url": u.foto_url,
                "foto_frontal": u.foto_frontal,
                "foto_lateral_izq": u.foto_lateral_izq,
                "foto_lateral_der": u.foto_lateral_der,
                "usar_reconocimiento_facial": u.usar_reconocimiento_facial,
                "rol": u.rol,
                "estado": u.estado,
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "updated_at": u.updated_at.isoformat() if u.updated_at else None
            }
            for u in usuarios
        ]
    }


@router.post("/")
async def crear_usuario(
    numero_dni: str = Form(...),
    email: str = Form(None),
    username: str = Form(None),
    password: str = Form(None),
    nombre_completo: str = Form(...),
    telefono: str = Form(...),
    fecha_nacimiento: str = Form(None),
    sexo: str = Form(None),
    estado_civil: str = Form(None),
    direccion: str = Form(None),
    departamento: str = Form(None),
    provincia: str = Form(None),
    distrito: str = Form(None),
    usar_reconocimiento_facial: bool = Form(False),
    rol: str = Form("usuario"),
    foto_frontal: Optional[UploadFile] = File(None),
    foto_lateral_izq: Optional[UploadFile] = File(None),
    foto_lateral_der: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Crear un nuevo usuario con soporte para fotos y datos Factiliza"""
    # Usar DNI como email y username si no se proveen
    email_final = email or f"{numero_dni}@comunidad.local"
    username_final = username or numero_dni
    password_final = password or ""

    # Validar que no exista email duplicado
    usuario_existente = db.query(Usuario).filter(Usuario.email == email_final).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Validar que no exista username duplicado
    username_existente = db.query(Usuario).filter(Usuario.username == username_final).first()
    if username_existente:
        raise HTTPException(status_code=400, detail="El username ya está registrado")

    # Validar que no exista DNI duplicado
    dni_existente = db.query(Usuario).filter(Usuario.numero_dni == numero_dni).first()
    if dni_existente:
        raise HTTPException(status_code=400, detail="El DNI ya está registrado")

    nuevo_usuario = Usuario(
        email=email_final,
        username=username_final,
        password_hash=password_final,
        numero_dni=numero_dni,
        nombre_completo=nombre_completo,
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo,
        estado_civil=estado_civil,
        direccion=direccion,
        departamento=departamento,
        provincia=provincia,
        distrito=distrito,
        usar_reconocimiento_facial=usar_reconocimiento_facial,
        rol=rol,
        estado="activo"
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # Guardar fotos si se proporcionan
    if foto_frontal:
        nuevo_usuario.foto_frontal = save_upload_file(foto_frontal, "frontal", nuevo_usuario.id)
    if foto_lateral_izq:
        nuevo_usuario.foto_lateral_izq = save_upload_file(foto_lateral_izq, "lateral_izq", nuevo_usuario.id)
    if foto_lateral_der:
        nuevo_usuario.foto_lateral_der = save_upload_file(foto_lateral_der, "lateral_der", nuevo_usuario.id)

    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "success": True,
        "message": "Usuario creado exitosamente",
        "data": {
            "id": nuevo_usuario.id,
            "email": nuevo_usuario.email,
            "username": nuevo_usuario.username,
            "nombre_completo": nuevo_usuario.nombre_completo,
            "numero_dni": nuevo_usuario.numero_dni,
            "telefono": nuevo_usuario.telefono,
            "rol": nuevo_usuario.rol,
            "estado": nuevo_usuario.estado,
            "created_at": nuevo_usuario.created_at.isoformat() if nuevo_usuario.created_at else None
        }
    }


@router.get("/{usuario_id}")
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de un usuario específico"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "success": True,
        "data": {
            "id": usuario.id,
            "email": usuario.email,
            "username": usuario.username,
            "nombre_completo": usuario.nombre_completo,
            "foto_url": usuario.foto_url,
            "rol": usuario.rol,
            "estado": usuario.estado,
            "created_at": usuario.created_at.isoformat() if usuario.created_at else None,
            "updated_at": usuario.updated_at.isoformat() if usuario.updated_at else None
        }
    }


@router.put("/{usuario_id}")
async def actualizar_usuario(
    usuario_id: int,
    email: Optional[str] = Form(None),
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    nombre_completo: Optional[str] = Form(None),
    numero_dni: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    fecha_nacimiento: Optional[str] = Form(None),
    sexo: Optional[str] = Form(None),
    estado_civil: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None),
    departamento: Optional[str] = Form(None),
    provincia: Optional[str] = Form(None),
    distrito: Optional[str] = Form(None),
    rol: Optional[str] = Form(None),
    estado: Optional[str] = Form(None),
    usar_reconocimiento_facial: Optional[bool] = Form(None),
    foto_frontal: UploadFile = File(None),
    foto_lateral_izq: UploadFile = File(None),
    foto_lateral_der: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Actualizar datos de un usuario"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar email único si se está actualizando
    if email and email != usuario.email:
        email_existente = db.query(Usuario).filter(Usuario.email == email).first()
        if email_existente:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        usuario.email = email

    # Validar username único si se está actualizando
    if username and username != usuario.username:
        username_existente = db.query(Usuario).filter(Usuario.username == username).first()
        if username_existente:
            raise HTTPException(status_code=400, detail="El username ya está registrado")
        usuario.username = username

    # Validar DNI único si se está actualizando
    if numero_dni and numero_dni != usuario.numero_dni:
        dni_existente = db.query(Usuario).filter(Usuario.numero_dni == numero_dni).first()
        if dni_existente:
            raise HTTPException(status_code=400, detail="El DNI ya está registrado")
        usuario.numero_dni = numero_dni

    if nombre_completo:
        usuario.nombre_completo = nombre_completo
    if telefono:
        usuario.telefono = telefono
    if fecha_nacimiento:
        usuario.fecha_nacimiento = fecha_nacimiento
    if sexo:
        usuario.sexo = sexo
    if estado_civil:
        usuario.estado_civil = estado_civil
    if direccion:
        usuario.direccion = direccion
    if departamento:
        usuario.departamento = departamento
    if provincia:
        usuario.provincia = provincia
    if distrito:
        usuario.distrito = distrito
    if password:
        usuario.password_hash = password
    if rol:
        usuario.rol = rol
    if estado:
        usuario.estado = estado
    if usar_reconocimiento_facial is not None:
        usuario.usar_reconocimiento_facial = usar_reconocimiento_facial

    # Guardar fotos si se proporcionan
    if foto_frontal:
        usuario.foto_frontal = save_upload_file(foto_frontal, "frontal", usuario_id)
    if foto_lateral_izq:
        usuario.foto_lateral_izq = save_upload_file(foto_lateral_izq, "lateral_izq", usuario_id)
    if foto_lateral_der:
        usuario.foto_lateral_der = save_upload_file(foto_lateral_der, "lateral_der", usuario_id)

    usuario.updated_at = datetime.now()

    db.commit()
    db.refresh(usuario)

    return {
        "success": True,
        "message": "Usuario actualizado exitosamente",
        "data": {
            "id": usuario.id,
            "email": usuario.email,
            "username": usuario.username,
            "nombre_completo": usuario.nombre_completo,
            "numero_dni": usuario.numero_dni,
            "telefono": usuario.telefono,
            "rol": usuario.rol,
            "estado": usuario.estado,
            "updated_at": usuario.updated_at.isoformat() if usuario.updated_at else None
        }
    }


@router.delete("/{usuario_id}")
async def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un usuario"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {
        "success": True,
        "message": "Usuario eliminado exitosamente"
    }


@router.get("/buscar/por-email")
async def buscar_por_email(
    email: str,
    db: Session = Depends(get_db)
):
    """Buscar usuario por email"""
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "success": True,
        "data": {
            "id": usuario.id,
            "email": usuario.email,
            "username": usuario.username,
            "nombre_completo": usuario.nombre_completo,
            "rol": usuario.rol,
            "estado": usuario.estado
        }
    }


@router.get("/estadisticas/total")
async def obtener_estadisticas(db: Session = Depends(get_db)):
    """Obtener estadísticas de usuarios"""
    total_usuarios = db.query(Usuario).count()
    usuarios_activos = db.query(Usuario).filter(Usuario.estado == "activo").count()
    usuarios_inactivos = db.query(Usuario).filter(Usuario.estado == "inactivo").count()

    return {
        "success": True,
        "data": {
            "total_usuarios": total_usuarios,
            "usuarios_activos": usuarios_activos,
            "usuarios_inactivos": usuarios_inactivos,
            "porcentaje_activos": (usuarios_activos / total_usuarios * 100) if total_usuarios > 0 else 0
        }
    }
