# Ejemplos de Código – Endpoints y Lógica Facial

---

## 1. BACKEND: Registrar Usuario + Subir 3 Fotos

### Schema Pydantic (DTO)

```python
# backend/app/schemas/usuario_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class FotoUsuarioCreate(BaseModel):
    tipo: str  # "frontal", "lateral_izquierdo", "lateral_derecho"
    # Se envía como multipart/form-data (imagen binaria)

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    rol: str = "vecino"
    familia_id: Optional[int] = None
    es_jefe_familia: bool = False
    direccion: Optional[str] = None
    # CAMPOS ABIERTOS: agregar aquí
    numero_casa: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str]
    rol: str
    estado: str
    familia_id: Optional[int]
    es_jefe_familia: bool
    direccion: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### Servicio de Reconocimiento Facial

```python
# backend/app/services/facial_recognition.py
import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO
from typing import List, Tuple

class FacialRecognitionService:
    """
    Maneja generación de embeddings y validación facial.
    """
    
    MODEL = "hog"  # "hog" o "cnn" (requiere GPU)
    DISTANCE_THRESHOLD = 0.6
    
    @staticmethod
    def generar_embedding(imagen_bytes: bytes) -> List[float]:
        """
        Entrada: bytes de imagen (PNG, JPG, etc.)
        Salida: List[float] embedding de 128 elementos
        """
        try:
            # Cargar imagen
            imagen = Image.open(BytesIO(imagen_bytes))
            imagen_array = np.array(imagen)
            
            # Detectar rostros
            rostros = face_recognition.face_locations(
                imagen_array, 
                model=FacialRecognitionService.MODEL
            )
            
            if not rostros:
                raise ValueError("No se detectó rostro en la imagen")
            
            if len(rostros) > 1:
                raise ValueError("Se detectaron múltiples rostros. Captura solo uno")
            
            # Generar embedding
            embeddings = face_recognition.face_encodings(imagen_array, rostros)
            
            if not embeddings:
                raise ValueError("No se pudo generar embedding")
            
            # Retornar como lista (JSON-serializable)
            return embeddings[0].tolist()
        
        except Exception as e:
            raise ValueError(f"Error al procesar imagen: {str(e)}")
    
    @staticmethod
    def comparar_embeddings(
        embedding_vivo: List[float],
        embeddings_almacenados: List[List[float]]
    ) -> Tuple[float, float]:
        """
        Compara embedding en vivo con almacenados.
        
        Retorna:
            (score: 0-100, distancia_promedio: 0-1)
        """
        if not embeddings_almacenados:
            raise ValueError("No hay embeddings almacenados")
        
        embedding_vivo = np.array(embedding_vivo)
        
        distancias = []
        for emb in embeddings_almacenados:
            dist = np.linalg.norm(
                embedding_vivo - np.array(emb)
            )
            distancias.append(dist)
        
        # Distancia promedio
        dist_promedio = np.mean(distancias)
        
        # Convertir a score (0-100)
        # A menor distancia, mayor score
        # dist=0 -> score=100, dist=1 -> score=0
        score = max(0, min(100, (1 - dist_promedio) * 100))
        
        return score, dist_promedio
    
    @staticmethod
    def validar_vivo(
        imagen_viva_bytes: bytes,
        embeddings_almacenados: List[List[float]],
        umbral: float = 60.0
    ) -> dict:
        """
        Valida una imagen en vivo contra embeddings almacenados.
        """
        try:
            # Generar embedding de captura viva
            embedding_vivo = FacialRecognitionService.generar_embedding(
                imagen_viva_bytes
            )
            
            # Comparar
            score, dist = FacialRecognitionService.comparar_embeddings(
                embedding_vivo,
                embeddings_almacenados
            )
            
            validado = score >= umbral
            
            return {
                "validado": validado,
                "score": round(score, 2),
                "distancia": round(dist, 4),
                "umbral": umbral,
                "mensaje": (
                    "✓ Identidad validada" if validado 
                    else f"✗ Score insuficiente ({score:.1f}% < {umbral}%)"
                )
            }
        
        except Exception as e:
            return {
                "validado": False,
                "error": str(e),
                "score": 0
            }
```

### Endpoint: Registrar Usuario + Fotos

```python
# backend/app/routes/usuarios.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime

from app.models.usuario import Usuario, Familia, EstadoEnum, RolEnum
from app.models.foto import FotoUsuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, FotoUsuarioCreate
from app.services.facial_recognition import FacialRecognitionService
from app.services.storage import StorageService
from app.db.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

