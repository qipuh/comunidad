"""
Migration script to add url_qr column to configuracion_carnet table.
"""
import os
import sys
from sqlalchemy import create_engine, text

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app.db.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

def add_url_qr_column():
    """Add url_qr column"""
    with engine.connect() as conn:
        try:
            # Check if column exists
            result = conn.execute(text("""
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'configuracion_carnet'
                AND COLUMN_NAME = 'url_qr'
            """))
            existing = result.fetchone()

            if not existing:
                print("Adding url_qr column...")
                conn.execute(text("""
                    ALTER TABLE configuracion_carnet
                    ADD COLUMN url_qr VARCHAR(500) NULL
                """))
                print("[OK] url_qr added")
            else:
                print("[OK] url_qr already exists")

            conn.commit()
            print("\n[OK] Migration completed successfully!")

        except Exception as e:
            print(f"[ERROR] {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    add_url_qr_column()
