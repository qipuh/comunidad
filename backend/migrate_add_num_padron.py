"""
Script para agregar la columna num_padron a la tabla usuarios.
Ejecutar como: python migrate_add_num_padron.py
"""
import sys
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import engine
from sqlalchemy import text

def migrate():
    """Agrega la columna num_padron a la tabla usuarios si no existe."""
    try:
        with engine.connect() as connection:
            # Verificar si la columna ya existe
            result = connection.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME='usuarios' AND COLUMN_NAME='num_padron'
            """))

            if result.fetchone():
                print("[INFO] La columna num_padron ya existe en la tabla usuarios")
                return

            # Agregar la columna
            connection.execute(text("""
                ALTER TABLE usuarios
                ADD COLUMN num_padron VARCHAR(50) NULL
            """))

            # Crear índice
            connection.execute(text("""
                CREATE INDEX idx_num_padron ON usuarios(num_padron)
            """))

            connection.commit()
            print("[SUCCESS] Columna num_padron agregada correctamente a la tabla usuarios")
    except Exception as e:
        print(f"[ERROR] Error al agregar la columna: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
