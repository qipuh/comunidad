# ⚡ Guía Rápida – Módulo de Configuración y APIs

**Implementación paso a paso del sistema de configuración dinámmica e integraciones API.**

---

## 🎯 En 5 Minutos

### Qué Es
```
Sistema que permite:
1. Definir dinámicamente qué campos se usan en registro
2. Conectar con APIs (RENIEC, Facturiza, SUNAT, Custom)
3. Auto-llenar datos desde esas APIs
4. Auditar todas las consultas realizadas
```

### Cómo Funciona
```
ADMIN CONFIGURA
    ↓
Define campo "documento_identidad"
    ├─ Tipo: string
    ├─ Regex: ^[0-9]{8}$
    └─ API: RENIEC
    
USUARIO SE REGISTRA
    ↓
Ingresa DNI: "12345678"
    ↓
Sistema:
  1. Valida formato
  2. Llama a RENIEC
  3. RENIEC retorna: {nombre, apellido, fecha_nacimiento}
  4. Auto-llena campos
    ↓
✓ Registro validado y completado
```

---

## 📋 Implementación Rápida (2 horas)

### Paso 1: Backend (30 min)

```bash
# 1. Crear archivo de modelos
nano backend/app/models/configuracion.py
# Copiar todo de CONFIGURACION_CAMPOS_Y_APIS.md secc. "Código Ejemplo: Backend"

# 2. Crear archivo de servicio
nano backend/app/services/integracion_api_service.py
# Copiar IntegracionAPIService completo

# 3. Crear archivo de endpoints
nano backend/app/routes/validaciones.py
# Copiar endpoints consultar_dni, consultar_ruc

# 4. Actualizar main.py
# Agregar: from app.models.configuracion import *
# Agregar: app.include_router(router_validaciones)

# 5. Crear migraciones
alembic revision --autogenerate -m "Add configuration and API tables"
alembic upgrade head
```

### Paso 2: Frontend (30 min)

```bash
# 1. Componente ConfiguradorCampos
nano frontend/src/components/admin/ConfiguradorCampos.vue
# Copiar de CONFIGURACION_CAMPOS_Y_APIS.md secc. "Componentes Vue.js"

# 2. Componente ConfiguradorAPIs
nano frontend/src/components/admin/ConfiguradorAPIs.vue
# Copiar de CONFIGURACION_AVANZADA_PARTE2.md secc. "ConfiguradorAPIs.vue"

# 3. Página de Registro Dinámico
nano frontend/src/pages/RegistroDinamico.vue
# Copiar de CONFIGURACION_AVANZADA_PARTE2.md secc. "FormularioRegistroDinamico.vue"

# 4. Actualizar router
# Agregar rutas:
#   /admin/configuracion/campos
#   /admin/configuracion/apis
#   /registro-dinamico
```

### Paso 3: Configurar Integraciones (30 min)

```bash
# 1. Acceso Admin → /admin/configuracion/apis

# 2. Agregar integración RENIEC
Nombre: RENIEC
Tipo: reniec
Endpoint: https://api.reniec.gob.pe/dni/
Auth: Bearer
Token: [tu_token_aqui]
Probar: ✅
Guardar

# 3. Agregar integración Facturiza (opcional)
Nombre: Facturiza
Tipo: facturiza
Endpoint: https://api.facturiza.com/consultas/ruc
Auth: API Key
Token: [tu_api_key_aqui]
Probar: ✅
Guardar

# 4. Configurar campos
Admin → /admin/configuracion/campos

Campo 1: documento_identidad
├─ Etiqueta: Documento de Identidad
├─ Tipo: string
├─ Obligatorio: true
├─ Regex: ^[0-9]{8}$
├─ API: RENIEC
├─ Campo en API: dni
└─ Guardar

Campo 2: nombre
├─ Etiqueta: Nombre Completo
├─ Tipo: string
├─ Obligatorio: false (auto-llenado desde RENIEC)
└─ Guardar

(Repetir para más campos)
```

### Paso 4: Probar (30 min)

```bash
# 1. Testear endpoint
curl -X POST http://localhost:8000/api/validaciones/consultar-dni \
  -H "Content-Type: application/json" \
  -d '{"dni": "12345678"}'

# Respuesta esperada:
{
  "exitosa": true,
  "datos": {
    "nombre": "Juan",
    "apellido_paterno": "Pérez",
    "apellido_materno": "García",
    "fecha_nacimiento": "1990-05-15"
  }
}

# 2. Testear formulario
http://localhost:5173/registro-dinamico
├─ Ingresa documento: 12345678
├─ Verifica auto-llenado
└─ Completa fotos

# 3. Revisar auditoría
BD → consultas_externas
├─ Ver registro de consultas
├─ Verificar campos mapeados
└─ Confirmar trazabilidad
```

