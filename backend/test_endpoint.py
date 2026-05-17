"""Test endpoint to check serialization"""
import sys
sys.path.insert(0, '.')
import json

from app.db.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
try:
    usuarios = db.query(Usuario).limit(2).all()

    for u in usuarios:
        respuesta = {
            "id": u.id,
            "email": u.email,
            "username": u.username,
            "nombres": u.nombres,
            "apellido_paterno": u.apellido_paterno,
            "apellido_materno": u.apellido_materno,
            "nombre_completo": u.nombre_completo,
            "numero_dni": u.numero_dni,
            "rol": u.rol,
        }
        try:
            json_str = json.dumps(respuesta, ensure_ascii=False, indent=2)
            print(f"Usuario {u.id} - OK")
            print(json_str)
            print()
        except Exception as e:
            print(f"Usuario {u.id} - ERROR: {e}")
            print(f"  respuesta: {respuesta}")

finally:
    db.close()
