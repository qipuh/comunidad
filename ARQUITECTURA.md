# Especificación Técnica – Sistema de Gestión Comunitaria

## 1. DIAGRAMA DE ENTIDAD-RELACIÓN (DER)

```
┌─────────────────────────┐
│       USUARIO           │
├─────────────────────────┤
│ id (PK)                 │
│ email (UNIQUE)          │
│ nombre                  │
│ telefono                │
│ rol (enum)              │
│ estado (activo/inactivo)│
│ familia_id (FK)         │
│ es_jefe_familia         │
│ direccion               │
│ [CAMPOS ABIERTOS]       │
│ created_at              │
│ updated_at              │
└─────────────────────────┘
         │
         │ (1:N)
         ▼
┌─────────────────────────┐
│      FAMILIA            │
├─────────────────────────┤
│ id (PK)                 │
│ nombre_grupo            │
│ jefe_id (FK → Usuario)  │
│ direccion               │
│ created_at              │
└─────────────────────────┘


┌─────────────────────────┐
│   FOTO_USUARIO          │
├─────────────────────────┤
│ id (PK)                 │
│ usuario_id (FK)         │
│ tipo (frontal/lat_izq..)│
│ embedding (vector)      │
│ url_archivo             │
│ fecha_captura           │
└─────────────────────────┘


┌─────────────────────────┐
│      APORTACION         │
├─────────────────────────┤
│ id (PK)                 │
│ usuario_id (FK)         │
│ tipo (ordinaria/extra)  │
│ monto                   │
│ fecha                   │
│ forma_pago              │
│ comprobante (URL)       │
│ periodo_id (FK)         │
│ created_at              │
└─────────────────────────┘
         │
         │ (N:1)
         ▼
┌─────────────────────────┐
│     PERIODO_APORTE      │
├─────────────────────────┤
│ id (PK)                 │
│ frecuencia (mensual..)  │
│ fecha_inicio            │
│ fecha_fin               │
│ estado                  │
└─────────────────────────┘


┌─────────────────────────┐
│       REUNION           │
├─────────────────────────┤
│ id (PK)                 │
│ titulo                  │
│ fecha                   │
│ hora                    │
│ lugar                   │
│ orden_dia               │
│ quorum_requerido        │
│ estado (programada...)  │
│ created_at              │
└─────────────────────────┘
         │
         │ (1:N)
         ▼
┌─────────────────────────┐
│      ASISTENCIA         │
├─────────────────────────┤
│ id (PK)                 │
│ reunion_id (FK)         │
│ usuario_id (FK)         │
│ presente (bool)         │
│ hora_llegada            │
│ score_facial (0-100)    │
│ validated_at            │
└─────────────────────────┘


┌─────────────────────────┐
│      ELECCION           │
├─────────────────────────┤
│ id (PK)                 │
│ titulo                  │
│ fecha_inicio            │
│ fecha_fin               │
│ estado (abierta/...)    │
│ umbral_facial (0-100)   │
│ tipo_voto (secreto...)  │
│ created_at              │
└─────────────────────────┘
         │
         │ (1:N)
         ▼
┌─────────────────────────┐
│      CANDIDATO          │
├─────────────────────────┤
│ id (PK)                 │
│ eleccion_id (FK)        │
│ nombre                  │
│ descripcion             │
│ votos_recibidos         │
└─────────────────────────┘


┌─────────────────────────┐
│        VOTO             │
├─────────────────────────┤
│ id (PK)                 │
│ eleccion_id (FK)        │
│ candidato_id (FK)       │
│ token_anonimo (UNIQUE)  │
│ score_facial (0-100)    │
│ validated_at            │
│ fingerprint (auditoría) │
└─────────────────────────┘
```

---

## 2. ARQUITECTURA DE CAPAS

```
FRONTEND (Vue.js 3 + Vite)
├── pages/
│   ├── RegistroUsuario.vue
│   ├── Reuniones.vue
│   ├── Aportaciones.vue
│   └── Elecciones.vue
├── components/
│   ├── FaceScanner.vue (captura 3 fotos)
│   ├── FaceValidation.vue (validación en tiempo real)
│   ├── FormUsuario.vue
│   └── TablaAportaciones.vue
├── stores/ (Pinia)
│   ├── usuarioStore.ts
│   ├── aportacionStore.ts
│   └── eleccionStore.ts
└── services/
    └── api.ts (comunicación con backend)

BACKEND (FastAPI + SQLAlchemy)
├── app/
│   ├── main.py
│   ├── models/ (SQLAlchemy)
│   │   ├── usuario.py
│   │   ├── aportacion.py
│   │   ├── reunion.py
│   │   └── eleccion.py
│   ├── schemas/ (Pydantic)
│   │   ├── usuario_schema.py
│   │   └── ...
│   ├── routes/
│   │   ├── usuarios.py
│   │   ├── aportaciones.py
│   │   ├── reuniones.py
│   │   └── elecciones.py
│   ├── services/
│   │   ├── facial_recognition.py
│   │   └── auditoría.py
│   └── db/
│       └── database.py

DB: PostgreSQL (producción) / SQLite (desarrollo)
```

