# Estructura de Carpetas del Proyecto

## BACKEND (FastAPI + SQLAlchemy + PostgreSQL)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # Punto de entrada FastAPI
│   ├── config.py                        # Variables de configuración
│   │
│   ├── models/                          # SQLAlchemy ORM
│   │   ├── __init__.py
│   │   ├── base.py                      # Base declarativa
│   │   ├── usuario.py                   # Usuario, Familia, RolEnum, EstadoEnum
│   │   ├── foto.py                      # FotoUsuario
│   │   ├── aportacion.py                # Aportacion, PeriodoAporte
│   │   ├── reunion.py                   # Reunion, Asistencia
│   │   └── eleccion.py                  # Eleccion, Candidato, Voto
│   │
│   ├── schemas/                         # Pydantic validators (DTOs)
│   │   ├── __init__.py
│   │   ├── usuario_schema.py            # UsuarioCreate, UsuarioResponse, etc.
│   │   ├── aportacion_schema.py
│   │   ├── reunion_schema.py
│   │   └── eleccion_schema.py
│   │
│   ├── routes/                          # API endpoints
│   │   ├── __init__.py
│   │   ├── usuarios.py                  # POST /usuarios, GET /usuarios/{id}, etc.
│   │   ├── aportaciones.py              # CRUD aportaciones, reportes
│   │   ├── reuniones.py                 # Crear reunión, marcar asistencia
│   │   ├── elecciones.py                # Crear elección, validar voto
│   │   └── auth.py                      # Login, JWT
│   │
│   ├── services/                        # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── facial_recognition.py        # Generar embedding, validar rostro
│   │   ├── usuario_service.py           # CRUD usuario, manejo de familia
│   │   ├── aportacion_service.py        # Reportes, deudas, morosidad
│   │   ├── reunion_service.py           # Asistencia, quórum
│   │   ├── eleccion_service.py          # Voto, auditoría
│   │   └── storage.py                   # Subir fotos a S3/Azure Blob
│   │
│   ├── dependencies/                    # Inyección de dependencias FastAPI
│   │   ├── __init__.py
│   │   ├── auth.py                      # get_current_user()
│   │   └── db.py                        # get_db()
│   │
│   ├── utils/                           # Utilidades varias
│   │   ├── __init__.py
│   │   ├── validators.py                # Email, teléfono, etc.
│   │   └── helpers.py                   # Funciones auxiliares
│   │
│   └── db/
│       ├── __init__.py
│       └── database.py                  # Conexión a BD, SessionLocal
│
├── migrations/                          # Alembic (schema migrations)
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_initial.py
│       └── ...
│
├── tests/                               # Tests unitarios e integración
│   ├── __init__.py
│   ├── test_usuarios.py
│   ├── test_facial.py
│   └── conftest.py                      # Fixtures pytest
│
├── requirements.txt                     # Dependencias Python
├── .env.example                         # Variables de entorno (ejemplo)
├── .env                                 # Variables de entorno (NO comitir)
├── Dockerfile                           # Para despliegue
└── docker-compose.yml                   # BD + Backend


FRONTEND (Vue.js 3 + Vite + Pinia)

