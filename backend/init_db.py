"""
Script para inicializar la base de datos con todos los modelos.
Ejecutar como: python init_db.py
"""
import sys
from pathlib import Path

# Agregar el directorio backend al path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.configuracion import Base
from app.models.usuario import Usuario
from app.models.eleccion import Eleccion, OpcionEleccion, Voto, PadronEleccion
from app.models.cobranza import *
from app.models.factiliza import *
from app.models.reunion import *
from app.db.database import engine

def init_db():
    """Crea todas las tablas en la BD."""
    print("Creando todas las tablas...")
    Base.metadata.create_all(bind=engine)
    print("[SUCCESS] Tablas creadas correctamente")

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"[ERROR] Error al crear las tablas: {e}")
        sys.exit(1)
