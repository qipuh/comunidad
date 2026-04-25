# ⚡ Quick Reference - Sistema de Configuración Dinámico

## 📁 Archivos Claves

```
backend/app/
├── models/configuracion.py          (Modelos: ConfiguracionCampo, IntegracionAPI, etc.)
├── services/integracion_api_service.py (Lógica de APIs)
└── routes/
    ├── validaciones.py              (Endpoints: /api/validaciones/*)
    ├── admin_configuracion.py       (Endpoints: /api/admin/*)
    └── registro.py                  (TODO: Guardar registros dinámicos)

frontend/src/
├── services/
│   ├── configuracion.service.ts     (CRUD campos/APIs)
│   └── validaciones.service.ts      (Consultar DNI/RUC)
└── components/
    ├── admin/ConfiguradorCampos.vue (Admin: crear/editar campos)
    ├── admin/ConfiguradorAPIs.vue   (Admin: gestionar APIs)
    └── RegistroDinamico.vue         (Usuario: formulario dinámico)
```

---

## 🔗 URLs Principales

| Recurso | Ruta | Método | Auth | Descripción |
|---------|------|--------|------|-------------|
| **Admin - Campos** | `/api/admin/configuracion/campos` | GET/POST/PUT/DELETE | Admin | CRUD campos |
| **Admin - APIs** | `/api/admin/integraciones-api` | GET/POST/PUT/DELETE | Admin | CRUD integraciones |
| **Admin - Probar API** | `/api/admin/integraciones-api/{id}/probar` | POST | Admin | Test conexión |
| **Admin - Stats** | `/api/admin/estadisticas/consultas` | GET | Admin | Estadísticas uso |
| **Usuario - Consultar DNI** | `/api/validaciones/consultar-dni` | POST | - | Validar DNI |
| **Usuario - Consultar RUC** | `/api/validaciones/consultar-ruc` | POST | - | Validar RUC |
| **Usuario - Historial** | `/api/validaciones/historial/{user_id}` | GET | Auth | Historial consultas |
| **Usuario - Probar RENIEC** | `/api/validaciones/probar-reniec` | GET | - | Check RENIEC disponible |
| **Usuario - Registro** | `/api/usuarios/registro-dinamico` | POST | Auth | Guardar registro |

---

## 📝 Tipos de Datos Soportados

```typescript
type TipoDato = 
  | 'string'      // Texto simple
  | 'number'      // Números
  | 'date'        // Fecha (YYYY-MM-DD)
  | 'email'       // Email con validación
  | 'phone'       // Teléfono
  | 'url'         // URL con validación
  | 'enum'        // Opciones múltiples
  | 'boolean'     // Checkbox
```

---

## 🔐 Tipos de Autenticación API

```typescript
type AuthType = 
  | 'bearer'      // Bearer {token}
  | 'api_key'     // X-API-Key: {key}
  | 'oauth2'      // OAuth2 flow
  | 'basic'       // Basic {base64(user:pass)}
```

---

## 🛠️ Funciones Principales

### ConfiguracionService

```typescript
// Campos
await configuracionService.obtenerCampos()
await configuracionService.crearCampo(campo)
await configuracionService.editarCampo(id, campo)
await configuracionService.eliminarCampo(id)

// APIs
await configuracionService.obtenerIntegraciones()
await configuracionService.crearIntegracion(api)
await configuracionService.editarIntegracion(id, api)
await configuracionService.eliminarIntegracion(id)
await configuracionService.probarIntegracion(id)
await configuracionService.obtenerEstadisticas()
```

### ValidacionesService

```typescript
// Consultas
await validacionesService.consultarDNI(dni)
await validacionesService.consultarRUC(ruc)
await validacionesService.obtenerHistorial(usuarioId)

// Pruebas
await validacionesService.probarRENIEC()
await validacionesService.probarFacturiza()

// Utilidades
validacionesService.mapearCampoAPI(campoAPI) // string | null
```

---

## 📊 Estructura de Datos

### ConfiguracionCampo
```typescript
interface ConfiguracionCampo {
  id: number
  nombre_campo: string           // Identificador único (ej: 'dni')
  etiqueta: string               // Texto visible (ej: 'DNI')
  descripcion?: string
  tipo_dato: string              // Uno de los 8 tipos
  es_obligatorio: boolean
  expresion_regex?: string       // Para validación (ej: ^[0-9]{8}$)
  valores_enum?: string[]        // Para tipo 'enum'
  posicion: number               // Orden en el formulario
  api_integracion_id?: number    // Para auto-llenado
  campo_mapa_api?: string        // Campo en respuesta API
  mostrar_en_registro: boolean
  mostrar_en_perfil: boolean
  mostrar_en_reportes: boolean
}
```

