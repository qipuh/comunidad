#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')

from app.db.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()

# Verificar primeros 125 usuarios
usuarios = db.query(Usuario).order_by(Usuario.created_at).limit(125).all()

print("Verificacion: Primeros 125 usuarios - num_padron asignados")
print(f"{'ID':<5} {'DNI':<12} {'Nombre':<30} {'Num Padron':<12}")
print("-" * 65)

for u in usuarios:
    nombre = (u.nombres or "")[:28]
    print(f"{u.id:<5} {u.numero_dni:<12} {nombre:<30} {u.num_padron:<12}")

# Específicamente buscar el DNI 04412242
print("\n\nBuscando DNI 04412242:")
user = db.query(Usuario).filter(Usuario.numero_dni == "04412242").first()
if user:
    print(f"Encontrado - ID: {user.id}, Nombre: {user.nombres}, num_padron: {user.num_padron}")
else:
    print("No encontrado")

# Verificar que no hay duplicados de num_padron
from sqlalchemy import func
duplicados = db.query(Usuario.num_padron, func.count(Usuario.id)).group_by(Usuario.num_padron).having(func.count(Usuario.id) > 1).all()
print(f"\n\nDuplicados de num_padron: {len(duplicados)}")
if duplicados:
    for padron, count in duplicados:
        print(f"  {padron}: {count} usuarios")

db.close()