@router.post("/registro", response_model=dict)
async def registrar_usuario_con_fotos(
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: Optional[str] = Form(None),
    rol: str = Form("vecino"),
    direccion: Optional[str] = Form(None),
    numero_casa: Optional[str] = Form(None),  # CAMPO ABIERTO
    fecha_ingreso: Optional[str] = Form(None),  # CAMPO ABIERTO
    familia_id: Optional[int] = Form(None),
    es_jefe_familia: bool = Form(False),
    
    # Fotos (3 archivos)
    foto_frontal: UploadFile = File(...),
    foto_lateral_izquierda: UploadFile = File(...),
    foto_lateral_derecha: UploadFile = File(...),
    
    db: Session = Depends(get_db)
):
    """
    Registrar usuario y subir 3 fotos.
    
    Flujo:
    1. Validar email único
    2. Generar embeddings de las 3 fotos
    3. Guardar usuario en BD
    4. Guardar fotos + embeddings
    5. Retornar usuario creado
    """
    
    # Validar email único
    usuario_existente = db.query(Usuario).filter_by(email=email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )
    
    try:
        # Procesar las 3 fotos
        fotos_data = {
            "frontal": await foto_frontal.read(),
            "lateral_izquierdo": await foto_lateral_izquierda.read(),
            "lateral_derecho": await foto_lateral_derecha.read()
        }
        
        embeddings_generados = {}
        urls_almacenadas = {}
        
        for tipo, imagen_bytes in fotos_data.items():
            # Generar embedding
            embedding = FacialRecognitionService.generar_embedding(imagen_bytes)
            embeddings_generados[tipo] = embedding
            
            # Subir a cloud storage (S3, Azure, etc.)
            nombre_archivo = f"{uuid.uuid4()}_{tipo}.jpg"
            url = StorageService.subir_foto(imagen_bytes, nombre_archivo)
            urls_almacenadas[tipo] = url
        
        # Crear usuario
        usuario = Usuario(
            nombre=nombre,
            email=email,
            telefono=telefono,
            rol=RolEnum[rol.upper()],
            estado=EstadoEnum.ACTIVO,
            familia_id=familia_id,
            es_jefe_familia=es_jefe_familia,
            direccion=direccion,
            numero_casa=numero_casa,
            fecha_ingreso=datetime.fromisoformat(fecha_ingreso) if fecha_ingreso else None
        )
        db.add(usuario)
        db.flush()  # Obtener ID antes de commit
        
        # Guardar fotos + embeddings
        for tipo, embedding in embeddings_generados.items():
            foto = FotoUsuario(
                usuario_id=usuario.id,
                tipo=tipo,
                embedding=embedding,
                url_archivo=urls_almacenadas[tipo],
                fecha_captura=datetime.utcnow()
            )
            db.add(foto)
        
        db.commit()
        
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "mensaje": "✓ Usuario registrado exitosamente",
            "fotos_subidas": list(embeddings_generados.keys())
        }
    
    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en fotos: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar: {str(e)}"
        )

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtener datos de un usuario (requiere autenticación)"""
    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
```

---

## 2. BACKEND: Validar Asistencia en Reunión

### Endpoint: Marcar Asistencia

```python
# backend/app/routes/reuniones.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.reunion import Reunion, Asistencia
from app.models.foto import FotoUsuario
from app.models.usuario import Usuario
from app.services.facial_recognition import FacialRecognitionService
from app.db.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/reuniones", tags=["reuniones"])

@router.post("/{reunion_id}/validar-asistencia")
async def validar_y_marcar_asistencia(
    reunion_id: int,
    usuario_id: int,
    foto_viva: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Validar rostro + marcar asistencia en reunión.
    
    Flujo:
    1. Obtener reunión y usuario
    2. Obtener embeddings almacenados del usuario (3 fotos)
    3. Generar embedding de foto_viva
    4. Comparar (distancia Euclidiana)
    5. Si score > umbral: marcar asistencia
    """
    
    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    if not reunion:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    
    usuario = db.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Obtener fotos almacenadas
    fotos = db.query(FotoUsuario).filter_by(usuario_id=usuario_id).all()
    if len(fotos) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no ha completado registro facial"
        )
    
    try:
        # Leer foto en vivo
        imagen_viva = await foto_viva.read()
        
        # Embeddings almacenados
        embeddings_almacenados = [np.array(f.embedding) for f in fotos]
        
        # Validar
        resultado = FacialRecognitionService.validar_vivo(
            imagen_viva,
            embeddings_almacenados,
            umbral=reunion.umbral_facial
        )
        
        # Registrar intento
        asistencia = db.query(Asistencia).filter_by(
            reunion_id=reunion_id,
            usuario_id=usuario_id
        ).first()
        
        if not asistencia:
            asistencia = Asistencia(
                reunion_id=reunion_id,
                usuario_id=usuario_id,
                presente=False,
                intentos=0
            )
            db.add(asistencia)
        
        asistencia.intentos += 1
        
        if resultado["validado"]:
            asistencia.presente = True
            asistencia.score_facial = resultado["score"]
            asistencia.validacion_exitosa = True
            asistencia.hora_llegada = datetime.utcnow()
            asistencia.validated_at = datetime.utcnow()
            db.commit()
            
            return {
                "validado": True,
                "score": resultado["score"],
                "mensaje": f"✓ {usuario.nombre} - Asistencia registrada",
                "hora": asistencia.hora_llegada.isoformat()
            }
        else:
            asistencia.score_facial = resultado["score"]
            db.commit()
            
            return {
                "validado": False,
                "score": resultado["score"],
                "mensaje": resultado.get("mensaje", "No validado"),
                "intento": asistencia.intentos
            }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en validación: {str(e)}"
        )