---

## 🔌 Integraciones en Detalle

### RENIEC (Perú)

```
1. Obtener Token
   └─ https://www.reniec.gob.pe/servicios-en-linea/consultas/

2. Configurar en Admin Panel
   Endpoint: https://api.reniec.gob.pe/dni/
   Auth: Bearer [token]

3. Campos que retorna
   ├─ nombres
   ├─ apellido_paterno
   ├─ apellido_materno
   ├─ genero
   ├─ fecha_nacimiento
   ├─ estado_civil
   └─ fotografia_url (opcional)

4. Mapear en formulario
   documento_identidad → dni
   nombre → nombres
   apellido → apellido_paterno
```

### Facturiza (Latinoamérica)

```
1. Obtener API Key
   └─ https://www.facturiza.com/

2. Configurar en Admin Panel
   Endpoint: https://api.facturiza.com/consultas/ruc
   Auth: API Key [key]

3. Campos que retorna
   ├─ razon_social
   ├─ direccion
   ├─ representante_legal
   ├─ actividad_economica
   ├─ estado_contribuyente
   └─ fecha_inscripcion

4. Mapear en formulario
   ruc → ruc
   razon_social → razon_social
   direccion → direccion
```

### Custom API

```
1. URL configurada por ti
   └─ https://tu-api.com/consulta

2. Método: GET o POST

3. Auth: Bearer, API Key, Basic, OAuth2

4. Mapeo: Definible por administrador
   Campo local → Campo en API

5. Ejemplo
   POST https://mi-api.com/datos
   Header: X-API-Key: xxx
   Body: {"codigo": "123"}
   Response: {"nombre": "Producto", "precio": 100}
```

---

## 🗂️ Estructura de Datos

### Flujo de Datos

```
USUARIO INGRESA DATO
        ↓
VALIDAR REGEX (opcional)
        ↓
¿TIENE API INTEGRADA?
  └─ SÍ: CONSULTAR API
        ├─ RENIEC
        ├─ Facturiza
        ├─ SUNAT
        └─ Custom
  └─ NO: CONTINUAR
        ↓
GUARDAR EN CampoUsuario
        ↓
REGISTRAR CONSULTA EN ConsultaExterna
        ↓
✓ CAMPO PROCESADO
```

### Tablas Involucradas

```
Usuario
  └─ campos_customizados (relación)
  └─ consultas_externas (relación)

ConfiguracionCampo
  ├─ nombre_campo: documento_identidad
  ├─ tipo_dato: string
  ├─ expresion_regex: ^[0-9]{8}$
  ├─ api_integracion_id: 1 (FK)
  └─ campo_mapa_api: dni

IntegracionAPI
  ├─ nombre: RENIEC
  ├─ tipo: reniec
  ├─ endpoint_url: https://...
  ├─ auth_token: (encriptado)
  └─ activa: true

ConsultaExterna
  ├─ usuario_id: 123
  ├─ integracion_api_id: 1
  ├─ parametro_busqueda: 12345678
  ├─ respuesta_json: {...}
  ├─ campos_mapeados: {...}
  ├─ estado: exitosa
  └─ ip_origen: 192.168.1.1

CampoUsuario
  ├─ usuario_id: 123
  ├─ configuracion_campo_id: 1
  ├─ valor: 12345678
  ├─ fue_validado_externamente: true
  └─ consulta_externa_id: 45
```

---

## 🔐 Seguridad

### Encriptación de Tokens

```python
# En backend/app/services/integracion_api_service.py
from cryptography.fernet import Fernet

# Generar key (hacer una sola vez)
key = Fernet.generate_key()
# Guardar en .env como: ENCRYPTION_KEY=key

# Encriptar al guardar
cipher = Fernet(ENCRYPTION_KEY)
token_encriptado = cipher.encrypt(auth_token.encode())

# Desencriptar al usar
token_decriptado = cipher.decrypt(token_encriptado).decode()
```

### Rate Limiting

```python
# En backend/app/routes/validaciones.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/consultar-dni")
@limiter.limit("10/hour")  # 10 consultas por hora por IP
async def consultar_dni(...):
    ...
```

### Auditoría

```sql
-- Ver todas las consultas realizadas
SELECT * FROM consultas_externas
WHERE usuario_id = 123
ORDER BY timestamp DESC;

-- Ver intento de fraude
SELECT usuario_id, COUNT(*) as intentos
FROM consultas_externas
WHERE estado = 'fallida'
  AND timestamp > NOW() - INTERVAL 1 HOUR
GROUP BY usuario_id
HAVING COUNT(*) > 3;
```

