# 🧪 Comandos para Testing - Sistema Dinámico

**Guía completa para probar el sistema de configuración dinámico.**

---

## 🚀 Setup Inicial

### 1. Iniciar Backend (Python/FastAPI)

```bash
# Terminal 1: Backend
cd backend

# Crear virtualenv (primera vez)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
python main.py
# Debería ver: "Uvicorn running on http://127.0.0.1:8000"
```

### 2. Iniciar Frontend (Vue.js)

```bash
# Terminal 2: Frontend
cd frontend

# Instalar dependencias (primera vez)
npm install

# Iniciar dev server
npm run dev
# Debería ver: "http://localhost:5173"
```

---

## 🧪 Testing por Secciones

### SECCIÓN 1: Crear Integración RENIEC

```bash
# 1️⃣ Crear integración RENIEC
curl -X POST "http://localhost:8000/api/admin/integraciones-api" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "RENIEC",
    "descripcion": "Consulta de DNI en Perú",
    "tipo": "reniec",
    "endpoint_url": "https://api.reniec.gob.pe/dni/",
    "auth_type": "bearer",
    "auth_token": "tu_token_reniec_aqui",
    "activa": true,
    "timeout_segundos": 30,
    "max_reintentos": 3
  }'

# Respuesta esperada:
# {
#   "id": 1,
#   "nombre": "RENIEC",
#   "tipo": "reniec",
#   "activa": true,
#   "created_at": "2026-04-25T10:00:00"
# }
```

### SECCIÓN 2: Crear Integración Facturiza

```bash
# 2️⃣ Crear integración Facturiza
curl -X POST "http://localhost:8000/api/admin/integraciones-api" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Facturiza",
    "descripcion": "Consulta de RUC en Perú",
    "tipo": "facturiza",
    "endpoint_url": "https://api.facturiza.com/",
    "auth_type": "api_key",
    "auth_token": "tu_api_key_aqui",
    "activa": true,
    "timeout_segundos": 30,
    "max_reintentos": 3
  }'
```

### SECCIÓN 3: Listar Integraciones

```bash
# 3️⃣ Verificar integraciones creadas
curl -X GET "http://localhost:8000/api/admin/integraciones-api" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Respuesta esperada:
# [
#   { "id": 1, "nombre": "RENIEC", "tipo": "reniec", "activa": true },
#   { "id": 2, "nombre": "Facturiza", "tipo": "facturiza", "activa": true }
# ]
```

### SECCIÓN 4: Probar Integración RENIEC

```bash
# 4️⃣ Probar conexión a RENIEC
curl -X POST "http://localhost:8000/api/admin/integraciones-api/1/probar" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Respuesta exitosa:
# {
#   "disponible": true,
#   "datos": {
#     "nombre": "Juan",
#     "apellido_paterno": "Pérez",
#     "apellido_materno": "García",
#     "fecha_nacimiento": "1990-05-15"
#   }
# }

# Respuesta con error:
# {
#   "disponible": false,
#   "error": "Timeout: No response from RENIEC after 30 seconds"
# }
```

---

## 📋 Testing Campos Dinámicos

### SECCIÓN 5: Crear Campo DNI

```bash
# 5️⃣ Crear campo "documento_identidad"
curl -X POST "http://localhost:8000/api/admin/configuracion/campos" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

# Respuesta:
# {
#   "id": 1,
#   "nombre_campo": "documento_identidad",
#   "etiqueta": "Documento de Identidad",
#   "tipo_dato": "string",
#   "created_at": "2026-04-25T10:05:00"
# }
```

### SECCIÓN 6: Crear Campo Nombre

```bash
# 6️⃣ Crear campo "nombre_completo"
curl -X POST "http://localhost:8000/api/admin/configuracion/campos" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_campo": "nombre_completo",
    "etiqueta": "Nombre Completo",
    "tipo_dato": "string",
    "es_obligatorio": true,
    "posicion": 2,
    "mostrar_en_registro": true,
    "mostrar_en_perfil": true,
    "mostrar_en_reportes": true
  }'
```

### SECCIÓN 7: Crear Campo Teléfono (Enum)

```bash
# 7️⃣ Crear campo con enum (dropdown)
curl -X POST "http://localhost:8000/api/admin/configuracion/campos" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_campo": "estado_civil",
    "etiqueta": "Estado Civil",
    "tipo_dato": "enum",
    "es_obligatorio": false,
    "valores_enum": ["Soltero", "Casado", "Viudo", "Divorciado"],
    "posicion": 3,
    "mostrar_en_registro": true
  }'
```

### SECCIÓN 8: Listar Campos

```bash
# 8️⃣ Verificar campos creados
curl -X GET "http://localhost:8000/api/admin/configuracion/campos" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Respuesta:
# [
#   {
#     "id": 1,
#     "nombre_campo": "documento_identidad",
#     "etiqueta": "Documento de Identidad",
#     "tipo_dato": "string",
#     "es_obligatorio": true,
#     "posicion": 1
#   },
#   { "id": 2, "nombre_campo": "nombre_completo", ... },
#   { "id": 3, "nombre_campo": "estado_civil", ... }
# ]
```

