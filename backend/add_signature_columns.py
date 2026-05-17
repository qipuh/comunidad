"""
Migration script to add signature columns to configuracion_carnet table.
"""
import os
import sys
from sqlalchemy import create_engine, text

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app.db.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

def add_signature_columns():
    """Add firma_secretario_url and firma_presidente_url columns"""
    with engine.connect() as conn:
        try:
            # Check if columns exist first
            result = conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'configuracion_carnet'
                AND COLUMN_NAME IN ('firma_secretario_url', 'firma_presidente_url')
            """))
            existing = [row[0] for row in result]

            if 'firma_secretario_url' not in existing:
                print("Adding firma_secretario_url column...")
                conn.execute(text("""
                    ALTER TABLE configuracion_carnet
                    ADD COLUMN firma_secretario_url VARCHAR(500) NULL
                """))
                print("[OK] firma_secretario_url added")
            else:
                print("[OK] firma_secretario_url already exists")

            if 'firma_presidente_url' not in existing:
                print("Adding firma_presidente_url column...")
                conn.execute(text("""
                    ALTER TABLE configuracion_carnet
                    ADD COLUMN firma_presidente_url VARCHAR(500) NULL
                """))
                print("[OK] firma_presidente_url added")
            else:
                print("[OK] firma_presidente_url already exists")

            conn.commit()
            print("\n[OK] Migration completed successfully!")

        except Exception as e:
            print(f"[ERROR] {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    add_signature_columns()
