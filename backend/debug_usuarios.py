"""Debug script to check usuarios"""
import sys
sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
try:
    usuarios = db.query(Usuario).limit(3).all()
    print(f'Total usuarios: {len(usuarios)}')
    for u in usuarios:
        print(f'\nID: {u.id}')
        print(f'  email: {u.email}')
        print(f'  nombres: {repr(u.nombres)}')
        print(f'  apellido_paterno: {repr(u.apellido_paterno)}')
        print(f'  apellido_materno: {repr(u.apellido_materno)}')
        try:
            print(f'  nombre_completo: {repr(u.nombre_completo)}')
        except Exception as e:
            print(f'  nombre_completo ERROR: {e}')
finally:
    db.close()
