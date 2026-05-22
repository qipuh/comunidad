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

print("[*] Actualizando código...")
stdin, stdout, stderr = ssh.exec_command("cd /var/www/comunidad && git pull origin master")
print(stdout.read().decode())

print("[*] Reiniciando backend...")
stdin, stdout, stderr = ssh.exec_command("systemctl restart comunidad-api || pkill -f 'uvicorn.*8001'")
stdout.channel.recv_exit_status()

print("[*] Esperando que inicie el backend...")
import time
time.sleep(2)

print("[*] Verificando backend...")
stdin, stdout, stderr = ssh.exec_command("ss -tlnp | grep 8001")
print(stdout.read().decode())

print("\n[+] Backend actualizado y reiniciado!")

ssh.close()
