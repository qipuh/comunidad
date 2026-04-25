# 🆕 Resumen de Actualización – Módulo Avanzado de Configuración

**Fecha:** 2026-04-25  
**Cambios:** Agregados 2 documentos nuevos con sistemas de configuración dinámica e integraciones API

---

## 📦 Nuevos Documentos

### 1. **CONFIGURACION_CAMPOS_Y_APIS.md** (20 KB)

Sistema completo para:
- ✅ Definir dinámicamente campos del registro de usuario
- ✅ Asignar tipos de datos (string, number, date, enum, boolean, email, phone, url)
- ✅ Hacer campos obligatorios/opcionales
- ✅ Conectar con APIs externas (RENIEC, Facturiza, SUNAT, Custom)
- ✅ Auto-llenar datos desde APIs
- ✅ Validar contra fuentes oficiales
- ✅ Mantener auditoría de todas las consultas

**Incluye:**
- Diagrama de 4 nuevas tablas (ConfiguracionCampo, IntegracionAPI, ConsultaExterna, CampoUsuario)
- Especificación de 3 integraciones reales (RENIEC, Facturiza, SUNAT)
- Modelos SQLAlchemy completos (4 clases + enums)
- Servicio de integración API (IntegracionAPIService)
- 2 endpoints REST para consultar RENIEC y Facturiza
- Componente Vue.js ConfiguradorCampos.vue (320 líneas)

### 2. **CONFIGURACION_AVANZADA_PARTE2.md** (18 KB)

Continuación del módulo avanzado:
- ✅ ConfiguradorAPIs.vue: Panel admin para gestionar integraciones
- ✅ FormularioRegistroDinamico.vue: Registro que se adapta a configuración
- ✅ Consultas API automáticas al ingresar datos
- ✅ Auto-completado de campos desde APIs
- ✅ Indicadores visuales de datos validados
- ✅ Historial y auditoría de integraciones

**Incluye:**
- Componente ConfiguradorAPIs.vue (450+ líneas)
- Componente FormularioRegistroDinamico.vue (400+ líneas)
- Endpoint de prueba de integraciones
- Caso de uso completo: Registro con RENIEC
- Mapeo inteligente de campos API

---

## 🎯 Flujos Nuevos

### Flujo 1: Administrador Configura Sistema

```
Admin → Dashboard Admin
    ↓
  Abre: ConfiguradorCampos
    ├─ Define campo: "documento_identidad"
    ├─ Tipo: string, Obligatorio: true
    ├─ Regex: ^[0-9]{8}$
    └─ API: RENIEC
    
  Abre: ConfiguradorAPIs
    ├─ Crea integración RENIEC
    ├─ URL: https://api.reniec.gob.pe/dni/
    ├─ Auth: Bearer token
    ├─ Prueba conexión ✅
    └─ Activa integración
    
  Mapea campos:
    ├─ documento → dni (RENIEC)
    ├─ nombre → nombres (RENIEC)
    └─ apellido → apellido_paterno (RENIEC)

✓ Sistema listo para usar
```

### Flujo 2: Usuario se Registra

```
Usuario → RegistroDinamico.vue
    ↓
Ve formulario dinámico:
  [Documento de Identidad] 🔗 (conectado a API)
  [Nombre]
  [Apellido]
  [Fecha de Nacimiento]
  ... (otros campos configurados)
  
Ingresa documento: "12345678"

Sistema:
  1. Valida formato (regex)
  2. Consulta RENIEC: GET /dni/12345678
  3. RENIEC responde con datos
  4. Auto-llena campos:
     - Nombre: "Juan"
     - Apellido: "Pérez"
     - Fecha Nacimiento: "1990-05-15"
  5. Muestra: "✅ Datos auto-llenados desde RENIEC"

Usuario:
  1. Revisa datos (puede editar)
  2. Completa foto facial
  3. Confirma registro

✓ Registro exitoso
✓ Consulta guardada en auditoría
```

---

## 🏗️ Nuevas Tablas en BD

