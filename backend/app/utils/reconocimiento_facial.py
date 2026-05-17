"""
Utilidad compartida para validación de rostros.
Implementa dos métodos: dlib face_recognition y fallback PIL pixel correlation.
"""
import base64
import os
import io
from typing import Tuple
from PIL import Image, ImageFilter
import math
from app.models.usuario import Usuario


def validar_rostro_contra_usuario(foto_base64: str, usuario: Usuario) -> Tuple[bool, str]:
    """
    Valida si foto_base64 coincide con las fotos registradas del usuario.
    Para votación: comparación 1-a-1 contra un usuario específico (más seguro que login 1-a-N).

    Returns: (bool: match encontrado, str: mensaje de error si aplica)
    """
    # Decodificar
    try:
        if "," in foto_base64:
            foto_data = foto_base64.split(",")[1]
        else:
            foto_data = foto_base64
        foto_bytes = base64.b64decode(foto_data)
    except Exception:
        return False, "Formato de imagen inválido"

    # Tier 1: face_recognition con dlib
    try:
        import face_recognition
        import numpy as np

        img_capturada = Image.open(io.BytesIO(foto_bytes)).convert("RGB")
        arr_capturada = np.array(img_capturada)
        encodings_capturados = face_recognition.face_encodings(arr_capturada)

        if not encodings_capturados:
            raise Exception("No face detected")

        encoding_capturado = encodings_capturados[0]

        # Comparar solo contra las fotos de ESTE usuario
        for foto_path in [usuario.foto_frontal, usuario.foto_lateral_izq, usuario.foto_lateral_der]:
            if not foto_path or not os.path.exists(foto_path):
                continue
            try:
                img_registrada = face_recognition.load_image_file(foto_path)
                encodings_registrados = face_recognition.face_encodings(img_registrada)
                if not encodings_registrados:
                    continue
                distancia = face_recognition.face_distance([encodings_registrados[0]], encoding_capturado)[0]
                if distancia < 0.5:  # threshold
                    return True, ""
            except Exception:
                continue

        return False, "Rostro no reconocido"

    except BaseException:
        # Tier 2: PIL pixel correlation fallback
        return _validar_por_pixeles(foto_bytes, usuario)


def _validar_por_pixeles(foto_bytes: bytes, usuario: Usuario) -> Tuple[bool, str]:
    """
    Fallback: comparación por correlación de píxeles (Pearson).
    Sin detección facial real, solo coincidencia de patrones visuales.
    """
    SIZE = 128
    UMBRAL = 0.20
    MARGEN = 0.05

    def extraer_vector(img_bytes):
        img = Image.open(io.BytesIO(img_bytes)).convert("L")  # grayscale
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
        dot = sum(a * b for a, b in zip(v1, v2))
        n = len(v1)
        return dot / n

    try:
        vec_capturado = extraer_vector(foto_bytes)
    except Exception:
        return False, "Imagen inválida"

    mejor_score = -999.0
    scores_fotos = []

    # Comparar contra fotos del usuario específico
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

    if not scores_fotos:
        return False, "No se puede validar - usuario sin fotos registradas"

    mejor_score = max(scores_fotos)

    # Para votación 1-a-1: solo necesita superar el umbral (no hay segundo lugar)
    if mejor_score >= UMBRAL:
        return True, ""
    else:
        return False, "Rostro no reconocido"