```
frontend/
├── src/
│   ├── App.vue                          # Componente raíz
│   ├── main.ts                          # Entry point
│   │
│   ├── assets/
│   │   ├── styles/
│   │   │   ├── main.css
│   │   │   └── tailwind.css
│   │   └── images/
│   │
│   ├── components/                      # Componentes reutilizables
│   │   ├── common/
│   │   │   ├── Header.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── Modal.vue
│   │   │
│   │   ├── facial/
│   │   │   ├── FaceScanner.vue          # Captura 3 fotos (registro)
│   │   │   ├── FaceValidator.vue        # Validación en tiempo real
│   │   │   └── FaceDebug.vue            # Debug: muestra embedding
│   │   │
│   │   ├── usuario/
│   │   │   ├── FormUsuario.vue
│   │   │   ├── FormFamilia.vue
│   │   │   └── ListaUsuarios.vue
│   │   │
│   │   ├── aportacion/
│   │   │   ├── FormAportacion.vue
│   │   │   ├── TablaAportaciones.vue
│   │   │   └── ReporteDeudas.vue
│   │   │
│   │   ├── reunion/
│   │   │   ├── FormReunion.vue
│   │   │   ├── ListaReuniones.vue
│   │   │   └── AsistenciaFacial.vue     # Validación facial en vivo
│   │   │
│   │   └── eleccion/
│   │       ├── FormEleccion.vue
│   │       ├── ListaCandidatos.vue
│   │       ├── PantallaVotacion.vue     # Validación facial + voto
│   │       └── ResultadosEleccion.vue
│   │
│   ├── pages/                           # Vistas/páginas
│   │   ├── Home.vue
│   │   ├── RegistroUsuario.vue          # /registro
│   │   ├── Perfil.vue                   # /perfil
│   │   ├── Aportaciones.vue             # /aportaciones
│   │   ├── Reuniones.vue                # /reuniones
│   │   ├── Elecciones.vue               # /elecciones
│   │   ├── Reportes.vue                 # /reportes (admin)
│   │   ├── Administracion.vue           # /admin
│   │   └── Login.vue                    # /login
│   │
│   ├── stores/                          # Pinia (state management)
│   │   ├── index.ts
│   │   ├── usuario.ts                   # usuarioStore
│   │   ├── aportacion.ts                # aportacionStore
│   │   ├── reunion.ts                   # reunionStore
│   │   ├── eleccion.ts                  # eleccionStore
│   │   └── auth.ts                      # authStore (JWT)
│   │
│   ├── router/                          # Vue Router
│   │   └── index.ts                     # Rutas y guards
│   │
│   ├── services/                        # Comunicación con API
│   │   ├── api.ts                       # Configuración axios
│   │   ├── usuario.service.ts           # GET/POST /usuarios
│   │   ├── facial.service.ts            # POST /facial/upload, /facial/validate
│   │   ├── aportacion.service.ts        # CRUD aportaciones
│   │   ├── reunion.service.ts           # CRUD reuniones
│   │   └── eleccion.service.ts          # CRUD elecciones, votar
│   │
│   ├── composables/                     # Vue 3 Composition API
│   │   ├── useFaceCapture.ts            # Captura cámara (3 fotos)
│   │   ├── useFaceValidation.ts         # Validación en tiempo real
│   │   ├── useForm.ts                   # Validación de formularios
│   │   └── useAuth.ts                   # Autenticación (JWT)
│   │
│   ├── types/                           # TypeScript interfaces
│   │   ├── usuario.ts
│   │   ├── aportacion.ts
│   │   ├── reunion.ts
│   │   └── eleccion.ts
│   │
│   └── utils/                           # Utilidades
│       ├── validators.ts
│       └── helpers.ts
│
├── public/
│   └── index.html                       # HTML principal
│
├── tests/
│   ├── unit/
│   └── e2e/
│
├── package.json
├── vite.config.ts
├── tsconfig.json
├── .env.example
├── .env                                 # NO comitir
└── Dockerfile


RAÍZ DEL PROYECTO

```
comunidad/
├── backend/                             # Carpeta backend (como arriba)
├── frontend/                            # Carpeta frontend (como arriba)
├── docker-compose.yml                   # Orquestación local (backend + BD)
├── README.md                            # Documentación general
├── ARQUITECTURA.md                      # Especificación técnica (tu documento)
├── MODELOS_DATOS.md                     # Modelos SQLAlchemy (tu documento)
├── ESTRUCTURA_PROYECTO.md               # Este archivo
└── ENDPOINTS_EJEMPLOS.md                # Ejemplos de código (próximo documento)
```

---

## Instalación y Setup

### Backend

```bash
# 1. Crear virtualenv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r backend/requirements.txt

# 3. Crear base de datos
cd backend
alembic upgrade head

# 4. Ejecutar servidor
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
# 1. Instalar dependencias
cd frontend
npm install

# 2. Ejecutar servidor de desarrollo
npm run dev
# La app estará en http://localhost:5173
```

### Docker Compose (Recomendado para producción)

```bash
docker-compose up -d
# Backend en http://localhost:8000
# Frontend en http://localhost:3000
# PostgreSQL en localhost:5432
```

---

## Variables de Entorno (.env)

### Backend

```
# Database
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/comunidad_db

# JWT
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS S3 (para subir fotos)
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_BUCKET=comunidad-fotos
AWS_REGION=us-east-1

# Face Recognition
FACE_RECOGNITION_MODEL=hog  # o cuda si tienes GPU
FACE_DISTANCE_THRESHOLD=0.6

# CORS
FRONTEND_URL=http://localhost:5173
```

### Frontend

```
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Comunidad
VITE_APP_LOGO_URL=/logo.png
```

---

## Dependencias Principales

### Backend (requirements.txt)

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
aiofiles==23.2.1
requests==2.31.0
boto3==1.29.7
face-recognition==1.3.5
numpy==1.24.3
pillow==10.1.0
opencv-python==4.8.1.78
```

### Frontend (package.json)

```json
{
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.6",
    "axios": "^1.6.2",
    "tracking": "^0.7.3",
    "mediapipe": "^0.8.9",
    "chart.js": "^4.4.0",
    "vue-chartjs": "^5.2.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "vite": "^5.0.8",
    "@vitejs/plugin-vue": "^5.0.0",
    "tailwindcss": "^3.4.1",
    "autoprefixer": "^10.4.16"
  }
}
```

