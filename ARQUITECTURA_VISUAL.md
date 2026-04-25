# 🏗️ Arquitectura Visual - Sistema de Configuración Dinámico

## 🎯 Flujo General

```
┌─────────────────────────────────────────────────────────────────┐
│                    USUARIO FINAL / ADMIN                        │
│                      (Web Browser)                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
     ┌───────────────────────────────────┐
     │   FRONTEND (Vue.js 3)             │
     │                                   │
     │  ┌──────────────────────────────┐ │
     │  │ Components:                  │ │
     │  │ • ConfiguradorCampos.vue     │ │
     │  │ • ConfiguradorAPIs.vue       │ │
     │  │ • RegistroDinamico.vue       │ │
     │  └──────────────────────────────┘ │
     │                                   │
     │  ┌──────────────────────────────┐ │
     │  │ Services:                    │ │
     │  │ • configuracion.service.ts   │ │
     │  │ • validaciones.service.ts    │ │
     │  └──────────────────────────────┘ │
     └────────────┬─────────────────────┘
                  │
                  │ HTTP REST / JSON
                  ▼
     ┌───────────────────────────────────┐
     │   BACKEND (FastAPI/Python)        │
     │                                   │
     │  ┌──────────────────────────────┐ │
     │  │ Routes:                      │ │
     │  │ • /api/admin/configuracion/* │ │
     │  │ • /api/admin/integraciones/* │ │
     │  │ • /api/validaciones/*        │ │
     │  │ • /api/usuarios/*            │ │
     │  └──────────────────────────────┘ │
     │                                   │
     │  ┌──────────────────────────────┐ │
     │  │ Services:                    │ │
     │  │ • IntegracionAPIService      │ │
     │  └──────────────────────────────┘ │
     │                                   │
     │  ┌──────────────────────────────┐ │
     │  │ Models (SQLAlchemy):         │ │
     │  │ • ConfiguracionCampo         │ │
     │  │ • IntegracionAPI             │ │
     │  │ • ConsultaExterna            │ │
     │  │ • CampoUsuario               │ │
     │  └──────────────────────────────┘ │
     └────────────┬─────────────────────┘
                  │
                  │ SQL
                  ▼
     ┌───────────────────────────────────┐
     │   POSTGRESQL DATABASE             │
     │                                   │
     │  ┌──────────────────────────────┐ │
     │  │ Tablas:                      │ │
     │  │ • integraciones_api          │ │
     │  │ • configuracion_campos       │ │
     │  │ • consultas_externas         │ │
     │  │ • campos_usuario             │ │
     │  └──────────────────────────────┘ │
     └────────────┬─────────────────────┘
                  │
     ┌────────────┴──────────────┐
     │                           │
     ▼                           ▼
┌──────────────────┐    ┌──────────────────┐
│  RENIEC (Perú)   │    │   Facturiza      │
│  (DNI Queries)   │    │   (RUC Queries)  │
└──────────────────┘    └──────────────────┘
     
     ▲                           ▲
     │                           │
     └────────────┬──────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
    ┌────────────┐    ┌────────────┐
    │   SUNAT    │    │  Custom    │
    │   (RUC)    │    │   APIs     │
    └────────────┘    └────────────┘
```

---

## 📱 Componentes Frontend

### 1. ConfiguradorCampos.vue (Admin)
```
┌─────────────────────────────────────┐
│ ⚙️ Configurar Campos de Registro   │
├─────────────────────────────────────┤
│ [➕ Nuevo Campo]                    │
├─────────────────────────────────────┤
│ Orden │ Información      │ Acciones │
│──────────────────────────────────── │
│  ≡ 1  │ DNI (Obligatorio)│[✏️][🗑️]  │
│  ≡ 2  │ Nombre           │[✏️][🗑️]  │
│  ≡ 3  │ Email 🔗 API     │[✏️][🗑️]  │
│  ≡ 4  │ Teléfono         │[✏️][🗑️]  │
└─────────────────────────────────────┘

Modal de Edición:
┌──────────────────────────────────────┐
│ ✏️ Editar Campo          [✕]        │
├──────────────────────────────────────┤
│ Nombre del Campo: [texto________]   │
│ Etiqueta: [Email_____________]      │
│ Tipo de Dato: [dropdown: email]     │
│ Expresión Regex: [^\w+@\w+..._]    │
│ ☑ Obligatorio                       │
│ [API Integraciones: Seleccionar]    │
│ [Enum Values: ____________]         │
│ ☑ Mostrar en registro               │
│ ☑ Mostrar en perfil                 │
│ ☑ Mostrar en reportes               │
├──────────────────────────────────────┤
│ [Cancelar] [💾 Guardar]            │
└──────────────────────────────────────┘
```

