"""
Migración para agregar padrón de electores e impugnación de votos.
Ejecutar como: python migracion_elecciones_v2.py
"""
import sqlite3
from pathlib import Path
import sys

# Forzar UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ruta de la BD
db_path = Path(__file__).parent / "app" / "db" / "comunidad.db"
print(f"Conectando a: {db_path}")

def ejecutar_migracion():
    """Ejecuta los cambios de BD para el sistema de padrón e impugnación."""
    if not db_path.exists():
        print(f"ERROR: BD no encontrada en {db_path}")
        return False

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        print("\n[1] Verificando tabla votos...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='votos'")
        if not cursor.fetchone():
            print("  ADVERTENCIA: tabla votos no existe. Las tablas se crearán automáticamente al iniciar FastAPI.")
            print("  Abortando migración. Por favor, inicia el backend primero.")
            return False

        print("[2] Agregando columnas de impugnación a tabla votos...")

        # Verificar si ya existen las columnas
        cursor.execute("PRAGMA table_info(votos)")
        columnas = [col[1] for col in cursor.fetchall()]

        if "impugnado" not in columnas:
            cursor.execute("ALTER TABLE votos ADD COLUMN impugnado BOOLEAN DEFAULT 0")
            print("  [OK] Columna 'impugnado' agregada")
        else:
            print("  [SKIP] Columna 'impugnado' ya existe")

        if "motivo_impugnacion" not in columnas:
            cursor.execute("ALTER TABLE votos ADD COLUMN motivo_impugnacion TEXT")
            print("  [OK] Columna 'motivo_impugnacion' agregada")
        else:
            print("  [SKIP] Columna 'motivo_impugnacion' ya existe")

        if "impugnado_por" not in columnas:
            cursor.execute("ALTER TABLE votos ADD COLUMN impugnado_por INTEGER")
            print("  [OK] Columna 'impugnado_por' agregada")
        else:
            print("  [SKIP] Columna 'impugnado_por' ya existe")

        if "impugnado_at" not in columnas:
            cursor.execute("ALTER TABLE votos ADD COLUMN impugnado_at DATETIME")
            print("  [OK] Columna 'impugnado_at' agregada")
        else:
            print("  [SKIP] Columna 'impugnado_at' ya existe")

        print("\n[3] Creando tabla padron_eleccion...")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS padron_eleccion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eleccion_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(eleccion_id, usuario_id),
                FOREIGN KEY(eleccion_id) REFERENCES elecciones(id) ON DELETE CASCADE,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        """)
        print("  [OK] Tabla 'padron_eleccion' creada o verificada")

        conn.commit()
        print("\n[SUCCESS] Migracion completada exitosamente")
        return True

    except Exception as e:
        print(f"\n[ERROR] Error durante la migración: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    ejecutar_migracion()
