# 🚀 Guía de Integración Final - Sistema de Configuración Dinámico

**Estado:** 2026-04-25 | Todos los componentes completados y listos para integrar

---

## 📋 Checklist de Integración

### 1️⃣ Backend - Registrar Rutas (main.py / app.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Comunidad",
    description="Sistema de gestión comunitaria"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Registrar nuevas rutas
from app.routes.validaciones import router as validaciones_router
from app.routes.admin_configuracion import router as admin_config_router

app.include_router(validaciones_router, prefix="/api/validaciones", tags=["Validaciones"])
app.include_router(admin_config_router, prefix="/api/admin", tags=["Admin"])

# ... resto de rutas existentes
```

**Verificar:**
- ✅ Las rutas importan correctamente desde `app.routes`
- ✅ Los prefijos coinciden con los llamados en los servicios frontend
- ✅ Middleware CORS está configurado

---

### 2️⃣ Backend - Ejecutar Migraciones

```bash
cd backend

# Opción A: Si la migración no existe
alembic revision --autogenerate -m "Add configuration tables"

# Opción B: Si ya existe la migración
alembic upgrade head
```

**Verificar:**
```bash
# Ver tablas creadas
psql -U usuario -d comunidad_db -c "\dt"

# Debería mostrar:
# integraciones_api
# configuracion_campos
# consultas_externas
# campos_usuario
```

---

### 3️⃣ Frontend - Rutas Vue Router

Si aún no existen rutas, crearlas en `frontend/src/router/index.ts`:

```typescript
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// Componentes Admin
import ConfiguradorCampos from '@/components/admin/ConfiguradorCampos.vue'
import ConfiguradorAPIs from '@/components/admin/ConfiguradorAPIs.vue'

// Componente de Usuario
import RegistroDinamico from '@/components/RegistroDinamico.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/admin/campos',
    name: 'ConfiguradorCampos',
    component: ConfiguradorCampos,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/apis',
    name: 'ConfiguradorAPIs',
    component: ConfiguradorAPIs,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/registro',
    name: 'RegistroDinamico',
    component: RegistroDinamico,
    meta: { requiresAuth: false }
  },
  // ... otras rutas existentes
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
```

**Verificar:**
- ✅ El router incluye los 3 componentes nuevos
- ✅ Las rutas tienen metas apropiadas (auth, admin)
- ✅ Los imports están correctos

---

### 4️⃣ Crear Endpoint para Guardar Registro Dinámico

Crear `backend/app/routes/registro.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.configuracion import CampoUsuario, ConfiguracionCampo
from app.database import get_db
from app.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/registro-dinamico")
async def guardar_registro_dinamico(
    datos: dict,
    db: Session = Depends(get_db),
    usuario_id: int = Depends(get_current_user)
):
    """Guardar datos de registro dinámico por usuario"""
    try:
        for nombre_campo, valor in datos.items():
            campo = db.query(ConfiguracionCampo).filter_by(
                nombre_campo=nombre_campo
            ).first()
            
            if not campo:
                continue
            
            campo_usuario = CampoUsuario(
                usuario_id=usuario_id,
                configuracion_campo_id=campo.id,
                valor=str(valor) if valor else None,
                fue_validado_externamente=datos.get(f"{nombre_campo}_validado", False)
            )
            db.add(campo_usuario)
        
        db.commit()
        return {"mensaje": "Registro guardado exitosamente"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

Luego registrar en main.py:
```python
from app.routes.registro import router as registro_router
app.include_router(registro_router, prefix="/api/usuarios", tags=["Usuarios"])
```

---

### 5️⃣ Configurar Variables de Entorno

Crear o actualizar `.env` en backend:

```env
# Base de Datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/comunidad_db

# JWT
SECRET_KEY=tu_secreto_super_secreto_aqui

# Encriptación de Tokens API
ENCRYPTION_KEY=tu_encryption_key_aqui

# APIs Externas (ejemplos)
RENIEC_API_TOKEN=token_opcional_aqui
FACTURIZA_API_KEY=api_key_opcional_aqui
SUNAT_API_TOKEN=token_opcional_aqui

# Configuración
LOG_LEVEL=INFO
API_TIMEOUT=30
MAX_RETRIES=3
```

**Generar ENCRYPTION_KEY:**
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())  # Copiar a .env
```

---

### 6️⃣ Completar la Integración Frontend

En el componente `RegistroDinamico.vue`, actualizar el método `enviarFormulario`:

```typescript
const enviarFormulario = async () => {
  if (!validarFormulario()) {
    console.error('Formulario inválido')
    return
  }

  enviando.value = true
  try {
    const response = await api.post('/usuarios/registro-dinamico', formData.value)
    
    if (response.status === 200) {
      mostrarExito.value = true
      setTimeout(() => {
        limpiarFormulario()
        mostrarExito.value = false
        // Redirigir a página de perfil o dashboard
        router.push('/dashboard')
      }, 3000)
    }
  } catch (error) {
    console.error('Error enviando formulario:', error)
    errores.value['general'] = 'Error al guardar el registro'
  } finally {
    enviando.value = false
  }
}
```

---

## 🧪 Testing Manual - Flujo Completo

### Paso 1: Crear Integración RENIEC

```bash
curl -X POST "http://localhost:8000/api/admin/integraciones-api" \
  -H "Authorization: Bearer {ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "RENIEC",
    "tipo": "reniec",
    "endpoint_url": "https://api.reniec.gob.pe/dni/",
    "auth_type": "bearer",
    "auth_token": "your_reniec_token"
  }'
