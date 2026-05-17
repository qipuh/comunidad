from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from pydantic import BaseModel
from typing import Optional
from app.utils.auth import crear_access_token, get_current_user
from app.utils.reconocimiento_facial import validar_rostro_contra_usuario

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginSchema(BaseModel):
    username: str  # DNI o username
    password: str


class LoginFacialSchema(BaseModel):
    foto_base64: str  # foto capturada en base64


class TokenResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    usuario: Optional[dict] = None
    message: Optional[str] = None


@router.post("/login")
async def login(datos: LoginSchema, db: Session = Depends(get_db)):
    """Login por DNI/username + contraseña"""
    # Buscar por DNI o username
    usuario = db.query(Usuario).filter(
        (Usuario.numero_dni == datos.username) |
        (Usuario.username == datos.username) |
        (Usuario.email == datos.username)
    ).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if usuario.estado != "activo":
        raise HTTPException(status_code=401, detail="Usuario inactivo")

    # Verificar contraseña (en producción usar bcrypt)
    if usuario.password_hash != datos.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Generar token JWT
    token = crear_access_token(usuario.id, usuario.rol, usuario.username)

    return {
        "success": True,
        "token": token,
        "message": "Login exitoso",
        "usuario": {
            "id": usuario.id,
            "nombre_completo": usuario.nombre_completo,
            "username": usuario.username,
            "numero_dni": usuario.numero_dni,
            "email": usuario.email,
            "rol": usuario.rol,
            "foto_frontal": usuario.foto_frontal,
            "usar_reconocimiento_facial": usuario.usar_reconocimiento_facial
        }
    }


@router.post("/login-facial")
async def login_facial(datos: LoginFacialSchema, db: Session = Depends(get_db)):
    """Login por reconocimiento facial - compara foto capturada con fotos registradas"""
    # Obtener todos los usuarios con reconocimiento facial habilitado
    usuarios = db.query(Usuario).filter(
        Usuario.usar_reconocimiento_facial == True,
        Usuario.estado == "activo",
        Usuario.foto_frontal != None
    ).all()

    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios con reconocimiento facial registrado")

    # Buscar coincidencia entre todos los usuarios (login 1-a-N)
    # Para cada usuario, llamar a la utilidad con comparación 1-a-1
    for usuario in usuarios:
        match, error = validar_rostro_contra_usuario(datos.foto_base64, usuario)
        if match:
            token = crear_access_token(usuario.id, usuario.rol, usuario.username)
            return {
                "success": True,
                "token": token,
                "message": f"Bienvenido, {usuario.nombre_completo}",
                "usuario": {
                    "id": usuario.id,
                    "nombre_completo": usuario.nombre_completo,
                    "username": usuario.username,
                    "numero_dni": usuario.numero_dni,
                    "email": usuario.email,
                    "rol": usuario.rol,
                    "foto_frontal": usuario.foto_frontal,
                    "usar_reconocimiento_facial": usuario.usar_reconocimiento_facial
                }
            }

    raise HTTPException(status_code=401, detail="Rostro no reconocido")


@router.post("/logout")
async def logout():
    """Logout - el cliente elimina el token"""
    return {"success": True, "message": "Sesión cerrada"}


@router.get("/me")
async def get_me(usuario: Usuario = Depends(get_current_user)):
    """Obtener usuario actual con token JWT validado"""
    return {
        "success": True,
        "usuario": {
            "id": usuario.id,
            "nombre_completo": usuario.nombre_completo,
            "username": usuario.username,
            "numero_dni": usuario.numero_dni,
            "email": usuario.email,
            "rol": usuario.rol
        }
    }