### 2. ConfiguradorAPIs.vue (Admin)
```
┌─────────────────────────────────────┐
│ 🔌 Configurar Integraciones API    │
├─────────────────────────────────────┤
│ [➕ Nueva Integración]              │
├─────────────────────────────────────┤
│ Nombre    │ Tipo      │ Estado │ ... │
│─────────────────────────────────── │
│ RENIEC    │ 🇵🇪 RENIEC │ 🟢 Activa   │
│           │           │      │[🧪][✏️][🗑️] │
│ Facturiza │ 📋 RUC    │ 🟢 Activa   │
│           │           │      │[🧪][✏️][🗑️] │
│ SUNAT     │ 🏛️ SUNAT  │ 🔴 Inactiva │
│           │           │      │[🧪][✏️][🗑️] │
└─────────────────────────────────────┘

Modal de Creación:
┌──────────────────────────────────────┐
│ ➕ Nueva Integración      [✕]        │
├──────────────────────────────────────┤
│ Nombre: [RENIEC____________]        │
│ Descripción: [textarea____...]      │
│ Tipo: [dropdown: reniec]            │
│ URL: [https://api.reniec.gob.pe]   │
│ Auth Type: [dropdown: bearer]       │
│ Token: [●●●●●●●●●●] 🔒            │
│                                      │
│ ⚙️ Configuración Avanzada           │
│ Timeout: [30] segundos              │
│ Reintentos: [3]                     │
│ ☑ Activa                            │
├──────────────────────────────────────┤
│ [Cancelar] [💾 Guardar]            │
└──────────────────────────────────────┘

Modal de Resultado de Prueba:
┌──────────────────────────────────────┐
│ ✅ Integración Funcional   [✕]     │
├──────────────────────────────────────┤
│ La API está respondiendo correctamente│
│                                      │
│ Datos Obtenidos:                    │
│ ┌────────────────────────────────┐  │
│ │ {                              │  │
│ │   "nombre": "Juan",            │  │
│ │   "apellido": "Pérez",         │  │
│ │   "fecha_nacimiento": "..."    │  │
│ │ }                              │  │
│ └────────────────────────────────┘  │
├──────────────────────────────────────┤
│ [Cerrar]                             │
└──────────────────────────────────────┘
```