```

Respuesta esperada:
```json
{
  "id": 1,
  "nombre": "RENIEC",
  "tipo": "reniec",
  "activa": true
}
```

### Paso 2: Crear Campo "dni"

```bash
curl -X POST "http://localhost:8000/api/admin/configuracion/campos" \
  -H "Authorization: Bearer {ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_campo": "dni",
    "etiqueta": "DNI",
    "tipo_dato": "string",
    "es_obligatorio": true,
    "expresion_regex": "^[0-9]{8}$",
    "posicion": 1,
    "api_integracion_id": 1,
    "campo_mapa_api": "dni",
    "mostrar_en_registro": true
  }'
```

### Paso 3: Probar API desde Admin Panel

Navega a `/admin/apis` y haz clic en "🧪 Probar" en la integración RENIEC.

Debería mostrar:
```json
{
  "disponible": true,
  "datos": {
    "nombre": "Juan",
    "apellido_paterno": "Pérez",
    "apellido_materno": "García"
  }
}
```

### Paso 4: Llenar Formulario de Registro

Navega a `/registro` y:
1. Ingresa un DNI válido
2. Haz clic en "🔗 Validar"
3. Verifica que se auto-llenen los campos (nombre, apellido_paterno, apellido_materno)
4. Completa cualquier campo faltante
5. Haz clic en "✅ Registrarse"

---

## 📊 Estructura de Respuestas API

### GET /api/admin/configuracion/campos

```json
[
  {
    "id": 1,
    "nombre_campo": "dni",
    "etiqueta": "DNI",
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
]
```

### POST /api/validaciones/consultar-dni

Request:
```json
{
  "dni": "12345678"
}
```

Response:
```json
{
  "exitosa": true,
  "datos": {
    "nombre": "Juan",
    "apellido_paterno": "Pérez",
    "apellido_materno": "García",
    "genero": "M",
    "fecha_nacimiento": "1990-05-15"
  },
  "validado_externamente": true,
  "fuente": "RENIEC"
}
```

### GET /api/admin/estadisticas/consultas

```json
{
  "total_consultas": 42,
  "consultas_exitosas": 38,
  "consultas_fallidas": 4,
  "tasa_exito": 90.5,
  "apis_mas_usadas": {
    "RENIEC": 25,
    "Facturiza": 17
  },
  "usuarios_unicos": 15,
  "fecha_inicio": "2026-04-01",
  "fecha_fin": "2026-04-25"
}
```

---

## 🔒 Consideraciones de Seguridad

- ✅ **Encriptación de Tokens**: Los tokens de APIs se encriptan en DB con Fernet
- ✅ **Validación de Entrada**: Todas las entradas se validan con regex y tipos
- ✅ **Control de Permisos**: Solo admins pueden crear/editar campos y APIs
- ✅ **Auditoría**: Todas las consultas se registran con IP, usuario, timestamp
- ✅ **HTTPS Recomendado**: Para producción, usar HTTPS en todas las APIs
- ⚠️ **Rate Limiting**: TODO - Implementar en mediano plazo
- ⚠️ **CORS**: Configurar dominios específicos en producción

---

## 🐛 Troubleshooting

### "Error: No routes registered"
**Solución:** Verificar que en main.py se incluyen las rutas:
```python
app.include_router(validaciones_router)
app.include_router(admin_config_router)
```

### "Error: Table 'integraciones_api' does not exist"
**Solución:** Ejecutar migraciones:
```bash
alembic upgrade head
```

### "Error: CORS blocked"
**Solución:** Verificar CORS middleware:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### "Error: Encryption key not found"
**Solución:** Generar y configurar en .env:
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
```

---

## 📞 Documentación Relacionada

- [IMPLEMENTACION_PROGRESS.md](IMPLEMENTACION_PROGRESS.md) - Estado general del proyecto
- [CONFIGURACION_CAMPOS_Y_APIS.md](CONFIGURACION_CAMPOS_Y_APIS.md) - Especificaciones técnicas
- [CONFIGURACION_AVANZADA_PARTE2.md](CONFIGURACION_AVANZADA_PARTE2.md) - Arquitectura detallada

---

## ✅ Siguiente Paso Recomendado

1. **Inmediato**: Ejecutar migraciones y registrar rutas
2. **Dentro de 1 hora**: Configurar rutas frontend y variables .env
3. **Dentro de 2 horas**: Realizar prueba E2E completa
4. **Hoy**: Integrar con el módulo de FaceScanner existente

---

**Creado:** 2026-04-25
**Actualizado:** 2026-04-25
**Responsable:** Sistema Comunitario
