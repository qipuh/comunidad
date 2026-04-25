# ⚡ Cheat Sheet – Sistema de Gestión Comunitaria

**Referencia rápida de comandos, configuración y código snippet.**

---

## 🚀 Setup Rápido (5 minutos)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate              # Windows
# source venv/bin/activate         # Linux/Mac

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Abre http://localhost:5173
```

### BD (Docker)
```bash
docker-compose up -d
# PostgreSQL en localhost:5432
```

---

## 📁 Estructura Base

```
backend/app/
├── models/
│   ├── usuario.py       # Usuario, Familia
│   ├── foto.py          # FotoUsuario (embeddings)
│   ├── aportacion.py    # Aportacion, PeriodoAporte
│   ├── reunion.py       # Reunion, Asistencia
│   └── eleccion.py      # Eleccion, Candidato, Voto
├── routes/
│   ├── usuarios.py      # POST /usuarios/registro
│   ├── reuniones.py     # POST /reuniones/{id}/validar-asistencia
│   ├── elecciones.py    # POST /elecciones/{id}/votar
│   └── ...
└── services/
    └── facial_recognition.py  # FacialRecognitionService
```

---

## 🧠 Facial Recognition – Resumen Técnico

### Generar Embedding (Registro)
```python
import face_recognition
import numpy as np

# 1. Cargar imagen
image = face_recognition.load_image_from_file("foto.jpg")

# 2. Detectar rostro
face_locations = face_recognition.face_locations(image)
if not face_locations:
    raise ValueError("No se detectó rostro")

# 3. Generar embedding (vector 128D)
embeddings = face_recognition.face_encodings(image, face_locations)
embedding = embeddings[0].tolist()  # JSON-serializable

# 4. Guardar en BD como JSON
db.add(FotoUsuario(usuario_id=id, embedding=embedding, tipo="frontal"))
```

### Validar Rostro (Reunión/Elección)
```python
# 1. Generar embedding de foto en vivo
embedding_vivo = face_recognition.face_encodings(imagen_viva)[0]

# 2. Obtener embeddings almacenados (3 fotos)
embeddings_almacenados = [np.array(f.embedding) for f in fotos]

# 3. Calcular distancias
distances = face_recognition.face_distance(embeddings_almacenados, embedding_vivo)
promedio = np.mean(distances)

# 4. Score (0-100)
score = (1 - promedio) * 100
validado = score >= 60  # Umbral
```

---

## 🗄️ Modelos Base (Copiar/Pegar)

### Usuario
```python
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), default=RolEnum.VECINO)
    estado = Column(Enum(EstadoEnum), default=EstadoEnum.ACTIVO)
    familia_id = Column(Integer, ForeignKey("familias.id"), nullable=True)
    # ⭐ AGREGA TUS CAMPOS AQUÍ
    created_at = Column(DateTime, default=datetime.utcnow)
```

### FotoUsuario
```python
class FotoUsuario(Base):
    __tablename__ = "fotos_usuario"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo = Column(String(50))  # "frontal", "lateral_izquierdo", "lateral_derecho"
    embedding = Column(JSON)   # List[float] 128 elementos
    url_archivo = Column(String(500))
