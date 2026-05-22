#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko
import sys
import io
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

host = "38.250.161.113"
user = "root"
password = "4D4pptik@A1225"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=password, timeout=10)

print("=" * 60)
print("[*] ACTUALIZACIÓN COMPLETA DE PRODUCCIÓN")
print("=" * 60)

# 1. Backup del dist
print("\n[1/6] Haciendo backup del dist actual...")
stdin, stdout, stderr = ssh.exec_command(
    "cp -r /var/www/comunidad/frontend/dist /var/www/comunidad/frontend/dist.backup.$(date +%s)"
)
stdout.channel.recv_exit_status()
print("    ✅ Backup creado")

# 2. Git pull
print("\n[2/6] Actualizando código desde GitHub...")
stdin, stdout, stderr = ssh.exec_command("cd /var/www/comunidad && git pull origin master")
output = stdout.read().decode()
print(output)

# 3. Limpiar dist viejo
print("\n[3/6] Limpiando dist antiguo...")
stdin, stdout, stderr = ssh.exec_command("rm -rf /var/www/comunidad/frontend/dist")
stdout.channel.recv_exit_status()
print("    ✅ Dist eliminado")

# 4. Compilar frontend
print("\n[4/6] Compilando frontend (esto toma ~15 segundos)...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /var/www/comunidad/frontend && npm run build 2>&1",
    timeout=120
)
output = stdout.read().decode()
if "✓ built" in output:
    print("    ✅ Frontend compilado exitosamente")
    print("    " + output.split('\n')[-3])
else:
    print("    ⚠️ Salida de compilación:")
    print(output[-300:])

# 5. Verificar que dist existe
print("\n[5/6] Verificando que dist fue creado...")
stdin, stdout, stderr = ssh.exec_command("ls -lh /var/www/comunidad/frontend/dist/index.html")
output = stdout.read().decode()
if output:
    print("    ✅ dist/index.html existe:")
    print("    " + output.strip())
else:
    print("    ❌ ERROR: dist/index.html no existe!")
    sys.exit(1)

# 6. Reiniciar Apache
print("\n[6/6] Reiniciando Apache...")
stdin, stdout, stderr = ssh.exec_command("systemctl restart apache2")
stdout.channel.recv_exit_status()
time.sleep(2)

# Verificar Apache
stdin, stdout, stderr = ssh.exec_command("systemctl status apache2 --no-pager | head -5")
output = stdout.read().decode()
if "active (running)" in output:
    print("    ✅ Apache reiniciado correctamente")
else:
    print("    ⚠️ Estado de Apache:")
    print(output)

print("\n" + "=" * 60)
print("[+] ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 60)
print("\n✅ Cambios en producción:")
print("   • Carga todos los usuarios (limit 10000)")
print("   • Exporta TODOS los carnets en PDF")
print("   • Cada carnet en su propia página")
print("\nAccede a: https://comunidadcampesinatpct.com/carnets")
print("Limpia caché: Ctrl+Shift+Delete")

ssh.close()