### 3. RegistroDinamico.vue (Usuario)
```
┌─────────────────────────────────────────────────────────────┐
│ 📝 Registro de Usuario                                      │
│ Completa el formulario con tus datos personales            │
├─────────────────────────────────────────────────────────────┤
│ ████████████░░░░░░ 65% completado                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ DNI * [12345678____] [🔗 Validar]  ✅ Validado ext.      │
│ Nombre [Juan__________]                                   │
│ Apellido Paterno [Pérez______]                            │
│ Email * [juan@example.com_________]                        │
│ Teléfono [987654321____]                                  │
│ Fecha Nacimiento [1990-05-15]                             │
│ Estado Civil [dropdown: Soltero]                          │
│ ☑ Acepto términos y condiciones                           │
│                                                             │
│ [🔄 Limpiar] [✅ Registrarse]                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                          📋 Información                     │
│                      ├─────────────────┤                  │
│                      │ Campos: 7       │                  │
│                      │ Obligatorios: 3 │                  │
│                      │ Con validación: 1│                  │
│                      └─────────────────┘                  │
│                                                             │
│                      🔒 Privacidad                         │
│                      ├──────────────────┤                │
│                      │ Tus datos serán  │                │
│                      │ encriptados y    │                │
│                      │ guardados de     │                │
│                      │ forma segura     │                │
│                      └──────────────────┘                │
│                                                             │
│                      💡 Consejos                          │
│                      ├──────────────────┤                │
│                      │ ✓ Usa validar   │                │
│                      │   para auto-ll  │                │
│                      │ ✓ Completa todos│                │
│                      │   los * req.    │                │
│                      │ ✓ Verifica datos│                │
│                      └──────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Interacción

### Admin: Crear Campo con API Integration
```
Admin
  │
  ├─> Navega a /admin/campos
  │   │
  │   ├─> [ConfiguradorCampos.vue]
  │   │   │
  │   │   ├─> GET /api/admin/configuracion/campos
  │   │   │   │
  │   │   │   └─> BACKEND obtiene campos de BD
  │   │   │
  │   │   └─> Hace clic en "➕ Nuevo Campo"
  │   │       │
  │   │       └─> Modal abierto
  │   │           │
  │   │           ├─> Ingresa: "dni", "DNI", "string"
  │   │           ├─> Selecciona API: RENIEC
  │   │           ├─> Ingresa mapping: "dni"
  │   │           │
  │   │           └─> Haz clic en "💾 Guardar"
  │   │               │
  │   │               └─> POST /api/admin/configuracion/campos
  │   │                   │
  │   │                   └─> BACKEND valida y guarda
  │   │                       │
  │   │                       └─> BD: integraciones_api 
  │   │                           BD: configuracion_campos
  │   │
  │   └─> Actualiza lista de campos en UI
  │
  └─> Proceso completado ✅
```

### Usuario: Consultar DNI y Auto-llenar
```
Usuario
  │
  ├─> Navega a /registro
  │   │
  │   ├─> [RegistroDinamico.vue]
  │   │   │
  │   │   ├─> GET /api/admin/configuracion/campos
  │   │   │   │
  │   │   │   └─> BACKEND obtiene campos configurados
  │   │   │
  │   │   └─> Ingresa "12345678" en DNI
  │   │       │
  │   │       └─> Haz clic en [🔗 Validar]
  │   │           │
  │   │           ├─> POST /api/validaciones/consultar-dni
  │   │           │   │
  │   │           │   └─> BACKEND
  │   │           │       │
  │   │           │       ├─> IntegracionAPIService
  │   │           │       │   ├─> Obtiene credenciales encriptadas
  │   │           │       │   ├─> Desencripta token
  │   │           │       │   └─> Llama RENIEC API
  │   │           │       │       │
  │   │           │       │       └─> Respuesta: {nombre, apellido...}
  │   │           │       │
  │   │           │       └─> Registra consulta en BD
  │   │           │           (auditoria/consultas_externas)
  │   │           │
  │   │           └─> Respuesta al FRONTEND
  │   │               │
  │   │               └─> Auto-llena campos
  │   │                   (nombre, apellido_paterno, etc)
  │   │
  │   └─> Completa campos restantes
  │       │
  │       └─> Haz clic en [✅ Registrarse]
  │           │
  │           ├─> Valida todos los campos
  │           │
  │           ├─> POST /api/usuarios/registro-dinamico
  │           │   │
  │           │   └─> BACKEND
  │           │       │
  │           │       ├─> Obtiene usuario autenticado
  │           │       ├─> Itera campos recibidos
  │           │       ├─> Valida contra configuracion_campos
  │           │       └─> Guarda en campos_usuario (uno por fila)
  │           │
  │           └─> Muestra mensaje de éxito
  │               │
  │               └─> Redirige a dashboard
  │
  └─> Proceso completado ✅
```

---

## 🗄️ Estructura de Base de Datos

```
integraciones_api
├─ id (PK)
├─ nombre (UNIQUE)
├─ descripcion
├─ tipo (ENUM: reniec, facturiza, sunat, custom)
├─ endpoint_url
├─ auth_type (ENUM: bearer, api_key, oauth2, basic)
├─ auth_token (ENCRIPTADO con Fernet)
├─ activa (BOOLEAN)
├─ timeout_segundos (DEFAULT: 30)
├─ max_reintentos (DEFAULT: 3)
├─ created_at
└─ updated_at

