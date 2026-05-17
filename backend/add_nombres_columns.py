"""
Script para agregar las columnas nombres, apellido_paterno, apellido_materno a la tabla usuarios
"""

from app.db.database import engine
import sqlalchemy as sa

def add_columns():
    """Agrega las columnas a la tabla usuarios"""
    with engine.connect() as connection:
        try:
            # Agregar columna nombres
            connection.execute(sa.text("""
                ALTER TABLE usuarios
                ADD COLUMN nombres VARCHAR(255) NULL
            """))
            print("[OK] Columna 'nombres' agregada")
        except Exception as e:
            if "Duplicate column" in str(e) or "already exists" in str(e):
                print("[INFO] Columna 'nombres' ya existe")
            else:
                print(f"[ERROR] {e}")

        try:
            # Agregar columna apellido_paterno
            connection.execute(sa.text("""
                ALTER TABLE usuarios
                ADD COLUMN apellido_paterno VARCHAR(255) NULL
            """))
            print("[OK] Columna 'apellido_paterno' agregada")
        except Exception as e:
            if "Duplicate column" in str(e) or "already exists" in str(e):
                print("[INFO] Columna 'apellido_paterno' ya existe")
            else:
                print(f"[ERROR] {e}")

        try:
            # Agregar columna apellido_materno
            connection.execute(sa.text("""
                ALTER TABLE usuarios
                ADD COLUMN apellido_materno VARCHAR(255) NULL
            """))
            print("[OK] Columna 'apellido_materno' agregada")
        except Exception as e:
            if "Duplicate column" in str(e) or "already exists" in str(e):
                print("[INFO] Columna 'apellido_materno' ya existe")
            else:
                print(f"[ERROR] {e}")

        connection.commit()

if __name__ == "__main__":
    add_columns()
