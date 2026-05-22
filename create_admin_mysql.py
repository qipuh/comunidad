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
print("[*] CREANDO USUARIO ADMIN EN BASE DE DATOS")
print("=" * 60)

# Primero, verificar qué credenciales de BD existen
check_config = """
grep -r "DATABASE_URL\\|DB_USER\\|DB_PASSWORD" /var/www/comunidad/backend/.env* /var/www/comunidad/backend/app/config.py 2>/dev/null || echo "No .env encontrado"
"""

print("\n[1/3] Buscando credenciales de BD...")
stdin, stdout, stderr = ssh.exec_command(check_config)
config_output = stdout.read().decode()
print(config_output if config_output else "Sin credenciales encontradas")

# Intentar crear usuario directamente con MySQL
create_user_mysql = """
mysql -u root -p'4D4pptik@A1225' -e "
USE comunidad;
INSERT INTO usuarios (email, username, password_hash, rol, estado, created_at)
VALUES ('admin@comunidad.test', 'admin', 'password', 'admin', 'activo', NOW())
ON DUPLICATE KEY UPDATE password_hash='password', rol='admin';
SELECT CONCAT('Usuario creado exitosamente. ID: ', id) as resultado FROM usuarios WHERE email='admin@comunidad.test';
" 2>&1
"""

print("\n[2/3] Creando usuario en MySQL...")
stdin, stdout, stderr = ssh.exec_command(create_user_mysql)
mysql_output = stdout.read().decode()
mysql_error = stderr.read().decode()

print(mysql_output)
if mysql_error and "Warning" not in mysql_error:
    print("Errores: " + mysql_error)

# Verificar que se creó
verify_user = """
mysql -u root -p'4D4pptik@A1225' -e "SELECT id, email, rol FROM comunidad.usuarios WHERE email='admin@comunidad.test';" 2>&1
"""

print("\n[3/3] Verificando usuario creado...")
stdin, stdout, stderr = ssh.exec_command(verify_user)
verify_output = stdout.read().decode()
print(verify_output)

print("\n" + "=" * 60)
print("[+] COMPLETADO")
print("=" * 60)
print("\nCredenciales de acceso:")
print("   Email: admin@comunidad.test")
print("   Contraseña: password")
print("\nAccede a: https://comunidadcampesinatpct.com")

ssh.close()
