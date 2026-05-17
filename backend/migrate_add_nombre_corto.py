"""
Script para agregar la columna nombre_corto a la tabla configuracion_carnet
"""

from app.db.database import engine
import sqlalchemy as sa

def add_nombre_corto_column():
    """Agrega la columna nombre_corto si no existe"""
    with engine.connect() as connection:
        try:
            # Intentar agregar la columna
            connection.execute(sa.text("""
                ALTER TABLE configuracion_carnet
                ADD COLUMN nombre_corto VARCHAR(20) DEFAULT 'CC.TPCT' NOT NULL
            """))
            connection.commit()
            print("[OK] Columna 'nombre_corto' agregada exitosamente")
        except Exception as e:
            if "Duplicate column name" in str(e) or "already exists" in str(e):
                print("[INFO] La columna 'nombre_corto' ya existe")
            else:
                print(f"[ERROR] {e}")

if __name__ == "__main__":
    add_nombre_corto_column()