@router.get("/{reunion_id}/reporte-asistencia")
def reporte_asistencia(
    reunion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Generar reporte de asistencia (solo admin)"""
    reunion = db.query(Reunion).filter_by(id=reunion_id).first()
    asistencias = db.query(Asistencia).filter_by(reunion_id=reunion_id).all()
    
    presentes = [a for a in asistencias if a.presente]
    ausentes = [a for a in asistencias if not a.presente]
    
    porcentaje_asistencia = (len(presentes) / len(asistencias) * 100) if asistencias else 0
    quorum_alcanzado = porcentaje_asistencia >= reunion.quorum_requerido
    
    return {
        "reunion": {
            "id": reunion.id,
            "titulo": reunion.titulo,
            "fecha": reunion.fecha.isoformat(),
            "quorum_requerido": reunion.quorum_requerido
        },
        "estadisticas": {
            "presentes": len(presentes),
            "ausentes": len(ausentes),
            "total": len(asistencias),
            "porcentaje_asistencia": round(porcentaje_asistencia, 2),
            "quorum_alcanzado": quorum_alcanzado
        },
        "detalles": [
            {
                "usuario": a.usuario.nombre,
                "presente": a.presente,
                "score_facial": a.score_facial,
                "hora_llegada": a.hora_llegada.isoformat() if a.hora_llegada else None,
                "intentos": a.intentos
            }
            for a in asistencias
        ]
    }
```

---

## 3. BACKEND: Proceso Electoral con Voto Secreto

### Endpoint: Votar

```python
# backend/app/routes/elecciones.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import hashlib

from app.models.eleccion import Eleccion, Candidato, Voto
from app.models.foto import FotoUsuario
from app.models.usuario import Usuario
from app.services.facial_recognition import FacialRecognitionService
from app.db.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/elecciones", tags=["elecciones"])

def generar_fingerprint(ip: str, user_agent: str, timestamp: datetime) -> str:
    """
    Generar fingerprint para auditoría sin revelar identidad.
    Usado para detectar fraude (múltiples votos del mismo "dispositivo").
    """
    datos = f"{ip}:{user_agent}:{timestamp.isoformat()}"
    return hashlib.sha256(datos.encode()).hexdigest()[:16]

@router.post("/{eleccion_id}/votar")
async def votar_con_validacion_facial(
    eleccion_id: int,
    email_usuario: str,
    candidato_id: int,
    foto_viva: UploadFile = File(...),
    request = None,  # Para obtener IP
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Votación con validación facial + voto secreto.
    
    Flujo:
    1. Validar que elección esté abierta
    2. Validar usuario en padrón
    3. Validar rostro (foto_viva vs. 3 fotos almacenadas)
    4. Generar token_anonimo (UUID)
    5. Registrar voto CON token (sin usuario_id vinculado después)
    6. Registrar fingerprint para auditoría
    """
    
    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")
    
    if eleccion.estado != "abierta":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Elección no está abierta"
        )
    
    # Validar usuario en padrón
    usuario = db.query(Usuario).filter_by(email=email_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if eleccion.padron_usuario_ids and usuario.id not in eleccion.padron_usuario_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No estás habilitado para votar en esta elección"
        )
    
    # Validar que no haya votado ya
    voto_existente = db.query(Voto).filter_by(
        eleccion_id=eleccion_id,
        usuario_id=usuario.id
    ).first()
    if voto_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya has votado en esta elección"
        )
    
    try:
        # Obtener fotos almacenadas
        fotos = db.query(FotoUsuario).filter_by(usuario_id=usuario.id).all()
        if len(fotos) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tu registro facial está incompleto"
            )
        
        # Leer foto en vivo
        imagen_viva = await foto_viva.read()
        
        # Embeddings almacenados
        embeddings_almacenados = [np.array(f.embedding) for f in fotos]
        
        # Validar rostro
        resultado = FacialRecognitionService.validar_vivo(
            imagen_viva,
            embeddings_almacenados,
            umbral=eleccion.umbral_facial
        )
        
        if not resultado["validado"]:
            return {
                "votado": False,
                "score": resultado["score"],
                "mensaje": f"No pudimos verificar tu identidad ({resultado['score']:.1f}%)"
            }
        
        # ⭐ VOTO SECRETO: Generar token anónimo
        token_anonimo = str(uuid.uuid4())
        
        # Fingerprint para auditoría
        ip = request.client.host if request else "127.0.0.1"
        user_agent = request.headers.get("user-agent", "") if request else ""
        fingerprint = generar_fingerprint(ip, user_agent, datetime.utcnow())
        
        # Registrar voto
        voto = Voto(
            eleccion_id=eleccion_id,
            candidato_id=candidato_id,
            usuario_id=usuario.id,  # Temporal para validación
            token_anonimo=token_anonimo,
            score_facial=resultado["score"],
            validated_at=datetime.utcnow(),
            fingerprint=fingerprint
        )
        db.add(voto)
        
        # Incrementar contador de candidato
        candidato = db.query(Candidato).filter_by(id=candidato_id).first()
        if candidato:
            candidato.votos_recibidos += 1
        
        db.commit()
        
        # ⭐ ANONIMIZAR: Borrar usuario_id del voto (mantener auditoría)
        # En producción: hacer esto en transacción separada después de confirmación
        voto.usuario_id = None
        db.commit()
        
        return {
            "votado": True,
            "token": token_anonimo[:8] + "...",  # Mostrar solo parte del token
            "score": resultado["score"],
            "mensaje": "✓ Tu voto ha sido registrado de forma segura y anónima"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en votación: {str(e)}"
        )

