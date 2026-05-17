"""Check all users"""
import sys
sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
try:
    usuarios = db.query(Usuario).all()
    print(f'Total usuarios: {len(usuarios)}\n')

    for idx, u in enumerate(usuarios[:10], 1):
        print(f'{idx}. ID={u.id}, email={u.email}')
        print(f'   nombres={repr(u.nombres)}, apellido_paterno={repr(u.apellido_paterno)}, apellido_materno={repr(u.apellido_materno)}')
        print(f'   nombre_completo={repr(u.nombre_completo)}')
        print()

    if len(usuarios) > 10:
        print(f'... y {len(usuarios) - 10} usuarios más')

finally:
    db.close()