### SECCIÓN 9: Editar Campo

```bash
# 9️⃣ Cambiar posición del campo
curl -X PUT "http://localhost:8000/api/admin/configuracion/campos/1" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "posicion": 5,
    "es_obligatorio": false
  }'
```

### SECCIÓN 10: Eliminar Campo

```bash
# 🔟 Eliminar campo (usar con cuidado)
curl -X DELETE "http://localhost:8000/api/admin/configuracion/campos/1" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Respuesta: 204 No Content
```

---

## 👤 Testing Usuario - Auto-llenado

### SECCIÓN 11: Consultar DNI (Sin token)

```bash
# 1️⃣1️⃣ Usuario ingresa DNI
curl -X POST "http://localhost:8000/api/validaciones/consultar-dni" \
  -H "Content-Type: application/json" \
  -d '{
    "dni": "12345678"
  }'

# Respuesta exitosa:
# {
#   "exitosa": true,
#   "datos": {
#     "nombre": "Juan",
#     "apellido_paterno": "Pérez",
#     "apellido_materno": "García",
#     "genero": "M",
#     "fecha_nacimiento": "1990-05-15",
#     "estado_civil": "Soltero"
#   },
#   "validado_externamente": true,
#   "fuente": "RENIEC"
# }

# Respuesta con error:
# {
#   "exitosa": false,
#   "error": "DNI no válido. Debe contener 8 dígitos.",
#   "validado_externamente": false
# }
```

### SECCIÓN 12: Consultar RUC

```bash
# 1️⃣2️⃣ Usuario ingresa RUC
curl -X POST "http://localhost:8000/api/validaciones/consultar-ruc" \
  -H "Content-Type: application/json" \
  -d '{
    "ruc": "12345678901"
  }'

# Respuesta:
# {
#   "exitosa": true,
#   "datos": {
#     "razon_social": "Empresa XYZ S.A.C.",
#     "representante_legal": "Juan Pérez",
#     "direccion": "Av. Principal 123",
#     "estado_contribuyente": "Habido"
#   },
#   "validado_externamente": true,
#   "fuente": "Facturiza"
# }
```

### SECCIÓN 13: Probar Disponibilidad RENIEC

```bash
# 1️⃣3️⃣ Verificar si RENIEC está up (sin auth)
curl -X GET "http://localhost:8000/api/validaciones/probar-reniec"

# Respuesta:
# {
#   "disponible": true,
#   "timestamp": "2026-04-25T10:15:00",
#   "tiempo_respuesta_ms": 245
# }
```

### SECCIÓN 14: Obtener Historial Usuario

```bash
# 1️⃣4️⃣ Ver historial de consultas (con auth)
curl -X GET "http://localhost:8000/api/validaciones/historial/42" \
  -H "Authorization: Bearer YOUR_USER_TOKEN"

# Respuesta:
# {
#   "usuario_id": 42,
#   "consultas": [
#     {
#       "id": 1,
#       "tipo_consulta": "DNI",
#       "parametro": "12345678",
#       "integracion": "RENIEC",
#       "estado": "exitosa",
#       "fecha": "2026-04-25T10:00:00",
#       "campos_obtenidos": ["nombre", "apellido_paterno"]
#     }
#   ]
# }
```

---

## 📊 Testing Estadísticas

### SECCIÓN 15: Obtener Estadísticas

```bash
# 1️⃣5️⃣ Ver estadísticas de uso
curl -X GET "http://localhost:8000/api/admin/estadisticas/consultas?desde=2026-04-01&hasta=2026-04-25" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Respuesta:
# {
#   "total_consultas": 42,
#   "consultas_exitosas": 38,
#   "consultas_fallidas": 4,
#   "tasa_exito": 90.48,
#   "apis_mas_usadas": {
#     "RENIEC": 25,
#     "Facturiza": 17
#   },
#   "usuarios_unicos": 15,
#   "fecha_inicio": "2026-04-01",
#   "fecha_fin": "2026-04-25"
# }
```

---

## 💾 Testing Registro Completo

### SECCIÓN 16: Guardar Registro Dinámico

```bash
# 1️⃣6️⃣ Usuario completa y envía registro
curl -X POST "http://localhost:8000/api/usuarios/registro-dinamico" \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "documento_identidad": "12345678",
    "nombre_completo": "Juan Pérez García",
    "estado_civil": "Soltero",
    "campos_validados": {
      "documento_identidad": true,
      "nombre_completo": true
    }
  }'

# Respuesta:
# {
#   "usuario_id": 42,
#   "mensaje": "Registro guardado exitosamente",
#   "campos_guardados": 3,
#   "campos_validados_externamente": 2,
#   "timestamp": "2026-04-25T10:20:00"
# }
```

---

## 🔄 Testing Completo (Flujo E2E)

Ejecuta estos comandos en orden para probar el flujo completo:

