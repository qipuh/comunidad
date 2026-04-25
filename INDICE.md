# 📖 Índice Completo – Sistema de Gestión Comunitaria

Navega fácilmente por toda la documentación. **Comienza por [CAMPOS_PERSONALIZADOS.md](#campos-personalizados) si es tu primera vez.**

---

## 📍 Comienza Aquí

1. **⭐ [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md)** — Define tus campos (número casa, profesión, etc.)
2. **[README.md](README.md)** — Resumen ejecutivo y quick start
3. **[ARQUITECTURA.md](ARQUITECTURA.md)** — Especificación técnica completa

---

## 📚 Documentación Completa

### 1. README.md
**📄 Resumen General y Quick Start**

| Sección | Descripción |
|---------|-------------|
| Contenido de Documentación | Links a todos los documentos |
| 🎯 Módulos del Sistema | Resumen de Registro, Aportaciones, Reuniones, Elecciones |
| 🏗️ Stack Tecnológico | Backend (FastAPI), Frontend (Vue.js 3), BD (PostgreSQL) |
| 🚀 Quick Start | Pasos para configurar backend y frontend |
| 🔐 Flujo de Reconocimiento Facial | Cómo funcionan los embeddings |
| 📊 Modelos de Datos | Tablas principales (resumen) |
| 🔒 Seguridad | JWT, CORS, Rate Limiting, Auditoría |
| 📈 Reportes | Qué se puede reportar |
| 🎨 Interfaz de Usuario | Páginas y componentes Vue.js |
| 📝 Próximos Pasos | Checklist de implementación |

**👉 [Ir a README.md](README.md)**

---

### 2. ARQUITECTURA.md
**🏗️ Especificación Técnica Completa**

| Sección | Contenido |
|---------|----------|
| 1. DER | Diagrama entidad-relación (usuarios, familias, fotos, aportaciones, reuniones, elecciones) |
| 2. Arquitectura de Capas | Frontend/Backend/BD, estructura de carpetas |
| 3. Reconocimiento Facial | Embeddings vs imágenes crudas, almacenamiento |
| 4. Lógica de Comparación | Distancia euclidiana, score 0-100 |
| 5. Flujos Principales | Registro, asistencia, voto |
| 6. Configuración de Frecuencias | Cambiar período sin perder histórico |
| 7. Seguridad | JWT, encriptación, validación, auditoría |

**👉 [Ir a ARQUITECTURA.md](ARQUITECTURA.md)**

---

### 3. MODELOS_DATOS.md
**💾 Código SQLAlchemy para Todos los Modelos**

| Modelo | Campos Principales |
|--------|------------------|
| **Usuario** | email, nombre, rol, estado, familia_id, **[CAMPOS ABIERTOS]** |
| **Familia** | nombre_grupo, jefe_id, direccion |
| **FotoUsuario** | usuario_id, tipo, embedding (vector), url_archivo |
| **Aportacion** | usuario_id, tipo, monto, fecha, periodo_id |
| **PeriodoAporte** | frecuencia, fecha_inicio, fecha_fin |
| **Reunion** | titulo, fecha, quorum, requiere_validacion_facial |
| **Asistencia** | reunion_id, usuario_id, presente, score_facial |
| **Eleccion** | titulo, fechas, estado, padron, umbral_facial |
| **Candidato** | nombre, numero_orden, votos_recibidos |
| **Voto** | eleccion_id, candidato_id, token_anonimo, fingerprint |

**Incluye:**
- ✅ Enums completos (RolEnum, EstadoEnum, TipoAporteEnum, etc.)
- ✅ Relaciones y constraints
- ✅ **Sección ABIERTA para campos personalizados**
- ✅ Instrucciones paso a paso para agregar campos

**👉 [Ir a MODELOS_DATOS.md](MODELOS_DATOS.md)**

---

### 4. ESTRUCTURA_PROYECTO.md
**📁 Árbol Completo de Carpetas y Archivos**

| Parte | Descripción |
|------|-------------|
| Backend | app/, models/, schemas/, routes/, services/, db/, migrations/, tests/ |
| Frontend | src/, pages/, components/, stores/, router/, services/, composables/, types/, utils/ |
| DevOps | Docker, docker-compose.yml, requirements.txt, package.json |

**Incluye:**
- ✅ Estructura completa (backend + frontend)
- ✅ Setup: virtualenv, npm install, Docker
- ✅ Variables de entorno (.env)
- ✅ Dependencias (Python + Node.js)
- ✅ Comandos para instalar y ejecutar

**👉 [Ir a ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md)**

---

### 5. ENDPOINTS_EJEMPLOS.md
**💻 Código Funcionable: Backend y Frontend**

| Sección | Código |
|---------|--------|
| 1. Registrar Usuario | Schema Pydantic, FacialRecognitionService, POST /usuarios/registro |
| 2. Validar Asistencia | POST /reuniones/{id}/validar-asistencia, comparación facial |
| 3. Votar Secreto | POST /elecciones/{id}/votar, token anónimo, fingerprint |
| 4. FaceScanner.vue | Componente captura 3 fotos (frontal, lateral, lateral) |
| 5. FaceValidator.vue | Componente validación en vivo |
| 6. Servicios | useFaceCapture.ts, useFaceValidation.ts |

**Incluye:**
- ✅ Código Python completo (backend)
- ✅ Código TypeScript/Vue (frontend)
- ✅ Composables y servicios reutilizables
- ✅ Manejo de errores

**👉 [Ir a ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md)**

---

### 6. CAMPOS_PERSONALIZADOS.md ⭐
**🎯 TU SECCIÓN PARA CONFIGURAR CAMPOS**

| Parte | Acción |
|------|--------|
| Tabla de Campos | Completa con tus necesidades (6 ejemplos) |
| Referencia de Tipos | String, Integer, DateTime, Boolean, Enum, JSON, etc. |
| Paso a Paso Implementación | Cómo agregar campos al código |
| Validaciones | Ejemplos en Python y TypeScript |
| Reportes | Cómo usar los campos en reportes |
| Checklist | Pasos de implementación |
| FAQs | Preguntas frecuentes |

**Incluye:**
- ✅ Tabla para rellenar (6 campos de ejemplo)
- ✅ Cómo modificar modelos SQLAlchemy
- ✅ Cómo actualizar schemas Pydantic
- ✅ Cómo crear migraciones Alembic
- ✅ Cómo actualizar endpoints
- ✅ Cómo actualizar formularios Vue.js
- ✅ Validaciones y casos de uso

**👉 [Ir a CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md)** ⭐ **COMPLETA ESTO PRIMERO**

---

## 🗺️ Mapa de Lectura Recomendado

### 👨‍💼 Si eres Gestor/Administrador:
```
1. README.md (descripción general)
   ↓
2. ARQUITECTURA.md secciones 1-5 (flujos principales)
   ↓
3. CAMPOS_PERSONALIZADOS.md (agrega tus campos)
```

### 👨‍💻 Si eres Desarrollador Backend:
```
1. README.md (stack tecnológico)
   ↓
2. ARQUITECTURA.md secciones 3-4 (facial logic)
   ↓
3. MODELOS_DATOS.md (código SQLAlchemy)
   ↓
4. ENDPOINTS_EJEMPLOS.md secciones 1-3 (API endpoints)
   ↓
5. ESTRUCTURA_PROYECTO.md (setup backend)
   ↓
6. CAMPOS_PERSONALIZADOS.md (implementar campos)
```

### 👩‍💻 Si eres Desarrollador Frontend:
```
1. README.md (stack tecnológico)
   ↓
2. ESTRUCTURA_PROYECTO.md (setup frontend)
   ↓
3. ENDPOINTS_EJEMPLOS.md secciones 4-6 (componentes Vue)
   ↓
4. CAMPOS_PERSONALIZADOS.md (agregar campos a formularios)
```

### 🔐 Si trabajas en Seguridad:
```
1. ARQUITECTURA.md sección 7 (seguridad)
   ↓
2. MODELOS_DATOS.md (campos de auditoría: fingerprint, token_anonimo)
   ↓
3. ENDPOINTS_EJEMPLOS.md sección 3 (voto secreto + auditoría)
```

---

## 🔍 Índice por Palabra Clave

### Facial Recognition
- **ARQUITECTURA.md** → Secciones 3-4
- **ENDPOINTS_EJEMPLOS.md** → Secciones 1-3, 5
- **MODELOS_DATOS.md** → FotoUsuario, embedding

### Base de Datos
- **MODELOS_DATOS.md** → Todos los modelos
- **ARQUITECTURA.md** → Sección 1 (DER)
- **ESTRUCTURA_PROYECTO.md** → Sección db/

### Vue.js 3
- **ENDPOINTS_EJEMPLOS.md** → Secciones 4-6
- **ESTRUCTURA_PROYECTO.md** → frontend/src/

### FastAPI
- **ENDPOINTS_EJEMPLOS.md** → Secciones 1-3
- **ESTRUCTURA_PROYECTO.md** → backend/app/routes/

### Seguridad & Auditoría
- **ARQUITECTURA.md** → Sección 7
- **MODELOS_DATOS.md** → Voto (token_anonimo, fingerprint)
- **ENDPOINTS_EJEMPLOS.md** → Sección 3 (voto secreto)

### Campos Personalizados
- **CAMPOS_PERSONALIZADOS.md** → TODO (completar)
- **MODELOS_DATOS.md** → Usuario model (CAMPOS ABIERTOS)

### Docker & Deploy
- **ESTRUCTURA_PROYECTO.md** → Secciones docker-compose, instalación

---

## 📊 Tabla Rápida de Referencias

| Necesito... | Ir a... | Sección |
|-----------|--------|--------|
| Ver estructura global | README.md | "📑 Contenido de la Documentación" |
| Entender cómo funciona lo facial | ARQUITECTURA.md | 3-4 |
| Ver código SQL | MODELOS_DATOS.md | Modelos (Usuario, FotoUsuario, etc.) |
| Ver código Python | ENDPOINTS_EJEMPLOS.md | 1-3 |
| Ver código Vue.js | ENDPOINTS_EJEMPLOS.md | 4-6 |
| Setup local | ESTRUCTURA_PROYECTO.md | "Instalación y Setup" |
| Variables .env | ESTRUCTURA_PROYECTO.md | "Variables de Entorno (.env)" |
| Agregar campo nuevo | CAMPOS_PERSONALIZADOS.md | "Cómo Implementar Los Campos" |
| Validar datos | CAMPOS_PERSONALIZADOS.md | "Validaciones Recomendadas" |
| Crear reporte | CAMPOS_PERSONALIZADOS.md | "Reportes con Campos Personalizados" |
| Seguridad | ARQUITECTURA.md | 7 |
| Auditoría | ENDPOINTS_EJEMPLOS.md | Sección 3 (Voto) |

---

## ✨ Funcionalidades Clave por Documento

### README.md
- ✅ Visión general del proyecto
- ✅ Quick start (3 comandos)
- ✅ Tips importantes
- ✅ Checklist de implementación

### ARQUITECTURA.md
- ✅ Diseño completo del sistema
- ✅ Flujos de usuario (happy path)
- ✅ Matemática del reconocimiento facial
- ✅ Seguridad y auditoría

### MODELOS_DATOS.md
- ✅ Código SQLAlchemy 100% funcional
- ✅ Todas las relaciones (1:N, N:N)
- ✅ Enums y tipos de datos
- ✅ Tabla ABIERTA para completar

### ESTRUCTURA_PROYECTO.md
- ✅ Árbol de carpetas exacto
- ✅ Instalación paso a paso
- ✅ Dependencias de Python y Node
- ✅ Variables de entorno

### ENDPOINTS_EJEMPLOS.md
- ✅ Código Python listo para copiar
- ✅ Código Vue.js listo para copiar
- ✅ Composables reutilizables
- ✅ Manejo de errores

### CAMPOS_PERSONALIZADOS.md
- ✅ Tabla para completar (TÚ)
- ✅ Paso a paso de implementación
- ✅ Validaciones
- ✅ Ejemplos prácticos

---

## 🎯 ¿Por Dónde Empiezo?

### Opción A: Solo quiero entender la idea
```
1. README.md (5 min)
2. ARQUITECTURA.md secciones 1-5 (10 min)
```

### Opción B: Voy a desarrollar
```
1. CAMPOS_PERSONALIZADOS.md (5 min - completar tabla)
2. README.md (5 min)
3. ESTRUCTURA_PROYECTO.md (10 min - setup)
4. ENDPOINTS_EJEMPLOS.md (20 min - código)
5. MODELOS_DATOS.md (consultar mientras codifico)
```

### Opción C: Voy a deployar
```
1. ARQUITECTURA.md sección 7 (seguridad)
2. ESTRUCTURA_PROYECTO.md (docker-compose)
3. README.md (checklist)
```

---

## 🚀 Siguientes Pasos

**1. Lee esto:** [README.md](README.md)
**2. Completa esto:** [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md)
**3. Comienza a codificar** con los ejemplos de [ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md)

---

## 📞 ¿Preguntas?

- ❓ "¿Cómo agrego un campo nuevo?" → [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md)
- ❓ "¿Cómo funciona el reconocimiento facial?" → [ARQUITECTURA.md](ARQUITECTURA.md) sección 3-4
- ❓ "¿Dónde está el código SQL?" → [MODELOS_DATOS.md](MODELOS_DATOS.md)
- ❓ "¿Cómo inicio el proyecto?" → [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md)
- ❓ "¿Cómo codifico los endpoints?" → [ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md)
- ❓ "¿Cómo funciona el voto secreto?" → [ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md) sección 3

---

**¡La documentación está completa! Abre [CAMPOS_PERSONALIZADOS.md](CAMPOS_PERSONALIZADOS.md) y comienza.** 🎯