---

## 3. FLUJO DE RECONOCIMIENTO FACIAL

### Almacenamiento de embeddings vs. imágenes crudas

**OPCIÓN RECOMENDADA: Embeddings (Vectores)**

```
1. REGISTRO (Usuario sube 3 fotos)
   ├─ Foto → face_recognition.load_image_from_file()
   ├─ Detectar rostro → detect_faces(image)
   ├─ Generar embedding (vector 128D) → face_encodings(image)
   ├─ Almacenar embedding en DB (columna VECTOR o JSON)
   └─ Almacenar foto en Cloud Storage (S3/Azure Blob) [OPCIONAL, para auditoría]

2. VALIDACIÓN (Escaneo en reunión/elección)
   ├─ Captura viva → MediaPipe / tracking.js
   ├─ Enviar foto → Backend
   ├─ Generar embedding de captura viva
   ├─ Comparar con 3 embeddings almacenados (distance < umbral)
   ├─ Calcular score: (1 - distancia_promedio) * 100
   └─ Si score > umbral → ACCESO PERMITIDO
```

**Ventajas:**
- ✅ Almacenamiento pequeño (vector 128D = ~512 bytes)
- ✅ Comparación rápida (distancia euclidiana)
- ✅ Privacidad: no se almacena foto cruda en BD
- ✅ Escalable (N usuarios, M validaciones)

**Desventajas:**
- ❌ Modelo debe estar actualizado (face_recognition/insightface)

---

## 4. LÓGICA DE COMPARACIÓN FACIAL

```python
# Pseudocódigo

def registrar_usuario_con_fotos(usuario_id, fotos_dict):
    """
    fotos_dict = {
        'frontal': imagen_bytes,
        'lateral_izquierdo': imagen_bytes,
        'lateral_derecho': imagen_bytes
    }
    """
    embeddings = {}
    for tipo, imagen_bytes in fotos_dict.items():
        embedding = generate_embedding(imagen_bytes)
        foto_record = FotoUsuario(
            usuario_id=usuario_id,
            tipo=tipo,
            embedding=embedding.tolist(),  # Guardar como JSON
            url_archivo=upload_to_s3(imagen_bytes)
        )
        db.add(foto_record)
    db.commit()

def validar_asistencia(reunion_id, usuario_id, foto_viva_bytes):
    """
    Captura en vivo vs. almacenadas
    """
    usuario = db.query(Usuario).get(usuario_id)
    fotos_usuario = db.query(FotoUsuario).filter_by(usuario_id=usuario_id).all()
    
    embedding_vivo = generate_embedding(foto_viva_bytes)
    
    distances = []
    for foto in fotos_usuario:
        embedding_almacenado = np.array(foto.embedding)
        dist = euclidean_distance(embedding_vivo, embedding_almacenado)
        distances.append(dist)
    
    promedio_distancia = np.mean(distances)
    score = (1 - promedio_distancia) * 100  # 0-100
    
    umbral = 60  # Configurable
    
    asistencia = Asistencia(
        reunion_id=reunion_id,
        usuario_id=usuario_id,
        presente=(score > umbral),
        score_facial=score,
        validated_at=datetime.now()
    )
    db.add(asistencia)
    db.commit()
    
    return {"validado": score > umbral, "score": score}
```

---

## 5. FLUJOS PRINCIPALES

### Flujo 1: Registro de Usuario + Subida de Fotos
```
Usuario abre app
  ↓
Ingresa datos (nombre, email, teléfono, rol, etc.)
  ↓
Elige si crear familia nueva o unirse a existente
  ↓
Si es jefe: agrega miembros (cónyuge, hijos)
  ↓
Captura 3 fotos (frontal, lat. izq., lat. der.) con cámara
  ↓
Backend: Genera embeddings + almacena
  ↓
Confirmación: Usuario registrado ✓
```