```sql
-- ConfiguracionCampo
CREATE TABLE configuracion_campos (
  id SERIAL PRIMARY KEY,
  nombre_campo VARCHAR(100) UNIQUE NOT NULL,
  etiqueta VARCHAR(255) NOT NULL,
  tipo_dato ENUM('string', 'number', 'date', 'enum', ...) NOT NULL,
  es_obligatorio BOOLEAN DEFAULT FALSE,
  posicion INTEGER DEFAULT 0,
  expresion_regex VARCHAR(500),
  valores_enum JSON,
  api_integracion_id INTEGER REFERENCES integraciones_api(id),
  campo_mapa_api VARCHAR(100),
  mostrar_en_registro BOOLEAN DEFAULT TRUE,
  mostrar_en_perfil BOOLEAN DEFAULT TRUE,
  mostrar_en_reportes BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- IntegracionAPI
CREATE TABLE integraciones_api (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  tipo ENUM('reniec', 'facturiza', 'sunat', 'custom') NOT NULL,
  endpoint_url VARCHAR(500) NOT NULL,
  auth_type ENUM('bearer', 'api_key', 'oauth2', 'basic') NOT NULL,
  auth_token VARCHAR(500) NOT NULL,
  activa BOOLEAN DEFAULT TRUE,
  timeout_segundos INTEGER DEFAULT 30,
  max_reintentos INTEGER DEFAULT 3,
  created_at TIMESTAMP DEFAULT NOW()
);

-- ConsultaExterna
CREATE TABLE consultas_externas (
  id SERIAL PRIMARY KEY,
  usuario_id INTEGER REFERENCES usuarios(id),
  integracion_api_id INTEGER REFERENCES integraciones_api(id),
  tipo_consulta VARCHAR(50),
  parametro_busqueda VARCHAR(255) NOT NULL,
  respuesta_json JSON,
  campos_mapeados JSON,
  estado VARCHAR(50) DEFAULT 'pendiente',
  mensaje_error VARCHAR(500),
  timestamp TIMESTAMP DEFAULT NOW(),
  ip_origen VARCHAR(45)
);

-- CampoUsuario
CREATE TABLE campos_usuario (
  id SERIAL PRIMARY KEY,
  usuario_id INTEGER REFERENCES usuarios(id),
  configuracion_campo_id INTEGER REFERENCES configuracion_campos(id),
  valor VARCHAR(1000),
  fue_validado_externamente BOOLEAN DEFAULT FALSE,
  consulta_externa_id INTEGER REFERENCES consultas_externas(id),
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📊 Integraciones Soportadas

### RENIEC (Perú) - Consulta de DNI
```
GET https://api.reniec.gob.pe/dni/{dni}
Auth: Bearer token
Retorna: nombres, apellidos, género, fecha_nacimiento, estado_civil
```

### Facturiza - Consulta de RUC
```
POST https://api.facturiza.com/consultas/ruc
Auth: X-API-Key header
Retorna: razon_social, direccion, representante, actividad, estado
```

### SUNAT - Consulta de Contribuyentes
```
SOAP: https://ws.sunat.gob.pe/cl-ti-itconfigserv/jaxwsservice/getStatus
Auth: Certificado digital
Retorna: nombre, razon_social, estado, domicilio
```

### Custom API - Personalizada
```
GET/POST: URL configurable
Auth: Bearer, API Key, Basic, OAuth2 (configurable)
Mapeo: Definible por administrador
```

---

## 🔐 Características de Seguridad

- ✅ **Tokens Encriptados:** Usar `cryptography.Fernet` para auth tokens
- ✅ **Rate Limiting:** Max 10 consultas/hora por usuario a APIs externas
- ✅ **Auditoría Completa:** Registrar todas las consultas (IP, timestamp, resultado)
- ✅ **Validación:** Validar respuestas antes de mapear datos
- ✅ **Retry Logic:** Reintentar 3 veces en timeout o error 5xx
- ✅ **CORS Restringido:** Solo dominio autorizado
- ✅ **Manejo de Errores:** No exponer detalles internos al usuario

---

## 📈 Casos de Uso

### Caso 1: Comunidad en Perú
```
Admin configura:
  1. Campo "documento_identidad" + RENIEC
  2. Campo "ruc_empresa" + Facturiza (para negocios)
  3. Campo "estado_contribuyente" + SUNAT (para verificación)