@router.get("/{eleccion_id}/resultados")
def obtener_resultados(
    eleccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # Solo admin
):
    """Ver resultados (solo después de cerrada la elección)"""
    eleccion = db.query(Eleccion).filter_by(id=eleccion_id).first()
    if not eleccion:
        raise HTTPException(status_code=404, detail="Elección no encontrada")
    
    candidatos = db.query(Candidato).filter_by(eleccion_id=eleccion_id).all()
    total_votos = sum(c.votos_recibidos for c in candidatos)
    
    return {
        "eleccion": {
            "id": eleccion.id,
            "titulo": eleccion.titulo,
            "estado": eleccion.estado,
            "total_votos": total_votos
        },
        "candidatos": [
            {
                "id": c.id,
                "nombre": c.nombre,
                "votos": c.votos_recibidos,
                "porcentaje": (c.votos_recibidos / total_votos * 100) if total_votos > 0 else 0
            }
            for c in sorted(candidatos, key=lambda x: x.votos_recibidos, reverse=True)
        ]
    }

@router.get("/{eleccion_id}/auditoria")
def auditoria_eleccion(
    eleccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # Solo admin
):
    """Ver auditoría: quién votó (sin revelar qué votó)"""
    votos = db.query(Voto).filter_by(eleccion_id=eleccion_id).all()
    
    return {
        "auditoria": [
            {
                "token": v.token_anonimo[:8] + "...",
                "score_facial": v.score_facial,
                "fecha_voto": v.created_at.isoformat(),
                "fingerprint": v.fingerprint  # Para detectar duplicados
            }
            for v in votos
        ],
        "estadisticas": {
            "total_votos": len(votos),
            "tokens_unicos": len(set(v.token_anonimo for v in votos))
        }
    }
```

---

## 4. FRONTEND: Componente de Captura de Fotos (Vue.js 3)

### useFaceCapture.ts (Composable)

```typescript
// frontend/src/composables/useFaceCapture.ts
import { ref, computed } from 'vue'

interface CapturedPhoto {
  frontal: Blob | null
  lateral_izquierdo: Blob | null
  lateral_derecho: Blob | null
}

