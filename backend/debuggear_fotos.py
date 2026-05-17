#!/usr/bin/env python3
"""
Script para debuggear las rutas de fotos vinculadas
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.usuario import Usuario
from dotenv import load_dotenv

load_dotenv()

# Configurar BD
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./comunidad.db"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Buscar usuarios con foto frontal
usuarios_con_foto = db.query(Usuario).filter(Usuario.foto_frontal != None, Usuario.foto_frontal != "").limit(10).all()

print(f"📊 Verificando {len(usuarios_con_foto)} usuarios con foto frontal...\n")

for usuario in usuarios_con_foto:
    ruta_en_bd = usuario.foto_frontal
    ruta_completa = Path(ruta_en_bd)
    ruta_absoluta = Path(ruta_en_bd).resolve() if Path(ruta_en_bd).is_absolute() else Path.cwd() / ruta_en_bd

    existe = ruta_absoluta.exists()

    print(f"👤 {usuario.numero_dni} - {usuario.nombre_completo}")
    print(f"   Ruta en BD:       {ruta_en_bd}")
    print(f"   Ruta absoluta:    {ruta_absoluta}")
    print(f"   ✓ Archivo existe:  {existe}")

    if existe:
        tamaño = ruta_absoluta.stat().st_size
        print(f"   📦 Tamaño:        {tamaño} bytes")
    print()

db.close()
