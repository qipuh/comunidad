"""
Script to check columns in configuracion_carnet table
"""

from app.db.database import engine
import sqlalchemy as sa

def check_columns():
    """Verifica las columnas de la tabla configuracion_carnet"""
    with engine.connect() as connection:
        try:
            # Obtener info de la tabla
            inspector = sa.inspect(engine)
            columns = inspector.get_columns('configuracion_carnet')

            print("Columnas en configuracion_carnet:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_columns()
