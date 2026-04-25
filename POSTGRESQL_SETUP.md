# Configuración PostgreSQL

**Base de datos:** comunidad  
**Usuarios:** root (sin contraseña)  
**Host:** localhost  
**Puerto:** 5432

---

## ⚠️ Estado Actual

Actualmente el backend está configurado con **SQLite** para máxima compatibilidad.

✅ **SQLite** - Funciona sin dependencias adicionales  
⏳ **PostgreSQL** - Requiere que el servidor esté corriendo en Laragon

---

## 🔄 Cambiar a PostgreSQL

### Paso 1: Iniciar PostgreSQL en Laragon

Abre **Laragon** y asegúrate de que PostgreSQL está **activado y corriendo**:

1. Abre Laragon
2. Ve a **Services** o **Servicios**
3. Verifica que **PostgreSQL** está **activado** (checkbox marcado)
4. El servidor debe estar **running**

### Paso 2: Actualizar .env

Edita `backend/.env`:

```bash
# ANTES (SQLite - actual):
DATABASE_URL=sqlite:///./comunidad.db

# DESPUÉS (PostgreSQL):
DATABASE_URL=postgresql://root@localhost:5432/comunidad
```

### Paso 3: Reiniciar Backend

```bash
cd backend
run.bat  # o bash run.sh

# El backend automáticamente:
# 1. Detectará PostgreSQL
# 2. Creará las tablas
# 3. Estará listo para usar
```

### Paso 4: Verificar Conexión

```bash
# En otra terminal:
curl http://localhost:8000/api/health

# Deberías ver:
# {"status": "healthy", "service": "comunidad-api", ...}
```

---

## 🗄️ Tablas que se Crearán

Cuando cambies a PostgreSQL, automáticamente se crearán en la base de datos `comunidad`:

```sql
usuarios                (10 columnas)
configuracion_campos    (17 columnas)
integraciones_api       (12 columnas)
consultas_externas      (11 columnas)
campos_usuario          (8 columnas)
```

---

## 📊 Verificar Tablas en PostgreSQL

### Opción 1: pgAdmin (GUI Laragon)
1. Abre **pgAdmin** desde Laragon
2. Conecta a servidor local
3. Ve a **Databases → comunidad**
4. Verifica que las tablas existen

### Opción 2: Terminal
```bash
# Conectar a PostgreSQL
psql -h localhost -U root -d comunidad

# Ver tablas
\dt

# Ver estructura de una tabla
\d usuarios

# Salir
\q
```

### Opción 3: Python
```python
python << 'EOF'
from app.db.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
for table in inspector.get_table_names():
    cols = len(inspector.get_columns(table))
    print(f"{table}: {cols} columnas")
EOF
```

---

## 🐛 Troubleshooting

### Error: "Connection refused"
```
ERROR: connection to server at "localhost" (127.0.0.1), port 5432 failed
```

**Solución:**
- [ ] Abre Laragon
- [ ] Verifica que PostgreSQL está activado
- [ ] Reinicia PostgreSQL (botón stop → start)
- [ ] Vuelve a intentar

### Error: "Database 'comunidad' does not exist"
```
ERROR: FATAL: database "comunidad" does not exist
```

**Solución:**
1. Abre pgAdmin en Laragon
2. Crea una nueva base de datos llamada `comunidad`
3. O ejecuta en terminal:
```bash
createdb -h localhost -U root comunidad
```

### Error: "Role root does not exist"
```
ERROR: role "root" does not exist
```

**Solución:**
1. Verifica el usuario PostgreSQL en Laragon (puede ser `postgres`, `laragon`, o `root`)
2. Actualiza `.env` con el usuario correcto:
```
DATABASE_URL=postgresql://USUARIO@localhost:5432/comunidad
```

---

## 📝 Sintaxis de DATABASE_URL

Formato PostgreSQL:
```
postgresql://[usuario]:[contraseña]@[host]:[puerto]/[database]
```

Ejemplos:
```bash
# Sin contraseña (actual)
postgresql://root@localhost:5432/comunidad

# Con contraseña
postgresql://root:password@localhost:5432/comunidad

# Host diferente
postgresql://root@192.168.1.100:5432/comunidad

# Puerto diferente
postgresql://root@localhost:5433/comunidad
```

---

## ✅ Checklist para PostgreSQL

- [ ] PostgreSQL está activado en Laragon
- [ ] PostgreSQL está corriendo (status = running)
- [ ] Base de datos `comunidad` existe
- [ ] `.env` tiene la URL de PostgreSQL correcta
- [ ] Backend reiniciado
- [ ] `curl http://localhost:8000/api/health` responde
- [ ] Tablas visibles en pgAdmin o terminal

---

## 🔄 Volver a SQLite

Si necesitas volver a SQLite (sin PostgreSQL):

1. Edita `.env`:
```bash
DATABASE_URL=sqlite:///./comunidad.db
```

2. Elimina base de datos anterior (opcional):
```bash
rm backend/comunidad.db
```

3. Reinicia backend:
```bash
run.bat
```

**Nota:** Todos los datos se perderán al cambiar entre SQLite y PostgreSQL.

---

## 📚 Documentación

Ver también:
- [MIGRACIONES_Y_SETUP.md](MIGRACIONES_Y_SETUP.md) - Manejo de migraciones
- [BACKEND_SETUP.md](BACKEND_SETUP.md) - Setup del backend
- [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md) - Estado completo del sistema

---

## 🚀 Resumen

**Actualmente:** SQLite (sin dependencias)
**Opción 1:** Cambiar a PostgreSQL cuando Laragon lo proporciona
**Opción 2:** Mantener SQLite para desarrollo local

Ambas configuraciones están soportadas. Solo necesitas actualizar una línea en `.env`.

---

*PostgreSQL Setup: 2026-04-25*  
*Base de datos disponible: comunidad*
