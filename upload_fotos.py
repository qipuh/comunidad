#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko
import os
from pathlib import Path
import sys
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

host = "38.250.161.113"
user = "root"
password = "4D4pptik@A1225"

# Directorio local de fotos
local_dir = Path(r"c:\laragon\www\comunidad\backend\uploads\usuarios")
remote_dir = "/var/www/comunidad/backend/uploads/usuarios/"

# Conectar
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=password, timeout=10)
sftp = ssh.open_sftp()

# Obtener lista de fotos locales
fotos_locales = list(local_dir.glob("*.png")) + list(local_dir.glob("*.jpg")) + list(local_dir.glob("*.jpeg"))
print(f"[*] Encontradas {len(fotos_locales)} fotos locales")
print(f"[*] Subiendo a {remote_dir}...\n")

subidas = 0
errores = 0

for i, foto_path in enumerate(fotos_locales, 1):
    try:
        remote_path = remote_dir + foto_path.name
        print(f"[{i}/{len(fotos_locales)}] Subiendo {foto_path.name}...", end=" ", flush=True)

        sftp.put(str(foto_path), remote_path)
        sftp.chmod(remote_path, 0o664)

        print("✅")
        subidas += 1
    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
        errores += 1

sftp.close()

print(f"\n{'='*60}")
print(f"✅ Subidas:    {subidas}")
print(f"❌ Errores:    {errores}")
print(f"📁 Total:      {len(fotos_locales)}")
print(f"{'='*60}")

if subidas > 0:
    print(f"\n[*] Ejecutando vincular_fotos.py...")
    stdin, stdout, stderr = ssh.exec_command(
        "cd /var/www/comunidad/backend && python3 vincular_fotos.py",
        timeout=120
    )
    output = stdout.read().decode()
    print(output)

ssh.close()
print("\n[+] Completado!")