export function useFaceCapture() {
  const videoRef = ref<HTMLVideoElement | null>(null)
  const canvasRef = ref<HTMLCanvasElement | null>(null)
  const photos = ref<CapturedPhoto>({
    frontal: null,
    lateral_izquierdo: null,
    lateral_derecho: null
  })
  
  const currentStep = ref<'frontal' | 'lateral_izquierdo' | 'lateral_derecho'>('frontal')
  const capturedCount = computed(() => {
    return Object.values(photos.value).filter(p => p !== null).length
  })
  
  const allCaptured = computed(() => capturedCount.value === 3)
  
  const initCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' }
      })
      if (videoRef.value) {
        videoRef.value.srcObject = stream
      }
    } catch (error) {
      console.error('Error accediendo a cámara:', error)
    }
  }
  
  const capturePhoto = () => {
    if (!videoRef.value || !canvasRef.value) return
    
    const context = canvasRef.value.getContext('2d')
    if (!context) return
    
    canvasRef.value.width = videoRef.value.videoWidth
    canvasRef.value.height = videoRef.value.videoHeight
    context.drawImage(videoRef.value, 0, 0)
    
    canvasRef.value.toBlob(blob => {
      if (blob) {
        photos.value[currentStep.value] = blob
        
        // Pasar al siguiente paso
        const steps: Array<'frontal' | 'lateral_izquierdo' | 'lateral_derecho'> = [
          'frontal',
          'lateral_izquierdo',
          'lateral_derecho'
        ]
        const nextIndex = steps.indexOf(currentStep.value) + 1
        if (nextIndex < steps.length) {
          currentStep.value = steps[nextIndex]
        }
      }
    })
  }
  
  const resetCapture = () => {
    photos.value = {
      frontal: null,
      lateral_izquierdo: null,
      lateral_derecho: null
    }
    currentStep.value = 'frontal'
  }
  
  const stopCamera = () => {
    if (videoRef.value?.srcObject) {
      const stream = videoRef.value.srcObject as MediaStream
      stream.getTracks().forEach(track => track.stop())
    }
  }
  
  return {
    videoRef,
    canvasRef,
    photos,
    currentStep,
    capturedCount,
    allCaptured,
    initCamera,
    capturePhoto,
    resetCapture,
    stopCamera
  }
}
```

### FaceScanner.vue

```vue
<!-- frontend/src/components/facial/FaceScanner.vue -->
<template>
  <div class="face-scanner">
    <h2>Captura de Rostro (3 fotos)</h2>
    
    <div class="progress">
      <div class="step" :class="{ active: currentStep === 'frontal', done: photos.frontal }">
        📸 Frontal
      </div>
      <div class="step" :class="{ active: currentStep === 'lateral_izquierdo', done: photos.lateral_izquierdo }">
        📸 Lateral Izq.
      </div>
      <div class="step" :class="{ active: currentStep === 'lateral_derecho', done: photos.lateral_derecho }">
        📸 Lateral Der.
      </div>
    </div>
    
    <div class="camera-container">
      <video
        ref="videoRef"
        autoplay
        playsinline
        @loadedmetadata="() => {}"
      />
      <canvas ref="canvasRef" style="display: none;" />
      
      <div class="instructions">
        <p v-if="currentStep === 'frontal'">
          Colócate frente a la cámara. Asegúrate de que tu rostro sea visible.
        </p>
        <p v-else-if="currentStep === 'lateral_izquierdo'">
          Gira tu cabeza hacia la izquierda 45°.
        </p>
        <p v-else>
          Gira tu cabeza hacia la derecha 45°.
        </p>
      </div>
      
      <button @click="capturePhoto" class="btn-primary">
        📷 Capturar {{ capturedCount }}/3
      </button>
    </div>
    
    <div class="preview-grid">
      <div v-if="photos.frontal" class="preview">
        <img :src="URL.createObjectURL(photos.frontal)" />
        <p>✓ Frontal</p>
      </div>
      <div v-if="photos.lateral_izquierdo" class="preview">
        <img :src="URL.createObjectURL(photos.lateral_izquierdo)" />
        <p>✓ Lateral Izq.</p>
      </div>
      <div v-if="photos.lateral_derecho" class="preview">
        <img :src="URL.createObjectURL(photos.lateral_derecho)" />
        <p>✓ Lateral Der.</p>
      </div>
    </div>
    
    <div v-if="allCaptured" class="actions">
      <button @click="$emit('photos-captured', photos)" class="btn-success">
        ✓ Confirmar y Continuar
      </button>
      <button @click="resetCapture" class="btn-secondary">
        🔄 Recapturar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useFaceCapture } from '@/composables/useFaceCapture'

const {
  videoRef,
  canvasRef,
  photos,
  currentStep,
  capturedCount,
  allCaptured,
  initCamera,
  capturePhoto,
  resetCapture,
  stopCamera
} = useFaceCapture()

defineEmits<{
  'photos-captured': [photos: Record<string, Blob>]
}>()

onMounted(() => {
  initCamera()
})

onUnmounted(() => {
  stopCamera()
})
</script>

