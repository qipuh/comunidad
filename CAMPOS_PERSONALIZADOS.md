# 📝 CAMPOS PERSONALIZADOS – Tu Configuración

Este documento es **tu espacio para definir los campos adicionales** que necesitas en el modelo `Usuario`.

---

## ✅ Cómo Usar Este Documento

1. **Completa la tabla abajo** con los campos que necesitas
2. Copia el nombre exacto de cada campo (será usado en código)
3. Elige el tipo de dato (String, Integer, DateTime, Boolean, etc.)
4. Indica si es obligatorio o no
5. Guarda el archivo

El sistema **generará automáticamente**:
- Los campos en `Usuario` model (SQLAlchemy)
- Los validadores en Pydantic schemas
- Las migraciones de BD (Alembic)
- Los endpoints para GET/PUT

---

## 📋 Define Tus Campos Aquí

| # | Campo | Tipo de Dato | ¿Obligatorio? | Descripción | Observaciones |
|---|-------|-------------|----------------|-------------|-----------------|
| 1 | numero_casa | String(50) | **Sí** | Número de vivienda en la comunidad | Se hereda si es miembro de familia |
| 2 | fecha_ingreso | DateTime | No | Cuándo se unió a la comunidad | Para reportes de antigüedad |
| 3 | documento_identidad | String(50) | Sí | Cédula / DNI / Pasaporte | Validar con regex según país |
| 4 | profesion | String(255) | No | Ocupación del usuario | Para estadísticas comunitarias |
| 5 | telefono_alternativo | String(20) | No | Teléfono secundario | Para contacto de emergencia |
| 6 | es_propietario | Boolean | No | Si es propietario o inquilino | Default: True |
| 7 | | | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |

---

## 📐 Referencia de Tipos de Datos

### Tipos comunes en SQLAlchemy:

```python
# String: Texto corto
String(50)          # Máx 50 caracteres
String(255)         # Máx 255 caracteres

# Integer: Números enteros
Integer             # Rango completo

# Float: Decimales
Float               # 8 bytes

# Boolean: Verdadero/Falso
Boolean             # True/False

# DateTime: Fecha y hora
DateTime            # datetime.now()

# Date: Solo fecha
Date                # date.today()

# Text: Texto largo
Text                # Sin límite de caracteres

# JSON: Datos complejos
JSON                # Objetos/arrays (flexible)

# Enum: Opciones limitadas
Enum(TuEnum)        # Valores predefinidos
```

---

## 🔧 Cómo Implementar Los Campos

### 1️⃣ Actualizar el Modelo

En `backend/app/models/usuario.py`, descomenta o agrega tu lista:

```python
class Usuario(Base):
    # ... campos existentes ...
    
    # ════════════════════════════════════════
    # CAMPOS ABIERTOS PERSONALIZADOS
    # ════════════════════════════════════════
    
    numero_casa = Column(String(50), nullable=False)
    fecha_ingreso = Column(DateTime, nullable=True)
    documento_identidad = Column(String(50), nullable=False, unique=True)
    profesion = Column(String(255), nullable=True)
    telefono_alternativo = Column(String(20), nullable=True)
    es_propietario = Column(Boolean, default=True)
    # Agrega aquí los demás campos de tu tabla...
```

### 2️⃣ Actualizar el Schema Pydantic

En `backend/app/schemas/usuario_schema.py`:

```python
class UsuarioCreate(BaseModel):
    # ... campos existentes ...
    numero_casa: str
    fecha_ingreso: Optional[datetime] = None
    documento_identidad: str
    profesion: Optional[str] = None
    telefono_alternativo: Optional[str] = None
    es_propietario: bool = True

class UsuarioResponse(BaseModel):
    # ... campos existentes ...
    numero_casa: str
    fecha_ingreso: Optional[datetime]
    documento_identidad: str
    profesion: Optional[str]
    telefono_alternativo: Optional[str]
    es_propietario: bool
    
    class Config:
        from_attributes = True
```

