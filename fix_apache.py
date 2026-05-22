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

print("[*] Actualizando DocumentRoot en Apache...")
# Cambiar DocumentRoot en la configuración
stdin, stdout, stderr = ssh.exec_command(
    "sed -i 's|DocumentRoot /var/www/comunidad/public|DocumentRoot /var/www/comunidad/frontend/dist|g' /etc/apache2/sites-enabled/000-comunidadcampesinatpct.com-le-ssl.conf"
)
stdout.channel.recv_exit_status()

print("[*] Verificando cambios...")
stdin, stdout, stderr = ssh.exec_command("grep -n 'DocumentRoot' /etc/apache2/sites-enabled/000-comunidadcampesinatpct.com-le-ssl.conf")
print(stdout.read().decode())

print("[*] Validando sintaxis de Apache...")
stdin, stdout, stderr = ssh.exec_command("apache2ctl configtest")
output = stdout.read().decode()
print(output)

print("[*] Reiniciando Apache...")
stdin, stdout, stderr = ssh.exec_command("systemctl restart apache2")
stdout.channel.recv_exit_status()

print("[*] Verificando status de Apache...")
stdin, stdout, stderr = ssh.exec_command("systemctl status apache2 --no-pager | head -10")
print(stdout.read().decode())

print("\n[+] Apache actualizado y reiniciado!")
print("\nAccede a https://comunidadcampesinatpct.com en tu navegador")
print("Recuerda hacer: Ctrl+Shift+Del para limpiar cache del navegador")

ssh.close()