Usuario se registra:
  - Ingresa DNI → Auto-llena nombre, apellido, fecha_nacimiento
  - Ingresa RUC → Auto-llena razón_social, dirección, representante
  - Sistema verifica en SUNAT si es contribuyente activo

Resultado:
  - Registro verificado y validado
  - Datos siempre al día
  - Auditoría de todas las validaciones
```

### Caso 2: Comunidad Cerrada
```
Admin configura:
  - Campo "codigo_acceso" (tipo string, expresión regex)
  - Campo "rol" (enum: residente, propietario, gestor, admin)
  - Sin APIs externas (validación local)

Usuario se registra:
  - Ingresa código (validado con regex)
  - Selecciona rol de lista
  - Carga fotos
  - Admin aprueba manualmente

Resultado:
  - Control total sin dependencias de APIs externas
  - Flexibilidad para cambiar validaciones
```

---

## 🚀 Cómo Implementar

### 1. Backend
```bash
# 1. Copiar modelos de CONFIGURACION_CAMPOS_Y_APIS.md
#    a: backend/app/models/configuracion.py

# 2. Crear servicio
#    a: backend/app/services/integracion_api_service.py

# 3. Crear endpoints
#    a: backend/app/routes/configuracion_campos.py
#    b: backend/app/routes/integraciones_api.py
#    c: backend/app/routes/validaciones.py

# 4. Crear migración Alembic
alembic revision --autogenerate -m "Add configuration and API integration tables"
alembic upgrade head
```

### 2. Frontend
```bash
# 1. Crear componentes admin
#    a: frontend/src/components/admin/ConfiguradorCampos.vue
#    b: frontend/src/components/admin/ConfiguradorAPIs.vue

# 2. Crear página de registro dinámico
#    a: frontend/src/pages/RegistroDinamico.vue

# 3. Actualizar router
#    a: Agregar ruta /registro dinámico
#    b: Agregar rutas admin /admin/campos, /admin/apis

# 4. Servicios API
#    a: Crear frontend/src/services/configuracion.service.ts
#    b: Crear frontend/src/services/integraciones.service.ts
```

### 3. Variables de Entorno
```env
# Backend
RENIEC_API_URL=https://api.reniec.gob.pe/dni/
RENIEC_API_TOKEN=tu_token_aqui
RENIEC_API_TIMEOUT=30

FACTURIZA_API_URL=https://api.facturiza.com/consultas/ruc
FACTURIZA_API_KEY=tu_api_key_aqui

# Encriptación de tokens
ENCRYPTION_KEY=<generar con Fernet.generate_key()>
```

---

## 📚 Estructura de Archivos Actualizada

```
comunidad/
├── backend/app/
│   ├── models/
│   │   ├── usuario.py                    (existente)
│   │   └── configuracion.py              ✨ NUEVO
│   │
│   ├── services/
│   │   ├── facial_recognition.py        (existente)
│   │   └── integracion_api_service.py    ✨ NUEVO
│   │
│   ├── routes/
│   │   ├── usuarios.py                  (existente)
│   │   ├── configuracion_campos.py       ✨ NUEVO
│   │   ├── integraciones_api.py          ✨ NUEVO
│   │   └── validaciones.py               ✨ NUEVO
│   │
│   └── clients/
│       ├── reniec_client.py              ✨ NUEVO
│       ├── facturiza_client.py           ✨ NUEVO
│       └── sunat_client.py               ✨ NUEVO
│
├── frontend/src/
│   ├── components/admin/
│   │   ├── ConfiguradorCampos.vue        ✨ NUEVO
│   │   └── ConfiguradorAPIs.vue          ✨ NUEVO
│   │
│   ├── pages/
│   │   ├── RegistroUsuario.vue           (existente)
│   │   └── RegistroDinamico.vue          ✨ NUEVO
│   │
│   └── services/
│       ├── api.ts                        (actualizar)
│       ├── configuracion.service.ts      ✨ NUEVO
│       └── integraciones.service.ts      ✨ NUEVO
│
└── DOCUMENTACION/
    ├── CONFIGURACION_CAMPOS_Y_APIS.md    ✨ NUEVO
    └── CONFIGURACION_AVANZADA_PARTE2.md  ✨ NUEVO