### 3️⃣ Crear Migración de BD

```bash
cd backend

# Generar migración automática
alembic revision --autogenerate -m "Add custom user fields"

# Revisar la migración en migrations/versions/
# (opcional: editar si es necesario)

# Aplicar migración
alembic upgrade head
```

### 4️⃣ Actualizar el Endpoint de Registro

En `backend/app/routes/usuarios.py`, agrega los campos al formulario:

```python
@router.post("/registro", response_model=dict)
async def registrar_usuario_con_fotos(
    # ... campos existentes ...
    numero_casa: str = Form(...),
    fecha_ingreso: Optional[str] = Form(None),
    documento_identidad: str = Form(...),
    profesion: Optional[str] = Form(None),
    telefono_alternativo: Optional[str] = Form(None),
    es_propietario: bool = Form(True),
    # ... resto del código ...
):
    usuario = Usuario(
        # ... campos existentes ...
        numero_casa=numero_casa,
        fecha_ingreso=datetime.fromisoformat(fecha_ingreso) if fecha_ingreso else None,
        documento_identidad=documento_identidad,
        profesion=profesion,
        telefono_alternativo=telefono_alternativo,
        es_propietario=es_propietario
    )
    # ... resto del código ...
```

### 5️⃣ Actualizar Frontend (Vue.js)

En `frontend/src/pages/RegistroUsuario.vue`:

```vue
<template>
  <form @submit.prevent="registrar">
    <!-- ... campos existentes ... -->
    
    <!-- CAMPOS PERSONALIZADOS -->
    <div class="form-group">
      <label>Número de Casa *</label>
      <input v-model="form.numero_casa" type="text" required />
    </div>
    
    <div class="form-group">
      <label>Documento de Identidad *</label>
      <input v-model="form.documento_identidad" type="text" required />
    </div>
    
    <div class="form-group">
      <label>Profesión</label>
      <input v-model="form.profesion" type="text" />
    </div>
    
    <div class="form-group">
      <label>Teléfono Alternativo</label>
      <input v-model="form.telefono_alternativo" type="tel" />
    </div>
    
    <div class="form-group">
      <label>
        <input v-model="form.es_propietario" type="checkbox" />
        Soy propietario (no inquilino)
      </label>
    </div>
    
    <!-- ... resto del formulario ... -->
  </form>
</template>

<script setup lang="ts">
const form = ref({
  nombre: '',
  email: '',
  telefono: '',
  numero_casa: '',
  documento_identidad: '',
  profesion: '',
  telefono_alternativo: '',
  es_propietario: true,
  // ... otros campos ...
})
</script>
```

---

## 🎯 Validaciones Recomendadas

### Backend (Pydantic)

```python
from pydantic import BaseModel, field_validator

class UsuarioCreate(BaseModel):
    numero_casa: str
    documento_identidad: str
    
    @field_validator('numero_casa')
    @classmethod
    def validar_numero_casa(cls, v):
        if not v.strip():
            raise ValueError('Número de casa no puede estar vacío')
        if len(v) > 50:
            raise ValueError('Número de casa muy largo')
        return v.upper()
    
    @field_validator('documento_identidad')
    @classmethod
    def validar_documento(cls, v):
        # Ejemplo para cédula numérica
        if not v.replace('-', '').isdigit():
            raise ValueError('Documento debe ser numérico')
        return v
```

### Frontend (Vue.js)

```typescript
const validarNumroCasa = (valor: string) => {
  if (!valor) return 'Número de casa es requerido'
  if (valor.length > 50) return 'Máximo 50 caracteres'
  return ''
}

const validarDocumento = (valor: string) => {
  if (!valor) return 'Documento es requerido'
  if (!/^\d{5,15}$/.test(valor.replace('-', ''))) {
    return 'Formato de documento inválido'
  }
  return ''
}
```

---

## 📊 Reportes con Campos Personalizados

Una vez definidos, puedes crear reportes aprovechando estos campos:

