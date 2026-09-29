#!/usr/bin/env python3
"""Deploy: git pull, build frontend, restart backend"""
import paramiko, sys, io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HOST, USER, PASS = "38.250.161.113", "root", "4D4pptik@A1225"
APP_DIR = "/var/www/comunidad"

def run(ssh, cmd, desc=""):
    if desc:
        print(f"\n>>> {desc}\n$ {cmd[:200]}")
    _, out, err = ssh.exec_command(cmd, timeout=600)
    o = out.read().decode('utf-8', errors='replace')
    e = err.read().decode('utf-8', errors='replace')
    if o: print(o[:3000])
    if e: print(f"ERR: {e[:1500]}")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS, timeout=20, allow_agent=False, look_for_keys=False)

run(ssh, f"cd {APP_DIR} && git pull origin master", "Git pull")
run(ssh, f"cd {APP_DIR}/frontend && npm run build", "Build frontend")
run(ssh, "systemctl restart comunidad-backend && sleep 3 && curl -sS http://127.0.0.1:8000/api/health", "Restart + health")
ssh.close()
print("\n[OK] Deploy completado")
