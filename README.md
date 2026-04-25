# 🏘️ Sistema de Gestión Comunitaria – Documentación Completa

**Especificación técnica y plan de implementación** para una plataforma comunitaria con reconocimiento facial biométrico.

---

## 📑 Contenido de la Documentación

### 1. **[ARQUITECTURA.md](ARQUITECTURA.md)**
   - Diagrama de entidad-relación (usuarios, familias, aportaciones, reuniones, elecciones)
   - Arquitectura de capas (Frontend/Backend/BD)
   - Flujo de reconocimiento facial (embeddings vs imágenes crudas)
   - Lógica de comparación facial (distancia euclidiana)
   - Flujos principales de cada módulo
   - Configuración de frecuencias de aporte
   - Seguridad (JWT, CORS, Rate Limiting, Auditoría)

### 2. **[MODELOS_DATOS.md](MODELOS_DATOS.md)**
   - Código SQLAlchemy para todos los modelos
   - Definición de campos, relaciones y tipos de datos
   - **SECCIÓN ABIERTA**: Campos personalizados que puedes agregar al modelo `Usuario`
   - Enums (RolEnum, EstadoEnum, TipoAporteEnum, etc.)

### 3. **[ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md)**
   - Árbol de carpetas completo (backend + frontend + raíz)
   - Descripción de cada carpeta y archivo
   - Instalación y setup (virtualenv, npm, Docker)
   - Variables de entorno (.env)
   - Dependencias principales (Python, Node.js)

### 4. **[ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md)**
   - **Código ejemplo: Registrar usuario + subir 3 fotos**
   - **Código ejemplo: Validar asistencia facial en reunión**
   - **Código ejemplo: Votar con validación facial + voto secreto**
   - Componentes Vue.js 3 (Composition API)
   - Composables para captura y validación facial
   - Servicios de comunicación con API

### 5. **[CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md)** ⭐
   - **Tu sección para definir campos adicionales**
   - Tabla para completar con tus necesidades
   - Referencia de tipos de datos
   - Paso a paso para implementar los campos
   - Ejemplos de validaciones
   - Casos de uso prácticos

---

## 🎯 Módulos del Sistema

### 1. **REGISTRO DE USUARIOS**
- Datos básicos: nombre, email, teléfono, rol, estado
- **Familia**: Jefe de familia + miembros (conyuge, hijos)
- Campos heredables: dirección, número de casa
- Fotos: 3 capturas (frontal, lateral izq., lateral der.)
- Embeddings: Almacenamiento de vectores (128D) para comparación
- **Campos abiertos**: Número de casa, fecha de ingreso, profesión, etc. (completar en [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md))

### 2. **APORTACIONES**
- Tipos: Ordinaria, Extraordinaria, Donación
- Frecuencia: Configurable (mensual, trimestral, anual, etc.)
- Registro: Monto, fecha, forma de pago, comprobante (opcional)
- Reportes: Deudas, morosidad, aportes por período
- Histórico: No se pierde al cambiar frecuencia

### 3. **REUNIONES**
- Crear: Título, fecha, hora, lugar, orden del día, quórum
- **Asistencia facial**: Captura rostro en vivo → Compara con 3 fotos almacenadas
- Score: 0-100 (configurable umbral)
- Registro: Presente/Ausente, hora de llegada, score facial
- Reporte: Quórum alcanzado, asistencia por usuario

### 4. **ELECCIONES**
- Crear: Título, fechas, candidatos, padrón habilitado
- **Validación facial**: Foto en vivo → Identidad validada
- **Voto secreto**: Token anónimo (desvincula usuario_id del voto)
- **Auditoría**: Fingerprint (trazabilidad sin revelar voto)
- Resultados: Votos por candidato, porcentajes

---

## 🏗️ Stack Tecnológico

### Backend
- **Framework**: FastAPI (documentación automática, async/await)
- **ORM**: SQLAlchemy
- **BD**: PostgreSQL (producción) / SQLite (desarrollo)
- **Reconocimiento Facial**: `face_recognition` o `insightface`
- **Almacenamiento**: AWS S3 o Azure Blob Storage
- **Autenticación**: JWT (python-jose)
- **Migraciones**: Alembic

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **Build Tool**: Vite
- **State**: Pinia
- **Routing**: Vue Router
- **HTTP**: Axios
- **Captura Facial**: MediaPipe / tracking.js
- **Estilos**: Tailwind CSS

### DevOps
- **Containerización**: Docker
- **Orquestación**: Docker Compose
- **Tests**: Pytest (backend), Vitest (frontend)

---

## 🚀 Quick Start

### 1. **Completar campos personalizados**
```markdown
Abre: CAMPOS_PERSONALIZADOS.md
Completa la tabla con los campos que necesitas
Ejemplo: numero_casa, fecha_ingreso, profesion, etc.
```

### 2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
# Backend en http://localhost:8000
```

### 3. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
# Frontend en http://localhost:5173
```

