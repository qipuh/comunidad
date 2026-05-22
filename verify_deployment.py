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

print("[*] Verificando frontend dist...")
stdin, stdout, stderr = ssh.exec_command("ls -lah /var/www/comunidad/frontend/dist/ | head -15")
print(stdout.read().decode())

print("\n[*] Verificando que index.html existe...")
stdin, stdout, stderr = ssh.exec_command("ls -lh /var/www/comunidad/frontend/dist/index.html && wc -l /var/www/comunidad/frontend/dist/index.html")
print(stdout.read().decode())

print("\n[*] Verificando DocumentRoot en Apache...")
stdin, stdout, stderr = ssh.exec_command("grep -n 'DocumentRoot' /etc/apache2/sites-enabled/000-comunidadcampesinatpct.com-le-ssl.conf")
print(stdout.read().decode())

print("\n[*] Verificando que Apache está sirviendo desde dist...")
stdin, stdout, stderr = ssh.exec_command("curl -s -I https://comunidadcampesinatpct.com/ 2>&1 | head -15")
print(stdout.read().decode())

print("\n[*] Verificando git log del repo en servidor...")
stdin, stdout, stderr = ssh.exec_command("cd /var/www/comunidad && git log --oneline -3")
print(stdout.read().decode())

ssh.close()
print("\n[+] Verificación completada")
