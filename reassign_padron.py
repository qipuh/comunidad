#!/usr/bin/env python3
"""
Script para reasignar números de padron a TODOS los usuarios de manera secuencial.
Los números de padron se asignan desde 0001 en adelante, ordenados por fecha de creación.
"""
import sys
sys.path.insert(0, 'backend')

from app.db.database import SessionLocal
from app.models.usuario import Usuario
from datetime import datetime

db = SessionLocal()

# Obtener todos los usuarios ordenados por fecha de creación
usuarios = db.query(Usuario).order_by(Usuario.created_at).all()

print(f"Total de usuarios a reasignar: {len(usuarios)}")
print(f"\nPrimeros 10 usuarios (antes):")

# Mostrar antes
for u in usuarios[:10]:
    print(f"  ID {u.id}: num_padron = {u.num_padron}")

# Reasignar números
for idx, usuario in enumerate(usuarios, start=1):
    nuevo_num_padron = f"{idx:04d}"
    usuario.num_padron = nuevo_num_padron
    usuario.updated_at = datetime.now()

db.commit()

print(f"\nPrimeros 10 usuarios (después):")
usuarios_updated = db.query(Usuario).order_by(Usuario.created_at).limit(10).all()
for u in usuarios_updated:
    print(f"  ID {u.id}: num_padron = {u.num_padron}")

print(f"\nÚltimos 10 usuarios (después):")
usuarios_updated_last = db.query(Usuario).order_by(Usuario.created_at.desc()).limit(10).all()
for u in reversed(usuarios_updated_last):
    print(f"  ID {u.id}: num_padron = {u.num_padron}")

print(f"\n✅ Reasignación completada: {len(usuarios)} usuarios con números de padron secuenciales")

db.close()