### 4. **BD (Docker)**
```bash
docker-compose up -d
# PostgreSQL en localhost:5432
```

---

## 🔐 Flujo de Reconocimiento Facial

### Registro (Guardar identidad)
```
1. Usuario sube 3 fotos (frontal, lateral izq., lateral der.)
   ↓
2. Backend: Detecta rostro → Genera embedding (vector 128D)
   ↓
3. Almacenar embedding en BD (JSON)
   ↓
4. Guardar foto en cloud (S3/Azure) para auditoría
```

### Validación (Comparar en tiempo real)
```
1. Usuario abre cámara en reunión/elección
   ↓
2. Captura rostro vivo → Envía foto a backend
   ↓
3. Backend: Genera embedding de captura viva
   ↓
4. Calcula distancia euclidiana con 3 embeddings almacenados
   ↓
5. Score = (1 - distancia_promedio) × 100
   ↓
6. Si score ≥ umbral → ACCESO PERMITIDO ✓
```

### Matemática
```
Distancia Euclidiana: d = √(Σ(embedding_vivo[i] - embedding_almacenado[i])²)

Score: (1 - d) × 100
  - d = 0 → score = 100% (coincidencia perfecta)
  - d = 1 → score = 0% (sin coincidencia)
  - Umbral típico: 60-70%
```

---

## 📊 Modelos de Datos

### Usuarios
```
Usuario
├─ email (unique)
├─ nombre
├─ telefono
├─ rol (enum: vecino, admin, tesorero, junta)
├─ estado (enum: activo, inactivo, suspendido)
├─ familia_id (FK)
├─ es_jefe_familia
├─ direccion
└─ [CAMPOS PERSONALIZADOS] ← Completar en CAMPOS_PERSONALIZADOS.md
```

### Familia
```
Familia
├─ nombre_grupo
├─ jefe_id (FK Usuario)
├─ direccion
└─ usuarios (1:N)
```

### Fotos & Embeddings
```
FotoUsuario
├─ usuario_id (FK)
├─ tipo (frontal, lateral_izquierdo, lateral_derecho)
├─ embedding (vector 128D como JSON)
└─ url_archivo (cloud storage)
```

### Aportaciones
```
Aportacion
├─ usuario_id (FK)
├─ tipo (ordinaria, extraordinaria, donacion)
├─ monto
├─ fecha
├─ forma_pago
├─ comprobante_url
└─ periodo_id (FK)

PeriodoAporte
├─ frecuencia (mensual, trimestral, anual, etc.)
├─ fecha_inicio, fecha_fin
└─ estado
```

### Reuniones & Asistencia
```
Reunion
├─ titulo, fecha, hora, lugar
├─ orden_dia
├─ quorum_requerido
├─ requiere_validacion_facial
└─ asistencias (1:N)

Asistencia
├─ reunion_id (FK)
├─ usuario_id (FK)
├─ presente (bool)
├─ score_facial (0-100)
└─ validated_at
```

### Elecciones & Votos
```
Eleccion
├─ titulo, fechas
├─ estado (abierta, cerrada, resultados)
├─ padron_usuario_ids (JSON)
├─ umbral_facial
└─ candidatos, votos (1:N)

Voto
├─ eleccion_id (FK)
├─ candidato_id (FK)
├─ usuario_id (FK) → se anula después de validación
├─ token_anonimo (UNIQUE)
├─ score_facial
└─ fingerprint (auditoría)
```

---

## 🔒 Seguridad

| Aspecto | Implementación |
|--------|-----------------|
| **Autenticación** | JWT (tokens con expiración) |
| **Autorización** | Roles (admin, tesorero, vecino, etc.) |
| **API** | CORS configurado, Rate Limiting en endpoints facial |
| **BD** | Contraseñas hasheadas (bcrypt), conexión SSL |
| **Almacenamiento** | Fotos encriptadas en S3/Azure |
| **Privacidad** | Voto secreto (token anónimo desvinculado) |
| **Auditoría** | Fingerprint de votos, logs de cambios |
| **Validación** | Embedding + foto original (no solo facial) |

---

## 📈 Reportes Disponibles

- **Usuarios**: Listado, activos/inactivos, por rol, por familia
- **Aportaciones**: Deudores, morosidad, aportes por período, ingresos totales
- **Reuniones**: Asistencia, quórum, score facial promedio
- **Elecciones**: Votos por candidato, participación, auditoría de identidades
- **Personalizados**: Por profesión, por antigüedad, etc. (usando campos abiertos)

---

## 🎨 Interfaz de Usuario (Vue.js)

### Páginas Principales
- **Home**: Dashboard con resumen
- **Registro**: Registro usuario + captura 3 fotos
- **Perfil**: Ver/editar datos, cambiar foto
- **Aportaciones**: Ver estado, agregar aporte, reportes
- **Reuniones**: Listar, marcar asistencia (facial)
- **Elecciones**: Ver candidatos, votar (facial + secreto)
- **Admin**: Crear usuarios, gestionarperiodos, reportes
- **Login**: Autenticación con JWT

