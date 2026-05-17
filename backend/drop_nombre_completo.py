"""
Script para eliminar la columna nombre_completo de la tabla usuarios
"""

from app.db.database import engine
import sqlalchemy as sa

def drop_nombre_completo():
    """Elimina la columna nombre_completo de la tabla usuarios"""
    with engine.connect() as connection:
        try:
            connection.execute(sa.text("""
                ALTER TABLE usuarios
                DROP COLUMN nombre_completo
            """))
            connection.commit()
            print("[OK] Columna 'nombre_completo' eliminada")
        except Exception as e:
            if "Unknown column" in str(e) or "no such column" in str(e):
                print("[INFO] Columna 'nombre_completo' ya no existe")
            else:
                print(f"[ERROR] {e}")

if __name__ == "__main__":
    drop_nombre_completo()
