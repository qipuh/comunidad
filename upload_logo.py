#!/usr/bin/env python3
"""Subir logo a producción"""
import paramiko, sys, io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("38.250.161.113", username="root", password="4D4pptik@A1225", timeout=20, allow_agent=False, look_for_keys=False)

for d in ["logo", "img", "img/ecoser", "img/inicio", "img/organizacion", "img/nosotros", "img/produccion", "img/variadas", "img/clientes"]:
    ssh.exec_command(f"mkdir -p /var/www/comunidad/backend/uploads/{d}")[1].channel.recv_exit_status()

sftp = ssh.open_sftp()
import os
for sub in ["logo", "img", "img/ecoser", "img/inicio", "img/organizacion", "img/nosotros", "img/produccion", "img/variadas", "img/clientes"]:
    local_dir = f"C:/laragon/www/comunidad/backend/uploads/{sub}"
    for f in os.listdir(local_dir):
        local = f"{local_dir}/{f}"
        if os.path.isdir(local):
            continue
        remote = f"/var/www/comunidad/backend/uploads/{sub}/{f}"
        sftp.put(local, remote)
        print(f"Subido {sub}/{f}")
sftp.close()

stdin, stdout, _ = ssh.exec_command("ls -la /var/www/comunidad/backend/uploads/logo/ /var/www/comunidad/backend/uploads/img/")
print(stdout.read().decode())
ssh.close()
print("[OK] Logo subido")
