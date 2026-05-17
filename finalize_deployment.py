#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko

host = "38.250.161.113"
user = "root"
password = "4D4pptik@A1225"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=password, timeout=10)

print("[*] Instalando dependencias del backend...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /var/www/comunidad/backend && pip install python-jose cryptography -q",
    timeout=60
)
stdout.channel.recv_exit_status()

print("[*] Creando usuario admin...")
admin_cmd = "cd /var/www/comunidad/backend && python3 -c \"from app.db.database import SessionLocal; from app.models.usuario import Usuario; from app.utils.auth import hash_password; from sqlalchemy.exc import IntegrityError; db = SessionLocal(); admin = Usuario(numero_dni='00000001', nombres='Admin', apellido_paterno='Sistema', apellido_materno='', email='admin@comunidad.local', password_hash=hash_password('admin123'), rol='admin', estado='activo'); db.add(admin) if not db.query(Usuario).filter_by(numero_dni='00000001').first() else None; db.commit() if not db.query(Usuario).filter_by(numero_dni='00000001').first() else print('Existe'); print('[OK] Admin creado')\" 2>&1"

stdin, stdout, stderr = ssh.exec_command(admin_cmd, timeout=30)
output = stdout.read().decode().strip()
print(output if output else "[OK] Usuario admin configurado")

print("[*] Ejecutando vincular_fotos.py...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /var/www/comunidad/backend && python3 vincular_fotos.py 2>&1 | head -20",
    timeout=30
)
output = stdout.read().decode().strip()
print(output if output else "[OK] Script ejecutado")

print("[*] Verificando servicios...")
stdin, stdout, stderr = ssh.exec_command(
    "ss -tlnp 2>/dev/null | grep -E ':80|:443|:8000'",
    timeout=10
)
output = stdout.read().decode().strip()
if output:
    print(output)

ssh.close()

print("\n" + "=" * 60)
print("[+] DESPLIEGUE COMPLETADO EXITOSAMENTE")
print("=" * 60)
print("\nAcceso a la aplicacion:")
print("  URL: https://comunidadcampesinatpct.com")
print("  DNI: 00000001")
print("  Contrasena: admin123")
print("\n[!] CAMBIAR CONTRASENA DESPUES DEL PRIMER LOGIN")
print("=" * 60)