configuracion_campos
├─ id (PK)
├─ nombre_campo (UNIQUE)
├─ etiqueta
├─ descripcion
├─ tipo_dato (ENUM: string, number, date, enum, boolean, email, phone, url)
├─ es_obligatorio
├─ expresion_regex
├─ valores_enum (JSON)
├─ posicion
├─ api_integracion_id (FK -> integraciones_api)
├─ campo_mapa_api
├─ mostrar_en_registro
├─ mostrar_en_perfil
├─ mostrar_en_reportes
├─ creado_por (FK -> usuarios)
├─ created_at
└─ updated_at

consultas_externas (AUDITORÍA)
├─ id (PK)
├─ usuario_id (FK -> usuarios)
├─ integracion_api_id (FK -> integraciones_api)
├─ tipo_consulta (ej: "DNI", "RUC")
├─ parametro_busqueda
├─ respuesta_json
├─ campos_mapeados (JSON)
├─ estado (pendiente, exitosa, fallida)
├─ mensaje_error
├─ timestamp
└─ ip_origen

campos_usuario (DATOS DINÁMICOS POR USUARIO)
├─ id (PK)
├─ usuario_id (FK -> usuarios)
├─ configuracion_campo_id (FK -> configuracion_campos)
├─ valor
├─ fue_validado_externamente (BOOLEAN)
├─ consulta_externa_id (FK -> consultas_externas)
├─ created_at
└─ updated_at
```

---

## 🔐 Flujo de Encriptación de Tokens

```
1. ADMIN CREA INTEGRACIÓN CON TOKEN
   │
   └─> IntegracionAPIService.encriptar_token(token)
       │
       ├─> Genera ENCRYPTION_KEY (de .env)
       ├─> Usa Fernet para encriptar
       └─> Retorna token_encriptado

2. GUARDAR EN BD
   │
   └─> BD.integraciones_api.auth_token = token_encriptado

3. USUARIO CONSULTA DNI
   │
   └─> IntegracionAPIService.desencriptar_token(token_encriptado)
       │
       ├─> Obtiene ENCRYPTION_KEY (de .env)
       ├─> Usa Fernet para desencriptar
       └─> Retorna token original
           │
           └─> Usa en llamada a RENIEC
```

---

## 📊 Flujo de Auditoría

```
CADA CONSULTA EXTERNA REGISTRA:

consultas_externas
├─ usuario_id         → Quién hizo la consulta
├─ integracion_api_id → Qué API se usó
├─ tipo_consulta      → Tipo (DNI, RUC, etc)
├─ parametro_busqueda → Qué se consultó (ej: "12345678")
├─ respuesta_json     → Qué datos se obtuvieron
├─ estado             → ¿Exitosa o no?
├─ mensaje_error      → Si falló, cuál fue el error
├─ timestamp          → Cuándo se hizo
└─ ip_origen          → Desde dónde se hizo

ESTADÍSTICAS DISPONIBLES:
├─ Total de consultas
├─ Tasa de éxito (exitosas / total)
├─ APIs más usadas
├─ Usuarios únicos
└─ Rango de fechas
```

---

## 🚀 Performance & Escalabilidad

```
OPTIMIZACIONES IMPLEMENTADAS:
├─ Índices en BD (nombre_campo, usuario_id, integracion_api_id)
├─ Reintentos automáticos (3 intentos)
├─ Timeouts configurables (30s default)
├─ Caché de credenciales desencriptadas (en memoria)
└─ Validación en cliente antes de envío

PROPUESTAS FUTURAS:
├─ Redis para caché de respuestas
├─ Rate limiting por usuario/IP
├─ Queue de consultas (Celery)
├─ CDN para assets estáticos
└─ GraphQL API (alternativa a REST)
```

---

**Creado:** 2026-04-25
