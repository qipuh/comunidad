"""
Script para migrar nombre_completo a campos separados (nombres, apellido_paterno, apellido_materno)
"""

from app.db.database import engine, SessionLocal
from app.models.usuario import Usuario
import sqlalchemy as sa

def migrate_nombres_apellidos():
    """Divide nombre_completo en nombres, apellido_paterno, apellido_materno"""
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()

        for usuario in usuarios:
            if not usuario.nombre_completo:
                continue

            partes = usuario.nombre_completo.split()

            if len(partes) >= 3:
                # Formato: Nombres Apellido_Paterno Apellido_Materno
                usuario.nombres = ' '.join(partes[:-2])
                usuario.apellido_paterno = partes[-2]
                usuario.apellido_materno = partes[-1]
            elif len(partes) == 2:
                # Formato: Nombres Apellido
                usuario.nombres = partes[0]
                usuario.apellido_paterno = partes[1]
                usuario.apellido_materno = None
            elif len(partes) == 1:
                # Solo un nombre
                usuario.nombres = partes[0]
                usuario.apellido_paterno = None
                usuario.apellido_materno = None

        db.commit()
        print(f"[OK] Migrados {len(usuarios)} usuarios exitosamente")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_nombres_apellidos()