```bash
# 1. Crear integraciones
curl -X POST "http://localhost:8000/api/admin/integraciones-api" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"RENIEC","tipo":"reniec","endpoint_url":"...","auth_type":"bearer","auth_token":"..."}'

# 2. Crear campos
curl -X POST "http://localhost:8000/api/admin/configuracion/campos" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre_campo":"documento_identidad","etiqueta":"DNI","tipo_dato":"string","api_integracion_id":1,...}'

# 3. Listar campos
curl -X GET "http://localhost:8000/api/admin/configuracion/campos" \
  -H "Authorization: Bearer ADMIN_TOKEN"

# 4. Usuario consulta DNI
curl -X POST "http://localhost:8000/api/validaciones/consultar-dni" \
  -H "Content-Type: application/json" \
  -d '{"dni":"12345678"}'

# 5. Usuario guarda registro
curl -X POST "http://localhost:8000/api/usuarios/registro-dinamico" \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"documento_identidad":"12345678","nombre_completo":"Juan Pérez",...}'

# 6. Ver estadísticas
curl -X GET "http://localhost:8000/api/admin/estadisticas/consultas" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## 🖥️ Testing desde Browser

### Frontend - Rutas de Testing

```
# Admin Panel
http://localhost:5173/admin/campos     # Gestionar campos
http://localhost:5173/admin/apis       # Gestionar APIs

# Usuario
http://localhost:5173/registro         # Formulario dinámico

# Dashboard
http://localhost:5173/dashboard        # Ver datos guardados
```

### Pasos en Browser

1. **Admin crea integración**
   - Navega a `http://localhost:5173/admin/apis`
   - Clic "➕ Nueva Integración"
   - Rellena: RENIEC, bearer, token
   - Clic "Guardar"

2. **Admin crea campo**
   - Navega a `http://localhost:5173/admin/campos`
   - Clic "➕ Nuevo Campo"
   - Rellena: documento_identidad, string, obligatorio
   - Selecciona API: RENIEC
   - Clic "Guardar"

3. **Usuario completa registro**
   - Navega a `http://localhost:5173/registro`
   - Ve campo dinámico "Documento de Identidad"
   - Ingresa: "12345678"
   - Clic "🔗 Validar"
   - Campos se auto-llenan automáticamente
   - Clic "✅ Registrarse"

---

## 🐛 Debugging

### Ver logs del Backend

```bash
# Terminal donde corre FastAPI
# Verás en tiempo real:
# INFO:     127.0.0.1:12345 - "POST /api/admin/integraciones-api HTTP/1.1" 201
# INFO:     Consulta a RENIEC iniciada para DNI: 12345678
# INFO:     Respuesta RENIEC recibida en 245ms
```

### Ver Network en Browser

```
F12 → Network tab
1. Filtrar por "api"
2. Ver cada request/response
3. Ver headers de Authorization
4. Ver payload JSON
```

### Verificar BD

```bash
# Conectarse a PostgreSQL
psql -U usuario -d comunidad_db

# Ver tablas creadas
\dt

# Ver integraciones_api
SELECT * FROM integraciones_api;

# Ver configuracion_campos
SELECT * FROM configuracion_campos;

# Ver consultas_externas (auditoría)
SELECT * FROM consultas_externas;
```

---

## ⚠️ Errores Comunes y Soluciones

### Error: "Unauthorized"
```
❌ Error: 401 Unauthorized
✅ Solución: Usar token válido en Authorization header
   curl ... -H "Authorization: Bearer YOUR_VALID_TOKEN"
```

### Error: "Table does not exist"
```
❌ Error: relation "integraciones_api" does not exist
✅ Solución: Ejecutar migraciones
   alembic upgrade head
```

### Error: "Invalid regex"
```
❌ Error: Invalid regular expression
✅ Solución: Escapar caracteres especiales
   "expresion_regex": "^[0-9]{8}$"  # Correcto
```

### Error: "API Timeout"
```
❌ Error: Timeout: No response from RENIEC after 30 seconds
✅ Solución: 
   - Verificar endpoint_url es correcto
   - Verificar token es válido
   - Aumentar timeout_segundos
```

---

## 📋 Checklist de Testing

- [ ] Backend inicia sin errores
- [ ] Frontend inicia en puerto 5173
- [ ] Crear integración RENIEC ✅
- [ ] Crear integración Facturiza ✅
- [ ] Listar integraciones ✅
- [ ] Probar integración RENIEC ✅
- [ ] Crear campo DNI con API ✅
- [ ] Crear campo Nombre sin API ✅
- [ ] Listar campos ✅
- [ ] Editar campo ✅
- [ ] Consultar DNI desde usuario ✅
- [ ] Auto-llenado funciona ✅
- [ ] Guardar registro completo ✅
- [ ] Ver historial usuario ✅
- [ ] Ver estadísticas ✅
- [ ] Todo en browser funciona ✅

---

**¡Listo para testing!** 🚀

Si encuentras problemas, revisa los logs del backend y el Network tab del browser.
