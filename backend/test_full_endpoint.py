"""Test full endpoint response"""
import sys
sys.path.insert(0, '.')
import json

from app.db.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()
try:
    usuarios = db.query(Usuario).order_by(Usuario.created_at.desc()).limit(5).offset(0).all()
    total = db.query(Usuario).count()

    respuesta = {
        "success": True,
        "count": len(usuarios),
        "total": total,
        "limit": 5,
        "offset": 0,
        "data": []
    }

    for u in usuarios:
        try:
            item = {
                "id": u.id,
                "email": u.email,
                "username": u.username,
                "nombres": u.nombres,
                "apellido_paterno": u.apellido_paterno,
                "apellido_materno": u.apellido_materno,
                "nombre_completo": u.nombre_completo,
                "numero_dni": u.numero_dni,
                "telefono": u.telefono,
                "fecha_nacimiento": u.fecha_nacimiento,
                "sexo": u.sexo,
                "estado_civil": u.estado_civil,
                "direccion": u.direccion,
                "departamento": u.departamento,
                "provincia": u.provincia,
                "distrito": u.distrito,
                "anexo": u.anexo,
                "foto_url": u.foto_url,
                "foto_frontal": u.foto_frontal,
                "foto_lateral_izq": u.foto_lateral_izq,
                "foto_lateral_der": u.foto_lateral_der,
                "usar_reconocimiento_facial": u.usar_reconocimiento_facial,
                "rol": u.rol,
                "estado": u.estado,
                "fecha_inicio_cobranza": u.fecha_inicio_cobranza.isoformat() if u.fecha_inicio_cobranza else None,
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "updated_at": u.updated_at.isoformat() if u.updated_at else None
            }
            respuesta["data"].append(item)
        except Exception as e:
            print(f"ERROR en usuario {u.id}: {e}")
            import traceback
            traceback.print_exc()

    try:
        json_str = json.dumps(respuesta, ensure_ascii=False, indent=2)
        print("[OK] Respuesta JSON OK")
        print(f"Tamaño: {len(json_str)} caracteres")
    except Exception as e:
        print(f"[ERROR] Error serializando a JSON: {e}")

finally:
    db.close()