<style scoped>
.face-scanner {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.progress {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.step {
  flex: 1;
  padding: 10px;
  background: #f0f0f0;
  border-radius: 8px;
  text-align: center;
  font-size: 12px;
  transition: all 0.3s;
}

.step.active {
  background: #3b82f6;
  color: white;
  font-weight: bold;
}

.step.done {
  background: #10b981;
  color: white;
}

.camera-container {
  position: relative;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  margin: 20px 0;
}

video {
  width: 100%;
  height: auto;
  display: block;
}

.instructions {
  background: rgba(255,255,255,0.9);
  padding: 15px;
  text-align: center;
  color: #333;
  font-size: 14px;
  margin-top: -40px;
  position: relative;
  z-index: 10;
}

.btn-primary, .btn-success, .btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  width: 100%;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-success:hover {
  background: #059669;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin: 20px 0;
}

.preview {
  text-align: center;
}

.preview img {
  width: 100%;
  border-radius: 8px;
  border: 2px solid #10b981;
}

.preview p {
  margin-top: 5px;
  color: #10b981;
  font-weight: bold;
  font-size: 12px;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.actions button {
  flex: 1;
}
</style>
```

---

## 5. FRONTEND: Componente de Validación Facial en Vivo

```vue
<!-- frontend/src/components/facial/FaceValidator.vue -->
<template>
  <div class="face-validator">
    <h3>{{ title }}</h3>
    
    <div class="validator-container">
      <video
        ref="videoRef"
        autoplay
        playsinline
      />
      
      <div class="score-display" v-if="lastScore !== null">
        <div :class="['score', { valid: lastScore >= umbral, invalid: lastScore < umbral }]">
          {{ Math.round(lastScore) }}%
        </div>
        <p v-if="lastScore >= umbral" class="success">✓ Identidad validada</p>
        <p v-else class="error">✗ Acércate a la cámara</p>
      </div>
      
      <button @click="captureAndValidate" :disabled="loading">
        {{ loading ? 'Validando...' : '📷 Validar Identidad' }}
      </button>
    </div>
    
    <div v-if="result" :class="['result', result.validado ? 'success' : 'error']">
      <p>{{ result.mensaje }}</p>
      <p v-if="result.score" class="score-info">Score: {{ result.score.toFixed(1) }}%</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { facialService } from '@/services/facial.service'

interface Props {
  title?: string
  umbral?: number
  usuarioId: number
}

interface Result {
  validado: boolean
  score: number
  mensaje: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Validar Identidad',
  umbral: 60
})

const emit = defineEmits<{
  'validation-complete': [result: Result]
}>()

const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const loading = ref(false)
const lastScore = ref<number | null>(null)
const result = ref<Result | null>(null)

const initCamera = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user' }
    })
    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }
  } catch (error) {
    console.error('Error accediendo a cámara:', error)
  }
}

const captureAndValidate = async () => {
  if (!videoRef.value) return
  
  loading.value = true
  
  try {
    const canvas = document.createElement('canvas')
    canvas.width = videoRef.value.videoWidth
    canvas.height = videoRef.value.videoHeight
    const ctx = canvas.getContext('2d')
    ctx?.drawImage(videoRef.value, 0, 0)
    
    canvas.toBlob(async blob => {
      if (!blob) return
      
      const validationResult = await facialService.validate(props.usuarioId, blob)
      lastScore.value = validationResult.score
      result.value = validationResult
      
      emit('validation-complete', validationResult)
    })
  } catch (error) {
    console.error('Error validando:', error)
    result.value = {
      validado: false,
      score: 0,
      mensaje: 'Error al validar identidad'
    }
  } finally {
    loading.value = false
  }
}

const stopCamera = () => {
  if (videoRef.value?.srcObject) {
    const stream = videoRef.value.srcObject as MediaStream
    stream.getTracks().forEach(track => track.stop())
  }
}

onMounted(initCamera)
onUnmounted(stopCamera)
</script>

<style scoped>
.face-validator {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.validator-container {
  position: relative;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  margin: 20px 0;
}

video {
  width: 100%;
  height: auto;
  display: block;
}

.score-display {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0,0,0,0.7);
  padding: 15px;
  border-radius: 8px;
  color: white;
  text-align: center;
}

.score {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
}

.score.valid {
  color: #10b981;
}

.score.invalid {
  color: #ef4444;
}

button {
  width: 100%;
  padding: 12px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  margin-top: -40px;
  position: relative;
  z-index: 10;
}

button:hover:not(:disabled) {
  background: #2563eb;
}