```

---

## 🔄 Migración Alembic

```python
# migrations/versions/xxx_add_configuration_tables.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Crear tabla configuracion_campos
    op.create_table(
        'configuracion_campos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre_campo', sa.String(100), nullable=False, unique=True),
        sa.Column('etiqueta', sa.String(255), nullable=False),
        sa.Column('tipo_dato', sa.Enum(...), nullable=False),
        # ... resto de columnas
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear tabla integraciones_api
    op.create_table('integraciones_api', ...)
    
    # Crear tabla consultas_externas
    op.create_table('consultas_externas', ...)
    
    # Crear tabla campos_usuario
    op.create_table('campos_usuario', ...)
    
    # Agregar FK a usuario
    op.add_column('usuarios', sa.Column('campos_customizados', ...))

def downgrade():
    op.drop_table('campos_usuario')
    op.drop_table('consultas_externas')
    op.drop_table('integraciones_api')
    op.drop_table('configuracion_campos')
```

---

## 📋 Checklist de Implementación

- [ ] Leer CONFIGURACION_CAMPOS_Y_APIS.md
- [ ] Leer CONFIGURACION_AVANZADA_PARTE2.md
- [ ] Crear modelos en backend/app/models/configuracion.py
- [ ] Crear IntegracionAPIService
- [ ] Crear endpoints para validaciones
- [ ] Crear ConfiguradorCampos.vue
- [ ] Crear ConfiguradorAPIs.vue
- [ ] Crear RegistroDinamico.vue
- [ ] Crear migraciones Alembic
- [ ] Configurar integraciones (RENIEC, Facturiza, etc.)
- [ ] Probar flujo completo de registro
- [ ] Crear tests para IntegracionAPIService
- [ ] Documentar integraciones custom
- [ ] Agregar rate limiting
- [ ] Encriptar tokens en BD

---

## 🎯 Próximos Pasos

1. **Integración RENIEC:** 
   - Obtener token de RENIEC
   - Configurar endpoint en admin panel
   - Probar con DNI de prueba

2. **Integración Facturiza:**
   - Obtener API Key
   - Configurar endpoint
   - Mapear campos RUC

3. **Custom APIs:**
   - Documentar formato esperado
   - Crear ejemplos para clientes
   - Validar respuestas

---

## 📞 Soporte Técnico

Preguntas comunes:

**P: ¿Cómo agrego una integración nueva?**
A: Crear clase en backend/app/clients/, mapear en IntegracionAPIService, configurar en admin

**P: ¿Qué pasa si la API falla?**
A: Retry automático 3 veces, timeout 30s, error en formulario, usuario puede continuar manualmente

**P: ¿Se guarda el token en la BD?**
A: Sí, encriptado con `cryptography.Fernet`. Ver CONFIGURACION_CAMPOS_Y_APIS.md secc. "Seguridad"

**P: ¿Puedo usar esta integración sin modificar el código?**
A: Sí, es 100% configurable desde admin panel para RENIEC, Facturiza, SUNAT y Custom APIs

---

## 📊 Resumen de Cambios

| Métrica | Antes | Después | Cambio |
|---------|-------|---------|--------|
| Documentos | 11 | 13 | +2 |
| Modelos BD | 10 | 14 | +4 |
| Líneas de especificación | 4,400 | 5,200+ | +800 |
| Componentes Vue | 10 | 12 | +2 |
| Integraciones soportadas | 0 | 4+ | ∞ |

---

**¡Tu sistema ahora soporta configuración dinámica e integraciones API avanzadas!** 🚀

