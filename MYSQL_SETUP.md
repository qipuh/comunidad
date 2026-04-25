# MySQL Setup - Base de Datos Configurada

**Fecha:** 2026-04-25  
**Status:** ✅ COMPLETADO

---

## 📊 Base de Datos MySQL

| Propiedad | Valor |
|-----------|-------|
| **Nombre** | comunidad |
| **Host** | localhost:3306 |
| **Usuario** | root |
| **Contraseña** | (sin contraseña) |
| **Driver** | pymysql |
| **Estado** | ✅ 5 Tablas creadas |

---

## 📋 Tablas Creadas

```
usuarios                (10 columnas)
configuracion_campos    (17 columnas)
integraciones_api       (12 columnas)
consultas_externas      (11 columnas)
campos_usuario          (8 columnas)
```

**Total:** 5 tablas, 58 columnas

---

## ✅ Verificación

Las tablas se crearon correctamente el **2026-04-25**:

```
OK - campos_usuario                 (8 columnas)
OK - configuracion_campos           (17 columnas)
OK - consultas_externas             (11 columnas)
OK - integraciones_api              (12 columnas)
OK - usuarios                       (10 columnas)
```

---

## 🔧 Configuración del Backend

El archivo `.env` está configurado para MySQL:

```env
DATABASE_URL=mysql+pymysql://root@localhost:3306/comunidad
```

### Dependencias Instaladas
- ✅ `pymysql` - Driver MySQL para Python
- ✅ `sqlalchemy` - ORM
- ✅ `psycopg2-binary` - Para PostgreSQL (opcional)

---

## 🚀 Iniciar Backend

```bash
cd backend
run.bat  # Windows
# o
bash run.sh  # Unix/Mac
```

El backend automáticamente:
1. Conecta a MySQL en `localhost:3306`
2. Usa la base de datos `comunidad`
3. Valida las tablas existentes
4. Inicia el servidor en puerto 8000

---

## 📊 Estructura de Tablas

### usuarios
- id (PK)
- email (UNIQUE)
- username (UNIQUE)
- password_hash
- nombre_completo
- foto_url
- rol (ENUM)
- estado (ENUM)
- created_at
- updated_at

### configuracion_campos
- id (PK)
- nombre_campo (UNIQUE)
- etiqueta
- descripcion
- tipo_dato (ENUM)
- es_obligatorio
- expresion_regex
- valores_enum (JSON)
- posicion
- api_integracion_id (FK)
- campo_mapa_api
- mostrar_en_registro
- mostrar_en_perfil
- mostrar_en_reportes
- creado_por (FK)
- created_at
- updated_at

### integraciones_api
- id (PK)
- nombre (UNIQUE)
- descripcion
- tipo (ENUM: reniec, facturiza, sunat, custom)
- endpoint_url
- auth_type (ENUM: bearer, api_key, oauth2, basic)
- auth_token
- activa
- timeout_segundos
- max_reintentos
- created_at
- updated_at

### consultas_externas
- id (PK)
- usuario_id (FK)
- integracion_api_id (FK)
- tipo_consulta
- parametro_busqueda
- respuesta_json
- campos_mapeados
- estado
- mensaje_error
- timestamp (INDEX)
- ip_origen

### campos_usuario
- id (PK)
- usuario_id (FK, INDEX)
- configuracion_campo_id (FK, INDEX)
- valor
- fue_validado_externamente
- consulta_externa_id (FK)
- created_at
- updated_at

---

## 🔄 Migraciones con Alembic

Las tablas están creadas. Para futuras migraciones:

```bash
# Ver cambios sin aplicar
alembic upgrade head --sql

# Aplicar migraciones
alembic upgrade head

# Ver histórico
alembic history

# Revertir a versión anterior
alembic downgrade -1
```

Ver: [MIGRACIONES_Y_SETUP.md](MIGRACIONES_Y_SETUP.md)

---

## 🧪 Testing

### Verificar conexión
```bash
curl http://localhost:8000/api/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "service": "comunidad-api",
  "timestamp": "2026-04-25T..."
}
```

### Ver datos en MySQL

**Opción 1: Panel Laragon**
1. Abre Laragon
2. Haz clic en "MySQL" → "phpMyAdmin"
3. Navega a base de datos "comunidad"

**Opción 2: Terminal MySQL**
```bash
mysql -h localhost -u root comunidad
SHOW TABLES;
DESCRIBE usuarios;
```

**Opción 3: Python**
```python
python << 'EOF'
from app.db.database import SessionLocal, engine
from app.models.usuario import Usuario
from sqlalchemy import select

db = SessionLocal()
usuarios = db.query(Usuario).all()
print(f"Total usuarios: {len(usuarios)}")
db.close()
EOF
```

---

## 📝 Cambios Recientes

### ✅ Completado Hoy
- Detectado que es MySQL (no PostgreSQL)
- Instalado `pymysql` driver
- Actualizado `.env` con URL de MySQL
- Creadas 5 tablas en `comunidad`
- Verificadas todas las columnas
- Documentación actualizada

### 📋 Próximos Pasos
- [ ] Iniciar backend
- [ ] Verificar salud del API
- [ ] Poblar datos de prueba (opcional)
- [ ] Integrar con frontend

---

## 🐛 Troubleshooting

### "Access denied for user 'root'@'localhost'"
**Causa:** Usuario/contraseña incorrectos  
**Solución:** Verifica en Laragon:
1. Abre phpMyAdmin
2. Verifica usuario actual
3. Actualiza `.env` si es necesario

### "Can't connect to MySQL server on 'localhost'"
**Causa:** MySQL no está corriendo  
**Solución:**
1. Abre Laragon
2. Verifica que MySQL está activado
3. Reinicia MySQL si es necesario

### "Unknown database 'comunidad'"
**Causa:** Base de datos no existe  
**Solución:**
1. Abre phpMyAdmin en Laragon
2. Crea una base de datos llamada `comunidad`
3. Asegúrate que esté vacía
4. Reinicia backend

### Tablas no se crean
**Causa:** Permisos insuficientes  
**Solución:**
1. Verifica que el usuario `root` tiene permisos CREATE
2. Ejecuta: `mysql -u root -e "GRANT ALL ON comunidad.* TO 'root'@'localhost';"`
3. Reinicia backend

---

## 📚 Referencias

- [BACKEND_SETUP.md](BACKEND_SETUP.md) - Setup del backend
- [MIGRACIONES_Y_SETUP.md](MIGRACIONES_Y_SETUP.md) - Gestión de migraciones
- [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md) - Estado del sistema completo

---

## 🎉 Resumen

✅ **MySQL está configurado y listo**

- Base de datos: `comunidad`
- 5 tablas creadas
- 58 columnas totales
- Driver: pymysql
- Backend: listo para iniciar

```bash
cd backend
run.bat  # ¡Inicia aquí!
```

---

*MySQL Setup: 2026-04-25*  
*Status: ✅ COMPLETADO*