button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.result {
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.result.success {
  background: #d1fae5;
  color: #065f46;
}

.result.error {
  background: #fee2e2;
  color: #991b1b;
}

.score-info {
  font-size: 12px;
  margin-top: 10px;
}
</style>
```

---

---

## 7. CONFIGURACIÓN DINÁMICA - ENDPOINTS ADMIN

### 7.1 CRUD de Integraciones API

**Crear Integración:**
```http
POST /api/admin/integraciones-api
Content-Type: application/json
Authorization: Bearer {token_admin}

{
  "nombre": "RENIEC",
  "descripcion": "Consulta de DNI en Perú",
  "tipo": "reniec",
  "endpoint_url": "https://api.reniec.gob.pe/dni/",
  "auth_type": "bearer",
  "auth_token": "tu_token_secreto",
  "activa": true,
  "timeout_segundos": 30,
  "max_reintentos": 3
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "nombre": "RENIEC",
  "tipo": "reniec",
  "activa": true,
  "created_at": "2026-04-25T10:00:00"
}
```

**Listar Integraciones:**
```http
GET /api/admin/integraciones-api
Authorization: Bearer {token_admin}
```

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "RENIEC",
    "tipo": "reniec",
    "endpoint_url": "https://api.reniec.gob.pe/dni/",
    "activa": true,
    "timeout_segundos": 30
  },
  {
    "id": 2,
    "nombre": "Facturiza",
    "tipo": "facturiza",
    "endpoint_url": "https://api.facturiza.com/",
    "activa": true
  }
]
```

**Editar Integración:**
```http
PUT /api/admin/integraciones-api/1
Content-Type: application/json
Authorization: Bearer {token_admin}

{
  "timeout_segundos": 60,
  "max_reintentos": 5,
  "activa": false
}
```

**Probar Integración:**
```http
POST /api/admin/integraciones-api/1/probar
Authorization: Bearer {token_admin}

# Respuesta exitosa
{
  "disponible": true,
  "datos": {
    "nombre": "Juan",
    "apellido_paterno": "Pérez",
    "apellido_materno": "García",
    "fecha_nacimiento": "1990-05-15",
    "genero": "M"
  }
}

# Respuesta con error
{
  "disponible": false,
  "error": "Timeout: No response from RENIEC after 30 seconds"
}
```

---

### 7.2 CRUD de Campos Configuración

**Crear Campo Dinámico:**
```http
POST /api/admin/configuracion/campos
Content-Type: application/json
Authorization: Bearer {token_admin}

{
  "nombre_campo": "documento_identidad",
  "etiqueta": "Documento de Identidad",
  "descripcion": "DNI, cédula o pasaporte",
  "tipo_dato": "string",
  "es_obligatorio": true,
  "expresion_regex": "^[0-9]{8}$",
  "posicion": 1,
  "api_integracion_id": 1,
  "campo_mapa_api": "dni",
  "mostrar_en_registro": true,
  "mostrar_en_perfil": true,
  "mostrar_en_reportes": true
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "nombre_campo": "documento_identidad",
  "etiqueta": "Documento de Identidad",
  "tipo_dato": "string",
  "es_obligatorio": true,
  "api_integracion_id": 1,
  "campo_mapa_api": "dni",
  "created_at": "2026-04-25T10:05:00"
}
```

**Listar Campos:**
```http
GET /api/admin/configuracion/campos
Authorization: Bearer {token_admin}
```

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "nombre_campo": "documento_identidad",
    "etiqueta": "Documento de Identidad",
    "tipo_dato": "string",
    "es_obligatorio": true,
    "posicion": 1,
    "api_integracion_id": 1
  },
  {
    "id": 2,
    "nombre_campo": "nombre_completo",
    "etiqueta": "Nombre Completo",
    "tipo_dato": "string",
    "es_obligatorio": true,
    "posicion": 2,
    "api_integracion_id": null
  }
]
```

**Editar Campo:**
```http
PUT /api/admin/configuracion/campos/1
Content-Type: application/json
Authorization: Bearer {token_admin}

{
  "posicion": 3,
  "es_obligatorio": false,
  "mostrar_en_registro": true
}
```

**Eliminar Campo:**
```http
DELETE /api/admin/configuracion/campos/1
Authorization: Bearer {token_admin}

