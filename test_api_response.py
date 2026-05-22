#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')

from app.db.database import SessionLocal
from app.models.usuario import Usuario
import json

db = SessionLocal()

# Simular lo que hace el endpoint /api/usuarios
usuarios = db.query(Usuario).order_by(Usuario.created_at.desc()).limit(100).offset(0).all()

data = []
for u in usuarios[:10]:  # Solo los primeros 10
    item = {
        "id": u.id,
        "email": u.email,
        "username": u.username,
        "nombres": u.nombres,
        "numero_dni": u.numero_dni,
        "num_padron": u.num_padron,
        "nombre_completo": u.nombre_completo,
        "rol": u.rol,
        "estado": u.estado,
    }
    data.append(item)

print("API Response (primeros 10 usuarios):")
print(json.dumps(data, indent=2, ensure_ascii=False))

# Verificar que num_padron está presente
print("\n\nVerificación del campo num_padron:")
for item in data:
    padron = item.get('num_padron')
    print(f"ID {item['id']}: num_padron = {repr(padron)}, present = {'num_padron' in item}")

db.close()
