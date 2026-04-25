from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.usuario import Usuario
from pydantic import BaseModel
from typing import Optional
import base64
import os

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

    # Generar token simple (en producción usar JWT)
    import secrets
    token = secrets.token_hex(32)

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

    # Decodificar la foto capturada
    try:
        if "," in datos.foto_base64:
            foto_data = datos.foto_base64.split(",")[1]
        else:
            foto_data = datos.foto_base64
        foto_bytes = base64.b64decode(foto_data)
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de imagen inválido")

    # Intentar comparación con face_recognition si está disponible
    try:
        import face_recognition
        import numpy as np
        from PIL import Image
        import io

        # Cargar imagen capturada
        img_capturada = Image.open(io.BytesIO(foto_bytes)).convert("RGB")
        arr_capturada = np.array(img_capturada)
        encodings_capturados = face_recognition.face_encodings(arr_capturada)

        if not encodings_capturados:
            raise HTTPException(status_code=400, detail="No se detectó un rostro en la imagen")

        encoding_capturado = encodings_capturados[0]

        # Comparar con cada usuario
        for usuario in usuarios:
            for foto_path in [usuario.foto_frontal, usuario.foto_lateral_izq, usuario.foto_lateral_der]:
                if not foto_path or not os.path.exists(foto_path):
                    continue
                try:
                    img_registrada = face_recognition.load_image_file(foto_path)
                    encodings_registrados = face_recognition.face_encodings(img_registrada)
                    if not encodings_registrados:
                        continue
                    distancia = face_recognition.face_distance([encodings_registrados[0]], encoding_capturado)[0]
                    if distancia < 0.5:  # umbral de similitud
                        import secrets
                        token = secrets.token_hex(32)
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
                except Exception:
                    continue

        raise HTTPException(status_code=401, detail="Rostro no reconocido")

    except BaseException:
        # Comparación por características visuales sin dlib
        from PIL import Image, ImageFilter
        import io, math

        SIZE = 128

        def extraer_vector(img_bytes):
            img = Image.open(io.BytesIO(img_bytes)).convert("L")  # escala de grises
            # Recortar zona central (rostro suele estar centrado)
            w, h = img.size
            margen_x, margen_y = w // 6, h // 8
            img = img.crop((margen_x, margen_y, w - margen_x, h - margen_y))
            img = img.resize((SIZE, SIZE), Image.LANCZOS)
            img = img.filter(ImageFilter.SHARPEN)
            pixels = list(img.getdata())
            total = len(pixels)
            media = sum(pixels) / total
            std = math.sqrt(sum((p - media) ** 2 for p in pixels) / total) or 1
            # Normalizar
            return [(p - media) / std for p in pixels]

        def similitud_vectores(v1, v2):
            # Correlación de Pearson (1.0 = idéntico, 0.0 = sin relación)
            dot = sum(a * b for a, b in zip(v1, v2))
            n = len(v1)
            return dot / n  # ya normalizados, dot/n ≈ correlación

        try:
            vec_capturado = extraer_vector(foto_bytes)
        except Exception:
            raise HTTPException(status_code=400, detail="Imagen inválida")

        mejor_usuario = None
        mejor_score = -999.0
        scores_por_usuario = {}
        UMBRAL = 0.20  # correlación mínima

        for usuario in usuarios:
            scores_fotos = []
            for foto_path in [usuario.foto_frontal, usuario.foto_lateral_izq, usuario.foto_lateral_der]:
                if not foto_path or not os.path.exists(foto_path):
                    continue
                try:
                    with open(foto_path, "rb") as f:
                        vec_reg = extraer_vector(f.read())
                    score = similitud_vectores(vec_capturado, vec_reg)
                    scores_fotos.append(score)
                except Exception:
                    continue
            if scores_fotos:
                score_usuario = max(scores_fotos)
                scores_por_usuario[usuario.nombre_completo] = round(score_usuario, 4)
                if score_usuario > mejor_score:
                    mejor_score = score_usuario
                    mejor_usuario = usuario

        # Verificar que el ganador supere al segundo por margen suficiente
        todos_scores = sorted(scores_por_usuario.values(), reverse=True)
        segundo_score = todos_scores[1] if len(todos_scores) > 1 else 0
        margen = mejor_score - segundo_score
        print(f"[FACIAL] scores={scores_por_usuario} umbral={UMBRAL} ganador={mejor_usuario.nombre_completo if mejor_usuario else None} score={mejor_score:.4f} margen={margen:.4f}")
        if mejor_usuario and mejor_score >= UMBRAL and margen >= 0.05:
            import secrets
            token = secrets.token_hex(32)
            return {
                "success": True,
                "token": token,
                "message": f"Bienvenido, {mejor_usuario.nombre_completo}",
                "usuario": {
                    "id": mejor_usuario.id,
                    "nombre_completo": mejor_usuario.nombre_completo,
                    "username": mejor_usuario.username,
                    "numero_dni": mejor_usuario.numero_dni,
                    "email": mejor_usuario.email,
                    "rol": mejor_usuario.rol,
                    "foto_frontal": mejor_usuario.foto_frontal,
                    "usar_reconocimiento_facial": mejor_usuario.usar_reconocimiento_facial
                }
            }

        raise HTTPException(status_code=401, detail="Rostro no reconocido")


@router.post("/logout")
async def logout():
    """Logout - el cliente elimina el token"""
    return {"success": True, "message": "Sesión cerrada"}


@router.get("/me")
async def get_me(db: Session = Depends(get_db)):
    """Obtener usuario actual - en producción validar token JWT"""
    return {"success": True, "message": "Token válido"}