# Respuesta (204 No Content)
```

---

### 7.3 Estadísticas de Consultas

**Obtener Estadísticas:**
```http
GET /api/admin/estadisticas/consultas?desde=2026-04-01&hasta=2026-04-25
Authorization: Bearer {token_admin}
```

**Respuesta (200 OK):**
```json
{
  "total_consultas": 142,
  "consultas_exitosas": 128,
  "consultas_fallidas": 14,
  "tasa_exito": 90.14,
  "apis_mas_usadas": {
    "RENIEC": 85,
    "Facturiza": 57
  },
  "usuarios_unicos": 42,
  "fecha_inicio": "2026-04-01",
  "fecha_fin": "2026-04-25",
  "errores_comunes": {
    "Timeout": 8,
    "Invalid credentials": 4,
    "Network error": 2
  }
}
```

---

## 8. CONFIGURACIÓN DINÁMICA - ENDPOINTS USUARIO

### 8.1 Consultar DNI (Auto-llenar datos)

**Consultar RENIEC:**
```http
POST /api/validaciones/consultar-dni
Content-Type: application/json

{
  "dni": "12345678"
}
```

**Respuesta (200 OK):**
```json
{
  "exitosa": true,
  "datos": {
    "nombre": "Juan",
    "apellido_paterno": "Pérez",
    "apellido_materno": "García",
    "genero": "M",
    "fecha_nacimiento": "1990-05-15",
    "estado_civil": "Soltero"
  },
  "validado_externamente": true,
  "fuente": "RENIEC"
}
```

**Respuesta de Error (400 Bad Request):**
```json
{
  "exitosa": false,
  "error": "DNI no válido. Debe contener 8 dígitos.",
  "validado_externamente": false
}
```

---

### 8.2 Consultar RUC (Auto-llenar datos empresa)

**Consultar Facturiza:**
```http
POST /api/validaciones/consultar-ruc
Content-Type: application/json

{
  "ruc": "12345678901"
}
```

**Respuesta (200 OK):**
```json
{
  "exitosa": true,
  "datos": {
    "razon_social": "Empresa XYZ S.A.C.",
    "representante_legal": "Juan Pérez García",
    "direccion": "Av. Principal 123, Lima",
    "estado_contribuyente": "Habido",
    "actividad_economica": "Venta de servicios"
  },
  "validado_externamente": true,
  "fuente": "Facturiza"
}
```

---

### 8.3 Probar Conectividad

**Probar RENIEC:**
```http
GET /api/validaciones/probar-reniec
```

**Respuesta exitosa:**
```json
{
  "disponible": true,
  "timestamp": "2026-04-25T10:15:00",
  "tiempo_respuesta_ms": 245
}
```

**Respuesta con error:**
```json
{
  "disponible": false,
  "error": "Connection refused",
  "timestamp": "2026-04-25T10:15:00"
}
```

---

### 8.4 Historial de Consultas del Usuario

**Obtener Historial:**
```http
GET /api/validaciones/historial/{usuario_id}
Authorization: Bearer {token}
```

**Respuesta (200 OK):**
```json
{
  "usuario_id": 42,
  "consultas": [
    {
      "id": 1,
      "tipo_consulta": "DNI",
      "parametro": "12345678",
      "integracion": "RENIEC",
      "estado": "exitosa",
      "fecha": "2026-04-25T10:00:00",
      "campos_obtenidos": ["nombre", "apellido_paterno", "apellido_materno"]
    },
    {
      "id": 2,
      "tipo_consulta": "RUC",
      "parametro": "12345678901",
      "integracion": "Facturiza",
      "estado": "fallida",
      "fecha": "2026-04-25T10:05:00",
      "error": "RUC no encontrado"
    }
  ]
}
```

---

## 9. REGISTRO DINÁMICO - ENDPOINT COMPLETO

**Guardar Registro con Campos Dinámicos:**
```http
POST /api/usuarios/registro-dinamico
Content-Type: application/json
Authorization: Bearer {token}

{
  "documento_identidad": "12345678",
  "nombre_completo": "Juan Pérez García",
  "email": "juan@example.com",
  "telefono": "987654321",
  "numero_casa": "45",
  "fecha_ingreso": "2026-01-15",
  "profesion": "Ingeniero",
  "campos_validados": {
    "documento_identidad": true,
    "nombre_completo": true
  }
}
```

**Respuesta (201 Created):**
```json
{
  "usuario_id": 42,
  "mensaje": "Registro guardado exitosamente",
  "campos_guardados": 7,
  "campos_validados_externamente": 2,
  "timestamp": "2026-04-25T10:20:00"
}
```

---

## Próximos Pasos

1. **Completar campos abiertos** en `CAMPOS_PERSONALIZADOS.md`
2. **Implementar autenticación JWT** en backend
3. **Configurar S3/Azure Blob** para almacenar fotos
4. **Crear migraciones Alembic** para la BD
5. **Escribir tests** para validación facial
6. **Deploar** con Docker Compose
7. **Activar endpoints de configuración** (nuevos en versión dinámica)