### Flujo 2: Asistencia a Reunión
```
Usuario llega a reunión
  ↓
Abre app → "Marcar asistencia"
  ↓
Cámara captura rostro (1-3 segundos)
  ↓
Backend: Valida contra 3 fotos almacenadas
  ↓
Si score > 60%: "Asistencia registrada ✓"
Si score < 60%: "Por favor intente de nuevo"
```

### Flujo 3: Voto con Validación Facial
```
Usuario entra a proceso electoral
  ↓
Ingresa email + código único
  ↓
Captura foto en vivo
  ↓
Backend: Valida + genera token_anonimo
  ↓
Frontend: Usuario selecciona candidato
  ↓
Voto registrado con token (sin vincular identidad)
  ↓
Auditoría: fingerprint grabado para trazabilidad
```

---

## 6. CONFIGURACIÓN DE FRECUENCIAS DE APORTE

Tabla `PERIODO_APORTE`:

| id | frecuencia | fecha_inicio | fecha_fin | estado |
|----|------------|--------------|-----------|--------|
| 1  | mensual    | 2026-01-01   | 2026-01-31| activo |
| 2  | trimestral | 2026-02-01   | 2026-04-30| activo |
| 3  | anual      | 2026-01-01   | 2026-12-31| activo |

**Cambio sin pérdida de histórico:**
- Los aportes ya registrados permanecen vinculados a su periodo
- Al cambiar frecuencia: crear nuevo `PERIODO_APORTE`
- Reportes filtran por periodo

---

## 7. SEGURIDAD

- **JWT**: Tokens para autenticación
- **CORS**: Configurado para frontend local + producción
- **Rate Limiting**: En endpoints de facial validation (30 req/min por usuario)
- **Auditoría**: Registro de quién votó (fingerprint + timestamp), sin revelar voto
- **Encriptación**: Almacenar embeddings + fotos en cloud encriptadas

---

## 8. CONFIGURACIÓN DINÁMICA (NUEVO MÓDULO)

### Características

Este módulo permite:
- ✅ Crear campos dinámicos **sin migración de BD**
- ✅ Integrar APIs externas (RENIEC, Facturiza, SUNAT, Custom)
- ✅ Auto-llenar datos desde APIs
- ✅ Encriptar credenciales con Fernet
- ✅ Auditar todas las consultas a APIs
- ✅ Admin panel para gestionar configuración

### Tablas Nuevas

```
integraciones_api
├─ id, nombre, tipo (reniec/facturiza/sunat/custom)
├─ endpoint_url, auth_type, auth_token (ENCRIPTADO)
└─ activa, timeout_segundos, max_reintentos

configuracion_campos
├─ id, nombre_campo, etiqueta, tipo_dato
├─ es_obligatorio, expresion_regex, valores_enum
├─ posicion, api_integracion_id, campo_mapa_api
└─ mostrar_en_registro/perfil/reportes

campos_usuario
├─ id, usuario_id, configuracion_campo_id
├─ valor, fue_validado_externamente
└─ consulta_externa_id

consultas_externas (AUDITORÍA)
├─ id, usuario_id, api_integracion_id
├─ tipo_consulta, parametro_busqueda, respuesta_json
├─ estado (exitosa/fallida), mensaje_error
└─ timestamp, ip_origen
```

### Flujo de Auto-llenado

```
Usuario ingresa DNI en formulario
  ↓
Hace clic en botón "🔗 Validar"
  ↓
Frontend: POST /api/validaciones/consultar-dni
  ↓
Backend: Desencripta token de RENIEC
  ↓
Consulta API RENIEC con reintentos
  ↓
Si exitosa: Retorna {nombre, apellido_paterno, apellido_materno, ...}
  ↓
Frontend: Auto-llena campos relacionados
  ↓
Registra en tabla consultas_externas (auditoría)
  ↓
Usuario confirma y envía registro
```

### Seguridad Específica

- **Tokens encriptados**: Fernet (simétrica, no necesita servidor de claves)
- **Auditoría**: Cada consulta registra usuario, IP, timestamp, respuesta
- **Validación**: Admin puede probar conexión antes de usar en producción
- **Rate limiting**: Limitar consultas por usuario para evitar abuso
- **HTTPS obligatorio**: En producción (credenciales en tránsito)

### Documentación

Ver:
- [MODELOS_DATOS.md](MODELOS_DATOS.md) Sección 6
- [ENDPOINTS_EJEMPLOS.md](ENDPOINTS_EJEMPLOS.md) Secciones 7-9
- [COMPONENTES_DINAMICOS.md](COMPONENTES_DINAMICOS.md)
- [README_CONFIGURACION.md](README_CONFIGURACION.md)

