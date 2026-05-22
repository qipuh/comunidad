#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko
import sys
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

host = "38.250.161.113"
user = "root"
password = "4D4pptik@A1225"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=password, timeout=10)

print("=" * 60)
print("[*] CREANDO USUARIO ADMIN")
print("=" * 60)

# Ejecutar comando para crear el usuario en la BD
create_user_script = """
cd /var/www/comunidad/backend
export PYTHONPATH=/var/www/comunidad/backend:$PYTHONPATH
python3 << 'EOF'
import sys
sys.path.insert(0, '/var/www/comunidad/backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Conectar a la BD MySQL
DB_USER = 'comunidad'
DB_PASSWORD = 'comunidad123'
DB_HOST = 'localhost'
DB_NAME = 'comunidad_db'

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Importar modelo
from app.models import Usuario

db = SessionLocal()

# Verificar si el usuario ya existe
usuario_existente = db.query(Usuario).filter_by(email='admin@comunidad.test').first()
if usuario_existente:
    print("⚠️ El usuario admin@comunidad.test ya existe")
    db.close()
    exit(0)

# Crear usuario admin
nuevo_usuario = Usuario(
    email='admin@comunidad.test',
    password_hash='password',
    rol='admin',
    estado='activo'
)

db.add(nuevo_usuario)
db.commit()
db.refresh(nuevo_usuario)

print(f"✅ Usuario creado exitosamente")
print(f"   Email: admin@comunidad.test")
print(f"   Rol: admin")
print(f"   ID: {nuevo_usuario.id}")

db.close()
EOF
"""

stdin, stdout, stderr = ssh.exec_command(create_user_script, timeout=30)
output = stdout.read().decode()
error = stderr.read().decode()

print("\n[Salida]:")
print(output)

if error:
    print("\n[Errores]:")
    print(error)

print("\n" + "=" * 60)
print("[+] COMPLETADO")
print("=" * 60)
print("\nCredenciales de acceso:")
print("   Email: admin@comunidad.test")
print("   Contraseña: password")
print("\nAccede a: https://comunidadcampesinatpct.com")

ssh.close()
