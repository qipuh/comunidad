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

print("[*] Verificando si el archivo tiene el fix...")
stdin, stdout, stderr = ssh.exec_command("grep -n 'nombre_completo = ' /var/www/comunidad/backend/app/routes/usuarios.py")
output = stdout.read().decode()
print("Ocurrencias de 'nombre_completo =':")
print(output if output else "No encontrado")

print("\n[*] Buscando todas las referencias a nombre_completo en usuarios.py...")
stdin, stdout, stderr = ssh.exec_command("grep -n 'nombre_completo' /var/www/comunidad/backend/app/routes/usuarios.py | grep -v '#'")
print(stdout.read().decode())

print("\n[*] Matando todos los procesos uvicorn...")
stdin, stdout, stderr = ssh.exec_command("pkill -9 uvicorn; sleep 1")
stdout.channel.recv_exit_status()

print("[*] Iniciando uvicorn en modo foreground para ver logs...")
stdin, stdout, stderr = ssh.exec_command("cd /var/www/comunidad/backend && nohup uvicorn app.main:app --host 127.0.0.1 --port 8001 > /tmp/uvicorn.log 2>&1 &")
stdout.channel.recv_exit_status()

print("[*] Esperando que inicie...")
import time
time.sleep(3)

print("[*] Verificando que está corriendo...")
stdin, stdout, stderr = ssh.exec_command("ps aux | grep uvicorn | grep -v grep")
print(stdout.read().decode())

print("[*] Últimas líneas del log de uvicorn...")
stdin, stdout, stderr = ssh.exec_command("tail -20 /tmp/uvicorn.log")
print(stdout.read().decode())

ssh.close()
print("\n[+] Backend reiniciado")
