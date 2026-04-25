# Migraciones y Setup de Base de Datos

**Fecha:** 2026-04-25  
**Status:** ✅ Base de datos lista y funcionando

---

## 📊 Enfoque de Migraciones

Este proyecto usa **dos enfoques de manera complementaria:**

### 1. Desarrollo: SQLAlchemy Auto-Create (Actual)
```python
# En app/db/database.py
Base.metadata.create_all(bind=engine)
```

**Ventajas:**
- ✅ Rápido para desarrollo
- ✅ Sincroniza automáticamente con modelos
- ✅ No hay desyncronización entre código y DB
- ✅ Perfecto para iteración rápida

**Cómo funciona:**
1. Defines modelos en `app/models/`
2. Al iniciar el backend, se crean las tablas automáticamente
3. Cambias modelos → reinicia → tablas se actualizan

### 2. Producción: Alembic Migrations (Preparado)
```bash
alembic revision --autogenerate -m "descripción"
alembic upgrade head
```

**Ventajas:**
- ✅ Control de versiones de schema
- ✅ Rollback a versión anterior
- ✅ Auditoria de cambios
- ✅ Mejor para equipos
- ✅ Zero-downtime updates

**Cómo funciona:**
1. Alembic detecta cambios en modelos
2. Genera archivo de migración
3. Ejecutas: `alembic upgrade head`
4. Historial en `migrations/versions/`

---

## 🔄 Estado Actual de Migraciones

### ✅ Infraestructura Alembic
```
migrations/
├── alembic.ini              ← Configuración Alembic
├── env.py                   ← Ambiente de ejecución
├── script.py.mako          ← Template de migraciones
├── README                  ← Info del directorio
└── versions/
    └── 001_initial_schema.py  ← Documentación inicial
```

### ✅ Base de Datos Actual
```
comunidad.db (SQLite)
├── usuarios (10 cols)
├── configuracion_campos (17 cols)
├── integraciones_api (12 cols)
├── consultas_externas (11 cols)
└── campos_usuario (8 cols)
```

### ✅ Modelos SQLAlchemy
```
app/models/
├── usuario.py              ← Usuario model
└── configuracion.py        ← 4 config models
```

**Estado:** Todas las tablas creadas. Modelos sincronizados con DB.

---

## 🔧 Cómo Trabajar con Migraciones

### Para Desarrollo (Ahora)

**1. Agregar un nuevo campo al modelo:**
```python
# En app/models/usuario.py
class Usuario(Base):
    telefono = Column(String(20), nullable=True)  # Nuevo campo
```

**2. Reiniciar backend:**
```bash
cd backend
run.bat  # o bash run.sh
```

**3. SQLAlchemy automáticamente:**
- ✅ Crea la columna en la DB
- ✅ Sincroniza el schema
- ✅ Backend listo

### Para Producción (Cuando lo necesites)

**1. Generar migración:**
```bash
cd backend
alembic revision --autogenerate -m "Agregar campo telefono a usuarios"
```

**2. Ver la migración generada:**
```bash
# Se crea: migrations/versions/002_agregar_campo_telefono_a_usuarios.py
cat migrations/versions/002_*.py
```

**3. Aplicar migración:**
```bash
alembic upgrade head
```

**4. Revertir si es necesario:**
```bash
alembic downgrade -1  # Vuelve a la versión anterior
```

---

## 📝 Crear Nueva Migración Manualmente

Si necesitas hacer cambios más complejos:

```python
# migrations/versions/002_custom_change.py
"""Descripción de cambios

Revision ID: 002
Revises: 001
Create Date: 2026-04-25
"""
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    # Agregar columna
    op.add_column('usuarios', sa.Column('telefono', sa.String(20), nullable=True))
    
    # Crear índice
    op.create_index('ix_usuarios_telefono', 'usuarios', ['telefono'])


def downgrade() -> None:
    # Eliminar índice
    op.drop_index('ix_usuarios_telefono', 'usuarios')
    
    # Eliminar columna
    op.drop_column('usuarios', 'telefono')
```