### Componentes Reutilizables
- `FaceScanner`: Captura 3 fotos
- `FaceValidator`: Validación en tiempo real
- `FormUsuario`: CRUD usuarios
- `TablaAportaciones`: Listado con filtros
- `ReporteDeudas`: Estadísticas de morosidad
- `Modal`, `Header`, `Sidebar`: UI común

---

## 📝 Próximos Pasos

### 1. **Completar Campos Personalizados** ⭐
   - Abre [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md)
   - Completa la tabla con tus campos
   - Sigue el paso a paso para implementar

### 2. **Clonar y Configurar Proyecto**
```bash
git clone <repo>
cd comunidad
cp .env.example .env
# Editar .env con tus valores
```

### 3. **Crear BD**
```bash
cd backend
python -m venv venv
. venv/Scripts/activate  # Windows
pip install -r requirements.txt
alembic upgrade head
```

### 4. **Instalar Dependencias Frontend**
```bash
cd frontend
npm install
```

### 5. **Ejecutar en Desarrollo**
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: BD (si usas Docker)
docker-compose up -d
```

### 6. **Escribir Tests**
- Tests unitarios para validación facial
- Tests de endpoints (usuarios, aportaciones, etc.)
- Tests E2E (registro completo, votación, etc.)

### 7. **Deployar**
```bash
# Producción con Docker
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🤝 Contribución y Soporte

### Estructura Recomendada
```
comunidad/
├── backend/          # FastAPI + SQLAlchemy
├── frontend/         # Vue.js 3
├── docker-compose.yml
├── ARQUITECTURA.md
├── MODELOS_DATOS.md
├── ESTRUCTURA_PROYECTO.md
├── ENDPOINTS_EJEMPLOS.md
└── CAMPOS_PERSONALIZADOS.md  ← Completar primero
```

### Checklist Antes de Comenzar
- [ ] Leí ARQUITECTURA.md
- [ ] Completé CAMPOS_PERSONALIZADOS.md
- [ ] Instalé backend (Python 3.9+)
- [ ] Instalé frontend (Node.js 16+)
- [ ] Configuré .env
- [ ] Creé la BD (alembic upgrade head)
- [ ] Ejecuté backend (uvicorn)
- [ ] Ejecuté frontend (npm run dev)
- [ ] Probé http://localhost:5173

---

## 💡 Tips Importantes

1. **Embeddings**: No guardamos fotos en BD, solo vectores 128D. Ahorras ~95% de espacio.

2. **Escalabilidad**: Para N usuarios, cada validación es O(3) comparaciones (rápido).

3. **Privacidad**: El voto secreto se logra generando token anónimo y anulando usuario_id.

4. **Auditoría**: El fingerprint permite rastrear fraude sin revelar identidad.

5. **Campos Abiertos**: El sistema soporta agregar campos nuevos sin romper la lógica.

6. **Familias**: Los miembros heredan dirección pero mantienen identidad facial única.

7. **Frecuencias**: Cambiar de mensual a trimestral no pierde histórico (vinculado a períodos).

---

## 📚 Documentos Relacionados

- [ARQUITECTURA.md](ARQUITECTURA.md) – Especificación técnica completa
- [MODELOS_DATOS.md](MODELOS_DATOS.md) – Código SQLAlchemy (con Sección 6 de configuración)
- [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md) – Árbol de carpetas
- [ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md) – Código ejemplo (con Secciones 7-9 dinámicas)
- [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md) – Tu sección + opción dinámica
- **[COMPONENTES_DINAMICOS.md](COMPONENTES_DINAMICOS.md) – Ejemplos Vue.js (NUEVO)**
- **[README_CONFIGURACION.md](README_CONFIGURACION.md) – Guía del módulo dinámico**
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md) – Quick reference técnico**

---

## ✨ Características Principales

✅ Registro con validación biométrica (3 fotos)
✅ Familia: jefe + miembros con datos heredados
✅ Aportaciones: frecuencia configurable, reportes de morosidad
✅ Reuniones: asistencia con validación facial en vivo
✅ Elecciones: voto secreto + auditoría sin revelar identidad
✅ **Campos dinámicos: sin migración de BD, solo UI admin**
✅ **Auto-llenado desde APIs: RENIEC (DNI), Facturiza (RUC), SUNAT**
✅ **Encriptación de credenciales: Fernet para tokens de APIs**
✅ JWT: autenticación segura con tokens
✅ API REST: documentación automática (Swagger)
✅ BD Relacional: PostgreSQL con migraciones
✅ Frontend moderno: Vue.js 3 + Composition API
✅ Escalable: Docker, PostgreSQL, S3/Azure
✅ Auditable: logs de quién votó (sin voto)

---

**¡Listo para comenzar! Abre [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md) y completa tu configuración.** 🚀