```python
# backend/app/routes/reportes.py

@router.get("/reportes/usuarios-por-profesion")
def usuarios_por_profesion(db: Session = Depends(get_db)):
    """Estadísticas de profesiones en la comunidad"""
    resultado = db.query(
        Usuario.profesion,
        func.count(Usuario.id).label('cantidad')
    ).group_by(Usuario.profesion).all()
    
    return {
        "profesiones": [
            {"profesion": r[0], "cantidad": r[1]}
            for r in resultado
        ]
    }

@router.get("/reportes/nuevos-miembros")
def nuevos_miembros(dias: int = 30, db: Session = Depends(get_db)):
    """Usuarios que se unieron en los últimos N días"""
    desde = datetime.utcnow() - timedelta(days=dias)
    usuarios = db.query(Usuario).filter(Usuario.fecha_ingreso >= desde).all()
    
    return {
        "periodo_dias": dias,
        "nuevos_miembros": len(usuarios),
        "usuarios": [
            {
                "nombre": u.nombre,
                "fecha_ingreso": u.fecha_ingreso.isoformat(),
                "numero_casa": u.numero_casa
            }
            for u in usuarios
        ]
    }
```

---

## 🚀 Checklist de Implementación

- [ ] Completé la tabla de campos (arriba)
- [ ] Actualicé `Usuario` model en SQLAlchemy
- [ ] Actualicé los schemas Pydantic
- [ ] Creé y apliqué la migración Alembic
- [ ] Actualicé los endpoints `/usuarios/registro` y `/usuarios/{id}`
- [ ] Actualicé el formulario en Frontend
- [ ] Probé el registro de usuario con nuevos campos
- [ ] Creé reportes que usan los nuevos campos (opcional)
- [ ] Documenté validaciones especiales (si las hay)

---

## 💡 Ejemplos Prácticos

### Caso: Comunidad de apartamentos

```markdown
| # | Campo | Tipo | Obligatorio | Descripción |
|---|-------|------|-------------|-------------|
| 1 | numero_apartamento | String(10) | Sí | Apto 401, 301B, etc. |
| 2 | piso | Integer | Sí | Piso donde vive |
| 3 | bloque | String(5) | Sí | Bloque A, B, C, etc. |
| 4 | numero_parqueadero | String(10) | No | Garaje asignado |
| 5 | mascotas | Boolean | No | Tiene mascotas |
```

### Caso: Comunidad de casas

```markdown
| # | Campo | Tipo | Obligatorio | Descripción |
|---|-------|------|-------------|-------------|
| 1 | numero_casa | String(50) | Sí | Calle y número |
| 2 | area_lote | Float | No | Área del lote en m² |
| 3 | material_construccion | String(50) | No | Ladrillo, concreto, etc. |
| 4 | tiene_jardin | Boolean | No | Si tiene área verde |
```

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo agregar campos después de lanzar el sistema?**
R: Sí. Usa Alembic para crear nuevas migraciones sin perder datos.

**P: ¿Puedo hacer un campo único (como el documento)?**
R: Sí, en SQLAlchemy: `unique=True`
```python
documento_identidad = Column(String(50), unique=True, nullable=False)
```

**P: ¿Y si necesito un dropdown (enum)?**
R: Crea un Enum y úsalo:
```python
class TipoViviendaEnum(str, enum.Enum):
    CASA = "casa"
    APARTAMENTO = "apartamento"
    OTRO = "otro"

tipo_vivienda = Column(Enum(TipoViviendaEnum), nullable=False)
```

**P: ¿Puedo heredar campos de familia?**
R: En la lógica de negocio (service), copia campos del jefe de familia:
```python
def crear_miembro_familia(usuario_jefe: Usuario) -> dict:
    return {
        "numero_casa": usuario_jefe.numero_casa,
        "direccion": usuario_jefe.direccion,
        # Pero documento_identidad es único, no se hereda
    }
```

---

---

