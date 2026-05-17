#!/usr/bin/env python3
"""
Script para vincular automáticamente las fotos frontales a los usuarios.
Las fotos deben estar en uploads/usuarios/ nombradas por DNI (ej: 12345678.png)
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

# Ruta de fotos
UPLOAD_DIR = Path("uploads/usuarios")
if not UPLOAD_DIR.exists():
    print(f"❌ Carpeta {UPLOAD_DIR} no existe")
    exit(1)

# Extensiones permitidas
EXTENSIONES_PERMITIDAS = {'.png', '.jpg', '.jpeg', '.webp'}

# Procesar fotos
fotos_encontradas = list(UPLOAD_DIR.glob("*"))
print(f"📁 Encontradas {len(fotos_encontradas)} fotos\n")

vinculados = 0
no_encontrados = 0
ya_vinculados = 0
errores = 0

for foto_path in fotos_encontradas:
    if not foto_path.is_file():
        continue

    ext = foto_path.suffix.lower()
    if ext not in EXTENSIONES_PERMITIDAS:
        continue

    # Extraer DNI del nombre del archivo
    dni = foto_path.stem  # nombre sin extensión

    # Buscar usuario
    usuario = db.query(Usuario).filter(Usuario.numero_dni == dni).first()

    if not usuario:
        print(f"⚠️  DNI {dni}: Usuario no encontrado")
        no_encontrados += 1
        continue

    # Ruta relativa para almacenar
    ruta_relativa = f"uploads/usuarios/{foto_path.name}"

    # Verificar si ya tiene foto frontal
    if usuario.foto_frontal and usuario.foto_frontal != "":
        print(f"⏭️  DNI {dni} ({usuario.nombre_completo}): Ya tiene foto frontal")
        ya_vinculados += 1
        continue

    try:
        # Actualizar
        usuario.foto_frontal = ruta_relativa
        db.commit()
        print(f"✅ DNI {dni} ({usuario.nombre_completo}): Foto vinculada")
        vinculados += 1
    except Exception as e:
        print(f"❌ DNI {dni}: Error al vincular - {str(e)}")
        db.rollback()
        errores += 1

# Resumen
print("\n" + "="*60)
print(f"📊 RESUMEN")
print("="*60)
print(f"✅ Vinculadas:      {vinculados}")
print(f"⏭️  Ya tenían foto:  {ya_vinculados}")
print(f"⚠️  No encontrados:  {no_encontrados}")
print(f"❌ Errores:         {errores}")
print(f"📁 Total procesadas: {vinculados + ya_vinculados + no_encontrados + errores}")
print("="*60)

db.close()
