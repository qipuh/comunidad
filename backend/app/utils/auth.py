"""
Utilidades de autenticación: token store y dependencias FastAPI.
"""
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from typing import Optional

# Token store: {token -> usuario_id}
# En producción, usar Redis o una tabla de tokens en la DB
_token_store: dict[str, int] = {}


def registrar_token(token: str, usuario_id: int):
    """Registra un token de autenticación emitido."""
    _token_store[token] = usuario_id


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia FastAPI que valida el token y retorna el usuario actual.
    Uso: @router.get("/mi-ruta")
         async def mi_ruta(usuario: Usuario = Depends(get_current_user)):
    """
    # Extraer token del header "Authorization: Bearer <token>"
    try:
        token = authorization.replace("Bearer ", "").strip()
    except Exception:
        raise HTTPException(status_code=401, detail="Header Authorization inválido")

    # Buscar en el store
    usuario_id = _token_store.get(token)
    if not usuario_id:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # Cargar usuario de la DB
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
    except Exception:
        return None

    usuario_id = _token_store.get(token)
    if not usuario_id:
        return None

    usuario = db.query(Usuario).filter_by(id=usuario_id, estado="activo").first()
    return usuario