## 🎯 OPCIÓN 2: CONFIGURACIÓN DINÁMICA (RECOMENDADO)

**Novedad:** Ahora puedes configurar campos **SIN migrar la base de datos**.

### ✨ Ventajas de Configuración Dinámica

| Aspecto | Tradicional | Dinámico |
|--------|-----------|----------|
| **Crear campo** | Migración Alembic | Admin panel UI |
| **Modificar campo** | Migración Alembic | Admin panel UI |
| **Validar DNI/RUC** | Manual con código | Auto-llenar desde API |
| **Integración APIs** | Código backend | Configure en admin |
| **Auditoría** | Manual | Automática |

### 🚀 Cómo Usar Configuración Dinámica

**Paso 1: Admin crea una integración RENIEC**
```bash
POST /api/admin/integraciones-api
{
  "nombre": "RENIEC",
  "tipo": "reniec",
  "endpoint_url": "https://api.reniec.gob.pe/dni/",
  "auth_type": "bearer",
  "auth_token": "your_token_here"
}
```

**Paso 2: Admin define campo "documento_identidad"**
```bash
POST /api/admin/configuracion/campos
{
  "nombre_campo": "documento_identidad",
  "etiqueta": "Documento de Identidad",
  "tipo_dato": "string",
  "es_obligatorio": true,
  "expresion_regex": "^[0-9]{8}$",
  "api_integracion_id": 1,
  "campo_mapa_api": "dni",
  "mostrar_en_registro": true
}
```

**Paso 3: Usuario completa el registro**
- Ingresa: "12345678"
- Hace clic en "🔗 Validar"
- Sistema consulta RENIEC automáticamente
- Se auto-llenan: nombre, apellido_paterno, apellido_materno
- Usuario confirma y envía

### 📋 Campos Dinámicos Disponibles

```python
# Tipo de Dato | Descripción | Ejemplo
"string"       # Texto libre | "Juan"
"number"       # Números | 42
"date"         # Fecha | "1990-05-15"
"email"        # Email validado | "user@example.com"
"phone"        # Teléfono | "+51987654321"
"url"          # URL validada | "https://..."
"enum"         # Opciones | ["Soltero", "Casado"]
"boolean"      # Checkbox | True/False
```

### 🔌 APIs Integradas

```python
# Tipo | País | Consulta | Ejemplo
"reniec"    # Perú | DNI | "12345678"
"facturiza" # Perú | RUC | "12345678901"
"sunat"     # Perú | Contribuyente | "12345678901"
"custom"    # Custom | Personalizado | Tu API
```

### 📊 Comparativa: Tradicional vs Dinámico

**TRADICIONAL (Tabla relacional):**
```python
# En MODELOS_DATOS.md, Sección 1
class Usuario(Base):
    numero_casa = Column(String(50))
    fecha_ingreso = Column(DateTime)
    documento_identidad = Column(String(50))
    # ... 10 campos más = cambio de BD
```

**DINÁMICO (Sin cambios en BD):**
```python
# En Admin UI (/admin/campos):
# 1. Crea 10 campos
# 2. Asocia APIs
# 3. Usuarios ven formulario dinámico
# 4. Datos se guardan en CampoUsuario table
```

### 🎯 Ventaja Principal

Con **Configuración Dinámica**:
- ✅ Cambia campos sin parar el sistema
- ✅ Auto-rellena datos desde RENIEC/Facturiza
- ✅ Auditoría automática de consultas
- ✅ Versión segura (tokens encriptados)
- ✅ Escalable (agrega nuevas APIs sin código)

---

## 📞 Soporte

Si tienes dudas al implementar:
1. Revisa [ARQUITECTURA.md](ARQUITECTURA.md)
2. Revisa [MODELOS_DATOS.md](MODELOS_DATOS.md) - **Sección 6 (Nuevo)**
3. Revisa [ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md)
4. Lee [README_CONFIGURACION.md](README_CONFIGURACION.md) para el nuevo módulo

