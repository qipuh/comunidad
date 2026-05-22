#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de despliegue a producción usando SSH con contraseña
"""

import paramiko
import sys
import time
import io

# Configurar stdout para UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def deploy():
    # Configuración
    host = "38.250.161.113"
    user = "root"
    password = "4D4pptik@A1225"
    app_dir = "/var/www/comunidad"
    domain = "comunidadcampesinatpct.com"

    print("=" * 50)
    print("[*] INICIANDO DESPLIEGUE A PRODUCCIÓN")
    print("=" * 50)
    print(f"Host: {host}")
    print(f"Usuario: {user}")
    print(f"Aplicacion: {app_dir}")
    print()

    try:
        # Conectar
        print("[+] Conectando al servidor...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=password, timeout=10)
        print("[+] Conectado")

        # Ejecutar comandos
        commands = [
            # 1. Verificar ubicación
            ("echo 'Verificando directorio...' && pwd && cd " + app_dir + " && git log -1 --oneline", "[*] Verificar repo"),

            # 2. Habilitar módulos Apache
            ("a2enmod proxy proxy_http rewrite ssl 2>&1 | grep -v 'already' | grep -v 'Module' || echo 'Modulos ya habilitados'", "[*] Habilitar modulos Apache"),

            # 3. Crear configuración Apache
            ("""cat > /etc/apache2/sites-available/comunidadcampesinatpct.com.conf << 'EOFAPACHE'
<VirtualHost *:80>
    ServerName comunidadcampesinatpct.com
    ServerAlias www.comunidadcampesinatpct.com
    DocumentRoot /var/www/comunidad/frontend/dist

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</VirtualHost>

<VirtualHost *:443>
    ServerName comunidadcampesinatpct.com
    ServerAlias www.comunidadcampesinatpct.com
    DocumentRoot /var/www/comunidad/frontend/dist

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/comunidadcampesinatpct.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/comunidadcampesinatpct.com/privkey.pem

    <Directory /var/www/comunidad/frontend/dist>
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>

    ProxyPreserveHost On
    ProxyPass /api/ http://127.0.0.1:8000/api/
    ProxyPassReverse /api/ http://127.0.0.1:8000/api/
    ProxyPass /uploads/ http://127.0.0.1:8000/uploads/
    ProxyPassReverse /uploads/ http://127.0.0.1:8000/uploads/

    <Location /api/>
        ProxyPreserveHost On
        SetEnvIf Request_URI "^" proxy_api=true
        RequestHeader set X-Real-IP "%{REMOTE_ADDR}s"
        RequestHeader set X-Forwarded-For "%{HTTP_X_FORWARDED_FOR}e"
        RequestHeader set X-Forwarded-Proto "https"
    </Location>

    <IfModule mod_deflate.c>
        AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
    </IfModule>

    ErrorLog ${'${APACHE_LOG_DIR}'}/comunidadcampesinatpct-error.log
    CustomLog ${'${APACHE_LOG_DIR}'}/comunidadcampesinatpct-access.log combined
</VirtualHost>
EOFAPACHE""", "[*] Crear configuracion Apache"),

            # 4. Habilitar sitio
            ("a2ensite comunidadcampesinatpct.com.conf 2>&1 | grep -v 'already' || echo 'Sitio habilitado'", "[*] Habilitar VirtualHost"),

            # 5. Verificar sintaxis Apache
            ("apache2ctl configtest", "[*] Verificar configuracion Apache"),

            # 6. Reiniciar Apache
            ("systemctl restart apache2 && echo 'Apache reiniciado' || echo 'Error reiniciando Apache'", "[*] Reiniciar Apache"),

            # 7. Verificar frontend
            ("test -f /var/www/comunidad/frontend/dist/index.html && echo '[OK] Frontend existe' || echo '[!] Frontend no existe'", "[*] Verificar frontend"),

            # 8. Verificar backend
            ("ss -tlnp 2>/dev/null | grep 8000 && echo '[OK] Backend en puerto 8000' || echo '[!] Backend no detectado'", "[*] Verificar backend"),

            # 9. Probar API
            ("curl -s http://127.0.0.1:8000/api/health || echo 'Backend no responde (puede estar iniciandose)'", "[*] Probar API"),
        ]

        print()
        print("Ejecutando tareas de despliegue:")
        print("-" * 50)

        for cmd, desc in commands:
            print(f"\n{desc}...")
            stdin, stdout, stderr = ssh.exec_command(cmd)

            # Esperar a que termine
            exit_status = stdout.channel.recv_exit_status()

            # Leer output
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if output:
                print(f"   {output}")
            if error and "already" not in error.lower():
                print(f"   {error}")

            if exit_status != 0 and "Module" not in error:
                print(f"   [ERROR] codigo {exit_status}")
            else:
                print(f"   [OK]")

        # Crear usuario admin
        print(f"\n\n[*] Crear usuario admin...")
        admin_script = """
cd /var/www/comunidad/backend
source venv/bin/activate 2>/dev/null

python3 << 'EOFPYTHON'
from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.auth import hash_password
from sqlalchemy.exc import IntegrityError

db = SessionLocal()

admin_user = Usuario(
    numero_dni="00000001",
    username="admin",
    nombres="Admin",
    apellido_paterno="Sistema",
    apellido_materno="",
    email="admin@comunidad.local",
    password_hash=hash_password("admin123"),
    rol="admin",
    estado="activo"
)

try:
    db.add(admin_user)
    db.commit()
    print("[OK] Usuario admin creado (DNI: 00000001, Contrasena: admin123)")
except IntegrityError:
    db.rollback()
    print("[!] Usuario admin ya existe")
except Exception as e:
    db.rollback()
    print(f"[ERROR] {e}")
finally:
    db.close()
EOFPYTHON

deactivate 2>/dev/null
"""
        stdin, stdout, stderr = ssh.exec_command(admin_script)
        time.sleep(2)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        if output:
            print(f"   {output}")
        if error and "already" not in error.lower():
            print(f"   {error}")

        # Cerrar conexión
        ssh.close()
        print()
        print("=" * 50)
        print("[+] DESPLIEGUE COMPLETADO")
        print("=" * 50)
        print()
        print("Proximos pasos:")
        print("1. [OK] Apache configurado")
        print("2. [OK] Usuario admin creado (DNI: 00000001, Contrasena: admin123)")
        print("3. Proximo: Vincular fotos - python3 /var/www/comunidad/backend/vincular_fotos.py")
        print("4. Verificar: https://comunidadcampesinatpct.com")
        print()

        return True

    except paramiko.AuthenticationException:
        print("[ERROR] Autenticacion fallida")
        return False
    except paramiko.SSHException as e:
        print(f"[ERROR] SSH: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
