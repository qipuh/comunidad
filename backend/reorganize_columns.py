"""
Script para reorganizar las columnas de la tabla usuarios
Mover nombres, apellido_paterno, apellido_materno después de numero_dni
"""

from app.db.database import engine
import sqlalchemy as sa

def reorganize_columns():
    """Reorganiza las columnas de la tabla usuarios"""
    with engine.connect() as connection:
        try:
            # Mover nombres después de numero_dni
            connection.execute(sa.text("""
                ALTER TABLE usuarios
                MODIFY COLUMN nombres VARCHAR(255) NULL AFTER numero_dni
            """))
            print("[OK] Columna 'nombres' movida después de 'numero_dni'")
        except Exception as e:
            print(f"[ERROR] Error moviendo 'nombres': {e}")

        try:
            # Mover apellido_paterno después de nombres
            connection.execute(sa.text("""
                ALTER TABLE usuarios
                MODIFY COLUMN apellido_paterno VARCHAR(255) NULL AFTER nombres
            """))
            print("[OK] Columna 'apellido_paterno' movida después de 'nombres'")
        except Exception as e:
            print(f"[ERROR] Error moviendo 'apellido_paterno': {e}")

        try:
            # Mover apellido_materno después de apellido_paterno
            connection.execute(sa.text("""
                ALTER TABLE usuarios
                MODIFY COLUMN apellido_materno VARCHAR(255) NULL AFTER apellido_paterno
            """))
            print("[OK] Columna 'apellido_materno' movida después de 'apellido_paterno'")
        except Exception as e:
            print(f"[ERROR] Error moviendo 'apellido_materno': {e}")

        connection.commit()
        print("[OK] Reorganización completada")

if __name__ == "__main__":
    reorganize_columns()