```

### Voto (Voto Secreto)
```python
class Voto(Base):
    __tablename__ = "votos"
    id = Column(Integer, primary_key=True)
    eleccion_id = Column(Integer, ForeignKey("elecciones.id"))
    candidato_id = Column(Integer, ForeignKey("candidatos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    token_anonimo = Column(String(255), unique=True)  # UUID anónimo
    score_facial = Column(Float)
    fingerprint = Column(String(255))  # hash(ip + user_agent) para auditoría
```

---

## 🔌 Endpoints Principales

### Usuarios
```bash
# Registrar + fotos
POST /api/usuarios/registro
  Multipart form data:
    nombre, email, telefono, rol
    foto_frontal, foto_lateral_izquierda, foto_lateral_derecha
  Response: { id, nombre, email, fotos_subidas }

# Obtener usuario
GET /api/usuarios/{usuario_id}
  Headers: Authorization: Bearer <token>
```

### Reuniones
```bash
# Validar asistencia (facial)
POST /api/reuniones/{reunion_id}/validar-asistencia
  usuario_id, foto_viva (multipart)
  Response: { validado, score, mensaje, hora }

# Reporte asistencia
GET /api/reuniones/{reunion_id}/reporte-asistencia
  Response: { asistencias, estadisticas }
```

### Elecciones
```bash
# Votar (con validación facial)
POST /api/elecciones/{eleccion_id}/votar
  email, candidato_id, foto_viva (multipart)
  Response: { votado, token, score, mensaje }

# Ver resultados
GET /api/elecciones/{eleccion_id}/resultados
  Response: { candidatos[], total_votos }

# Auditoría (quién votó, sin revelar qué)
GET /api/elecciones/{eleccion_id}/auditoria
  Response: { votos[], tokens_unicos, estadisticas }
```

---

## 🎨 Componentes Vue.js

### FaceScanner (Captura 3 fotos)
```vue
<template>
  <div>
    <video ref="videoRef" autoplay></video>
    <button @click="capturePhoto">📷 Capturar {{ capturedCount }}/3</button>
    <button v-if="allCaptured" @click="$emit('photos-captured', photos)">
      ✓ Continuar
    </button>
  </div>
</template>

<script setup>
import { useFaceCapture } from '@/composables/useFaceCapture'
const { videoRef, photos, capturePhoto, capturedCount, allCaptured } = useFaceCapture()
</script>
```

### FaceValidator (Validación en vivo)
```vue
<template>
  <div>
    <video ref="videoRef" autoplay></video>
    <div class="score">{{ Math.round(lastScore) }}%</div>
    <button @click="captureAndValidate">📷 Validar</button>
  </div>
</template>

<script setup>
const { videoRef, lastScore, captureAndValidate } = useFaceValidator()
</script>
```

---

## 🔐 JWT – Autenticación

### Login (Backend)
```python
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "tu-secreto-super-seguro"
ALGORITHM = "HS256"

def login(email: str, password: str, db: Session):
    usuario = db.query(Usuario).filter_by(email=email).first()
    if not usuario or not verify_password(password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = jwt.encode(
        {"sub": usuario.email, "exp": datetime.utcnow() + timedelta(hours=24)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}
```

### Middleware (Backend)
```python
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(credentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=401)
    
    usuario = db.query(Usuario).filter_by(email=email).first()
    if not usuario:
        raise HTTPException(status_code=401)
    return usuario
```

### Usar en Endpoint
```python
@router.get("/perfil")
def obtener_perfil(current_user = Depends(get_current_user)):
    return current_user
```

### Header (Frontend)
```typescript
// axios.js
const api = axios.create({
  baseURL: 'http://localhost:8000/api'
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

---

## 🗺️ Migrations (Alembic)

```bash
# Ver estado actual
alembic current

# Crear migración automática
alembic revision --autogenerate -m "Add custom fields"

# Editar migración (si es necesario)
nano migrations/versions/xxx_add_custom_fields.py

# Aplicar migración
alembic upgrade head

# Ver historia de migraciones
alembic history

# Revertir última migración
alembic downgrade -1
```

---

## 📊 Tipos de Datos Frecuentes

| Caso | Tipo | Código |
|------|------|--------|
| Email único | String | `Column(String(255), unique=True)` |
| Enumeración | Enum | `Column(Enum(MiEnum))` |
| Fecha | DateTime | `Column(DateTime, default=datetime.utcnow)` |
| Decimal (dinero) | Float | `Column(Float)` |
| Booleano | Boolean | `Column(Boolean, default=True)` |
| Texto largo | Text | `Column(Text)` |
| JSON flexible | JSON | `Column(JSON)` ← Para embeddings, arrays |
| Clave foránea | ForeignKey | `Column(Integer, ForeignKey("tabla.id"))` |

---

## 🎯 Workflow Típico

### 1️⃣ Registrar Usuario + Fotos
```
Frontend → Captura 3 fotos con FaceScanner
         → Envía POST /usuarios/registro (multipart)
Backend  → Detecta rostros con face_recognition
         → Genera embeddings (vector 128D)
         → Almacena en BD
Frontend → ✓ "Usuario registrado"
```

### 2️⃣ Marcar Asistencia Reunión
```
Usuario llega a reunión
    ↓
Frontend → FaceValidator captura rostro
         → Envía POST /reuniones/{id}/validar-asistencia
Backend  → Genera embedding de captura viva
         → Compara con 3 embeddings almacenados
         → Si score > 60%: Asistencia registrada
Frontend → ✓ "Asistencia validada" o ✗ "Intente de nuevo"
```

### 3️⃣ Votación Secreta
```
Usuario accede a elección
    ↓
Frontend → Valida email/código
         → FaceValidator captura rostro
         → Envía foto + candidato elegido
Backend  → Valida rostro (score > umbral)
         → Genera token_anonimo (UUID)
         → Registra voto con token (sin usuario_id)
         → Registra fingerprint para auditoría
Frontend → ✓ "Tu voto fue registrado de forma anónima"

Después:
         → Usuario_id se anula del voto (total anonimato)
         → Solo fingerprint queda para auditoría
```

---

## 🐛 Debug Rápido

### Problema: "No se detecta rostro"
```python
# Verificar imagen
from PIL import Image
img = Image.open("foto.jpg")
print(img.size)  # ¿Es muy pequeña?

# Mostrar rostros detectados
import cv2
import face_recognition
image = face_recognition.load_image_from_file("foto.jpg")
face_locations = face_recognition.face_locations(image)
print(f"Rostros detectados: {len(face_locations)}")
```

### Problema: "Score bajo"
```python
# Comparar embeddings manualmente
distances = face_recognition.face_distance([embedding1], embedding2)
print(f"Distancia: {distances[0]:.4f}")  # Menor = más parecido
print(f"Score: {(1 - distances[0]) * 100:.1f}%")
```

### Problema: "Base de datos no inicializa"
```bash
# Verificar conexión
psql -U usuario -d comunidad_db -c "SELECT 1"

# Ver migraciones pendientes
alembic current

# Ver error exacto de migración
alembic upgrade head --sql
```

---

## 📦 Paquetes Clave

| Paquete | Para | Línea |
|---------|------|-------|
| fastapi | Backend | `from fastapi import FastAPI` |
| sqlalchemy | ORM BD | `from sqlalchemy import Column, String` |
| pydantic | Validación | `from pydantic import BaseModel, EmailStr` |
| face_recognition | Facial | `import face_recognition` |
| python-jose | JWT | `from jose import jwt` |
| vue | Frontend | `import { createApp } from 'vue'` |
| pinia | State | `import { defineStore } from 'pinia'` |
| axios | HTTP | `import axios from 'axios'` |

---

## ⚙️ .env Mínimo

```
# Database
DATABASE_URL=postgresql://usuario:pass@localhost:5432/comunidad_db

# JWT
SECRET_KEY=tu-secreto-super-seguro-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Facial
FACE_DISTANCE_THRESHOLD=0.6

# Frontend (en archivo .env frontend/)
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 🚨 Checklist Antes de Producción

- [ ] `SECRET_KEY` cambio a valor aleatorio seguro
- [ ] `DATABASE_URL` apunta a PostgreSQL de producción
- [ ] Fotos almacenadas en S3/Azure (no locales)
- [ ] CORS configurado solo para tu dominio
- [ ] HTTPS activado
- [ ] Rate limiting en endpoints facial
- [ ] Logs habilitados para auditoría
- [ ] Tests pasando (pytest + vitest)
- [ ] BD hecha backup

---

## 📚 Links Rápidos

- [README.md](README.md) – Inicio rápido
- [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md) – Define tus campos
- [ARQUITECTURA.md](ARQUITECTURA.md) – Especificación completa
- [ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md) – Código funcional
- [INDICE.md](INDICE.md) – Mapa de documentación

---

**🎯 Necesitas algo?** Usa Ctrl+F para buscar en este documento o consulta [INDICE.md](INDICE.md) para ir al documento específico.