Luego ejecutar:
```bash
alembic upgrade head
```

---

## 🚀 Transición a Producción

### Paso 1: Cambiar de SQLite a PostgreSQL
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/comunidad
```

### Paso 2: Ejecutar migraciones en producción
```bash
alembic upgrade head
```

### Paso 3: Iniciar backend (sin init_db())
```python
# main.py - comentar init_db() para producción
# init_db()  # Solo para desarrollo
```

---

## 📋 Checklist de Migraciones

- [x] SQLAlchemy models creados (5 tablas)
- [x] Base de datos inicializada (comunidad.db)
- [x] Alembic configurado
- [x] Migraciones preparadas
- [x] env.py listo
- [x] Documentación de migraciones

**Próximos pasos:**
- [ ] Cambiar a PostgreSQL (si lo necesitas)
- [ ] Generar migraciones con Alembic (cuando hagas cambios)
- [ ] Versionar migraciones en Git

---

## 🐛 Troubleshooting Migraciones

### Problema: "Relation already exists"
```bash
# Solución: Elimina comunidad.db y reinicia
rm backend/comunidad.db
# Backend auto-recreará las tablas
```

### Problema: "Column already exists"
```bash
# Asegúrate que no creaste la columna en dos lugares
# Busca en app/models/ y elimina duplicados
```

### Problema: Alembic no detecta cambios
```bash
# Asegúrate de importar todos los modelos en env.py
# Ver: migrations/env.py línea 13-16
from app.models.usuario import Usuario
from app.models.configuracion import ConfiguracionCampo, ...
```

### Problema: "Target database is not up to date"
```bash
# Aplica todas las migraciones pendientes
alembic upgrade head

# O ver el estado actual
alembic current
alembic history
```

---

## 📊 Entender tu Database

### Ver estructura actual
```bash
# En Python:
python << 'EOF'
from app.db.database import SessionLocal, engine
from sqlalchemy import inspect

inspector = inspect(engine)
for table_name in inspector.get_table_names():
    print(f"\n{table_name}:")
    for column in inspector.get_columns(table_name):
        print(f"  - {column['name']}: {column['type']}")
EOF
```

### Ver todas las migraciones
```bash
alembic history
```

### Ver migración pendiente
```bash
alembic current  # muestra revisión actual
alembic upgrade head --sql  # muestra SQL sin ejecutar
```

---

## 🎯 Recomendaciones

### Para Desarrollo
✅ Usa `Base.metadata.create_all()` (actual)
✅ Reinicia backend cuando cambies modelos
✅ No uses Alembic aún
✅ Sé flexible con cambios

### Para Producción
✅ Usa PostgreSQL (en lugar de SQLite)
✅ Crea migraciones con Alembic
✅ Versiona migraciones en Git
✅ Prueba migraciones locales antes de prod
✅ Ten rollback plan

### Transición
1. **Ahora:** SQLite + auto-create (desarrollo)
2. **Pronto:** Cambiar a PostgreSQL
3. **Después:** Usar Alembic para cambios
4. **Producción:** Migraciones versionadas

---

## 📚 Referencias

### Documentación
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)

### En este Proyecto
- Backend: `backend/`
- Modelos: `backend/app/models/`
- Migraciones: `backend/migrations/`
- Config DB: `backend/app/db/database.py`

---

## ✨ Resumen

**Estado Actual:**
- ✅ Base de datos funcionando (SQLite)
- ✅ Todas las tablas creadas
- ✅ Modelos sincronizados
- ✅ Alembic preparado para producción
- ✅ Listo para desarrollo

**Próximos pasos:**
1. Desarrollo con cambios rápidos (reinicia backend)
2. Cuando sea necesario: Cambiar a PostgreSQL
3. Producción: Usar Alembic con migraciones versionadas

---

*Configuración de migraciones: 2026-04-25*  
*Status: ✅ LISTO PARA DESARROLLO*
