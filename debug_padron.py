#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')

from app.db.database import SessionLocal
from app.models.usuario import Usuario
from sqlalchemy import text

db = SessionLocal()

# Verificar si hay algún problema con el almacenamiento o lectura de num_padron
usuarios = db.query(Usuario).order_by(Usuario.id).limit(122).all()

# Verificar el tipo de datos y valores
print("Verificación de num_padron (primeros 15):")
for i, u in enumerate(usuarios[:15]):
    padron_value = u.num_padron
    padron_type = type(padron_value).__name__
    padron_repr = repr(padron_value)
    print(f"ID {u.id}: type={padron_type}, value={padron_repr}, bool={bool(padron_value)}")

# Usar SQL directo para ver cómo se almacenan
print("\n\nDirectamente desde SQL (primeros 10):")
result = db.execute(text("SELECT id, numero_dni, num_padron FROM usuarios LIMIT 10"))
for row in result:
    print(f"ID {row[0]}: num_padron = {repr(row[2])}")

# Verificar si hay valores vacíos siendo guardados
print("\n\nVerificación de valores vacíos:")
empty_check = db.execute(text("SELECT COUNT(*) as cnt FROM usuarios WHERE num_padron = '' OR num_padron IS NULL"))
result = empty_check.fetchone()
print(f"Usuarios con num_padron vacío o NULL: {result[0]}")

# Verificar el rango de números de padron
print("\n\nRango de números de padron:")
min_max = db.execute(text("SELECT MIN(num_padron), MAX(num_padron) FROM usuarios WHERE num_padron != '' AND num_padron IS NOT NULL"))
row = min_max.fetchone()
print(f"MIN: {row[0]}, MAX: {row[1]}")

db.close()
