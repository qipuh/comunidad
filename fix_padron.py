#!/usr/bin/env python3
"""
Script para asignar números de padron a usuarios que los necesitan.
Los números de padron se asignan secuencialmente de 0001 en adelante.
"""
import sys
sys.path.insert(0, 'backend')

from app.db.database import SessionLocal
from app.models.usuario import Usuario
from datetime import datetime

db = SessionLocal()

# Obtener usuarios sin num_padron
usuarios_sin_padron = db.query(Usuario).filter(
    (Usuario.num_padron == None) | (Usuario.num_padron == '')
).order_by(Usuario.created_at).all()

print(f"Usuarios sin num_padron: {len(usuarios_sin_padron)}")

if usuarios_sin_padron:
    # Obtener el máximo número de padron actual
    max_padron = db.query(Usuario).filter(
        Usuario.num_padron != None,
        Usuario.num_padron != ''
    ).order_by(Usuario.num_padron.desc()).first()

    max_num = 0
    if max_padron and max_padron.num_padron:
        try:
            max_num = int(max_padron.num_padron)
        except:
            max_num = 0

    print(f"Máximo número de padron actual: {max_num:04d}")

    # Asignar nuevos números de padron
    next_num = max_num + 1
    for usuario in usuarios_sin_padron:
        usuario.num_padron = f"{next_num:04d}"
        usuario.updated_at = datetime.now()
        print(f"  Asignado {next_num:04d} a usuario ID {usuario.id} (DNI: {usuario.numero_dni})")
        next_num += 1

    db.commit()
    print(f"\nSe asignaron {len(usuarios_sin_padron)} números de padron exitosamente")
else:
    print("No hay usuarios sin num_padron")

db.close()