### IntegracionAPI
```typescript
interface IntegracionAPI {
  id: number
  nombre: string                 // RENIEC, Facturiza, etc.
  descripcion?: string
  tipo: string                   // 'reniec' | 'facturiza' | 'sunat' | 'custom'
  endpoint_url: string           // URL del endpoint
  auth_type: string              // bearer | api_key | oauth2 | basic
  activa: boolean
  timeout_segundos: number       // Default: 30
  max_reintentos: number         // Default: 3
  created_at: string             // Timestamp
}
```

### ResultadoValidacion
```typescript
interface ResultadoValidacion {
  exitosa: boolean
  datos?: Record<string, any>
  validado_externamente: boolean
  fuente?: string                // RENIEC, Facturiza, etc.
  error?: string
}
```

---

## 🧪 Ejemplos de Uso

### Crear un Campo
```typescript
await configuracionService.crearCampo({
  nombre_campo: 'email',
  etiqueta: 'Correo Electrónico',
  tipo_dato: 'email',
  es_obligatorio: true,
  posicion: 5,
  mostrar_en_registro: true
})
```

### Crear una Integración
```typescript
await configuracionService.crearIntegracion({
  nombre: 'RENIEC',
  tipo: 'reniec',
  endpoint_url: 'https://api.reniec.gob.pe/dni/',
  auth_type: 'bearer',
  auth_token: 'tu_token_aqui',
  activa: true,
  timeout_segundos: 30,
  max_reintentos: 3
})
```

### Consultar DNI
```typescript
const resultado = await validacionesService.consultarDNI('12345678')
if (resultado.exitosa) {
  console.log(resultado.datos) // { nombre, apellido_paterno, ... }
}
```

### Llenar Campo desde API
```typescript
const resultado = await validacionesService.consultarDNI(dni)
if (resultado.exitosa) {
  Object.keys(resultado.datos).forEach(key => {
    const campoLocal = validacionesService.mapearCampoAPI(key)
    if (campoLocal) {
      formData[campoLocal] = resultado.datos[key]
    }
  })
}
```

---

## 🎨 Componentes Vue

### ConfiguradorCampos.vue
- Admin panel para gestionar campos dinámicos
- Drag-and-drop para reordenar
- Modal CRUD con validación visual

**Ruta:** `/admin/campos`

### ConfiguradorAPIs.vue
- Admin panel para gestionar integraciones
- Botón "Probar" para verificar conexión
- Modal con resultado de prueba

**Ruta:** `/admin/apis`

### RegistroDinamico.vue
- Formulario que se adapta a campos configurados
- Botones "Validar" para auto-llenar desde APIs
- Barra de progreso
- Panel informativo

**Ruta:** `/registro`

---

## ⚙️ Pasos de Integración Rápida

```bash
# 1. Ejecutar migraciones
cd backend
alembic upgrade head

# 2. Registrar rutas en main.py
# app.include_router(validaciones_router)
# app.include_router(admin_config_router)

# 3. Configurar rutas en router/index.ts
# import ConfiguradorCampos from '@/components/admin/ConfiguradorCampos.vue'
# routes.push({ path: '/admin/campos', component: ConfiguradorCampos })

# 4. Iniciar servers
npm run dev          # Frontend (puerto 5173)
python main.py       # Backend (puerto 8000)

# 5. Navegar a:
# http://localhost:5173/admin/campos    # Admin
# http://localhost:5173/admin/apis      # Admin
# http://localhost:5173/registro        # Usuario
```

---

## 🔍 Estado del Proyecto

**Completado:** 100% ✅

- [x] Backend: Modelos + Servicios + Endpoints
- [x] Frontend: Servicios + Componentes
- [x] Admin: ConfiguradorCampos + ConfiguradorAPIs
- [x] Usuario: RegistroDinamico
- [x] Integración: RENIEC, Facturiza, SUNAT, Custom
- [x] Encriptación: Tokens protegidos
- [x] Auditoría: Registro de consultas

**Próximo:** Integración en main.py + Testing E2E

---

## 📚 Documentación Completa

- [IMPLEMENTACION_PROGRESS.md](IMPLEMENTACION_PROGRESS.md) - Estado detallado
- [GUIA_INTEGRACION_FINAL.md](GUIA_INTEGRACION_FINAL.md) - Guía paso a paso
- [CONFIGURACION_CAMPOS_Y_APIS.md](CONFIGURACION_CAMPOS_Y_APIS.md) - Especificaciones
- [CONFIGURACION_AVANZADA_PARTE2.md](CONFIGURACION_AVANZADA_PARTE2.md) - Arquitectura

---

**Creado:** 2026-04-25 | **Versión:** 1.0
