"""
Utilidades de autenticación con JWT.
"""
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def hash_password(password: str) -> str:
    """Hash password for storage. Currently uses plain text for compatibility."""
    return password


def crear_access_token(usuario_id: int, rol: str, username: str) -> str:
    """Crear un token JWT con expiración de 24 horas."""
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": str(usuario_id),
        "rol": rol,
        "username": username,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _decode_token(token: str) -> dict:
    """Decodificar y validar token JWT."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia FastAPI que valida el token JWT y retorna el usuario actual.
    Uso: @router.get("/mi-ruta")
         async def mi_ruta(usuario: Usuario = Depends(get_current_user)):
    """
    token = authorization.replace("Bearer ", "").strip()
    payload = _decode_token(token)
    usuario_id = int(payload.get("sub"))

    usuario = db.query(Usuario).filter_by(id=usuario_id, estado="activo").first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")

    return usuario


def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[Usuario]:
    """
    Versión opcional de get_current_user para endpoints que aceptan auth opcional.
    """
    if not authorization:
        return None

    try:
        token = authorization.replace("Bearer ", "").strip()
        payload = _decode_token(token)
        usuario_id = int(payload.get("sub"))
        return db.query(Usuario).filter_by(id=usuario_id, estado="activo").first()
    except HTTPException:
        return None