---

## 🐛 Troubleshooting

### Problema: "Token inválido en RENIEC"
```
Solución:
1. Verificar token en .env
2. Verificar que no esté expirado
3. Probar token desde postman
4. En admin: Prueba Conexión → Ver error exacto
```

### Problema: "Timeout en consulta"
```
Solución:
1. Aumentar timeout en IntegracionAPI (default 30s)
2. Verificar conexión a internet
3. Revisar status de API externa
4. Habilitar reintentos automáticos (default 3)
```

### Problema: "Datos no se auto-llenan"
```
Solución:
1. Verificar que api_integracion_id no sea NULL en ConfiguracionCampo
2. Verificar que campo_mapa_api coincida con respuesta API
3. Revisar console del navegador para errores
4. Verificar que IntegracionAPI.activa = true
5. Probar endpoint manualmente con curl
```

### Problema: "Consulta guardada con error"
```
Solución:
1. Ver mensaje_error en consultas_externas
2. Verificar respuesta JSON en respuesta_json
3. Revisar logs del backend
4. Comprobar si API está caída (status page)
```

---

## 📞 Ejemplo: Integración RENIEC Completa

### 1. Obtener Token RENIEC
```
Ir a: https://www.reniec.gob.pe/servicios-en-linea/
Solicitar acceso a API
Recibir: token_abc123xyz
```

### 2. Agregar en .env
```
RENIEC_API_TOKEN=token_abc123xyz
```

### 3. Crear integración en Admin
```
POST /api/admin/integraciones-api
{
  "nombre": "RENIEC",
  "tipo": "reniec",
  "endpoint_url": "https://api.reniec.gob.pe/dni/",
  "auth_type": "bearer",
  "auth_token": "token_abc123xyz",
  "timeout_segundos": 30,
  "max_reintentos": 3,
  "activa": true
}
```

### 4. Crear campo en Admin
```
POST /api/admin/configuracion/campos
{
  "nombre_campo": "documento_identidad",
  "etiqueta": "Documento de Identidad",
  "tipo_dato": "string",
  "es_obligatorio": true,
  "expresion_regex": "^[0-9]{8}$",
  "api_integracion_id": 1,
  "campo_mapa_api": "dni",
  "posicion": 1
}
```

### 5. Crear campo "nombre" (auto-llenado)
```
POST /api/admin/configuracion/campos
{
  "nombre_campo": "nombre",
  "etiqueta": "Nombre Completo",
  "tipo_dato": "string",
  "es_obligatorio": false,
  "posicion": 2
}
```

### 6. Usuario se registra
```
Abre: /registro-dinamico
Ingresa: documento_identidad = "12345678"
Sistema:
  1. Valida regex: ✓
  2. POST /validaciones/consultar-dni
  3. RENIEC retorna: {nombres: "Juan Pérez García", ...}
  4. Auto-llena nombre: "Juan Pérez García"
  5. Usuario ve: "✅ Datos auto-llenados desde RENIEC"
  6. Usuario confirma/corrige
  7. Completa fotos
  8. ✓ Registro exitoso
```

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| Documentos nuevos | 3 |
| Líneas de código nuevo | 2,000+ |
| Nuevas tablas | 4 |
| Integraciones soportadas | 4+ (RENIEC, Facturiza, SUNAT, Custom) |
| Tiempo implementación | 2-3 horas |
| Complejidad | Media |

---

## ✅ Checklist

- [ ] Leer CONFIGURACION_CAMPOS_Y_APIS.md
- [ ] Leer CONFIGURACION_AVANZADA_PARTE2.md
- [ ] Implementar modelos (30 min)
- [ ] Implementar servicios (30 min)
- [ ] Implementar endpoints (30 min)
- [ ] Implementar componentes Vue (30 min)
- [ ] Crear migraciones (10 min)
- [ ] Configurar RENIEC (10 min)
- [ ] Probar flujo completo (20 min)
- [ ] Documentar integraciones custom
- [ ] Deploy a producción

---

## 🔗 Links Útiles

- CONFIGURACION_CAMPOS_Y_APIS.md - Especificación completa
- CONFIGURACION_AVANZADA_PARTE2.md - Componentes y casos de uso
- RESUMEN_ACTUALIZACION.md - Cambios y migración
- ENDPOINTS_EJEMPLOS.md - Código original (aún válido)

---

**¡Listo para implementar!** 🚀

