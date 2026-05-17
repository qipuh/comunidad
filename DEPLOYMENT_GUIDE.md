# Guía de Despliegue - Comunidad TPCT

## Estado Actual
- ✅ Código actualizado en el servidor (último commit: `e7baa16`)
- ✅ Base de datos migrada a producción
- ⚠️ Apache VirtualHost necesita configuración para `comunidadcampesinatpct.com`
- ⚠️ Backend debe estar corriendo en puerto 8000

---

## 1. Conectar al Servidor

```bash
ssh -o StrictHostKeyChecking=no root@38.250.161.113
# Contraseña: 4D4pptik@A1225
```

---

## 2. Copiar la Configuración de Apache

El archivo `comunidadcampesinatpct.com.conf` debe copiarse al servidor:

### Opción A: Copiar manualmente vía SCP
```bash
scp comunidadcampesinatpct.com.conf root@38.250.161.113:/etc/apache2/sites-available/
```

### Opción B: En el servidor, crear el archivo
```bash
cat > /etc/apache2/sites-available/comunidadcampesinatpct.com.conf << 'EOF'
<VirtualHost *:80>
    ServerName comunidadcampesinatpct.com
    ServerAlias www.comunidadcampesinatpct.com
    DocumentRoot /var/www/comunidad/frontend/dist

    # Redirect HTTP to HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</VirtualHost>

<VirtualHost *:443>
    ServerName comunidadcampesinatpct.com
    ServerAlias www.comunidadcampesinatpct.com
    DocumentRoot /var/www/comunidad/frontend/dist

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/comunidadcampesinatpct.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/comunidadcampesinatpct.com/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/comunidadcampesinatpct.com/chain.pem

    # Vue Router - SPA fallback to index.html
    <Directory /var/www/comunidad/frontend/dist>
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>

    # Proxy API requests to FastAPI backend
    ProxyPreserveHost On
    ProxyPass /api/ http://127.0.0.1:8000/api/
    ProxyPassReverse /api/ http://127.0.0.1:8000/api/

    # Proxy uploads
    ProxyPass /uploads/ http://127.0.0.1:8000/uploads/
    ProxyPassReverse /uploads/ http://127.0.0.1:8000/uploads/

    # Set proper headers for proxied requests
    <Location /api/>
        ProxyPreserveHost On
        SetEnvIf Request_URI "^" proxy_api=true
        RequestHeader set X-Real-IP "%{REMOTE_ADDR}s"
        RequestHeader set X-Forwarded-For "%{HTTP_X_FORWARDED_FOR}e"
        RequestHeader set X-Forwarded-Proto "https"
    </Location>

    # Enable compression
    <IfModule mod_deflate.c>
        AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/comunidadcampesinatpct-error.log
    CustomLog ${APACHE_LOG_DIR}/comunidadcampesinatpct-access.log combined
</VirtualHost>
EOF
```

---

## 3. Habilitar el VirtualHost en Apache

```bash
# Habilitar módulos necesarios
a2enmod proxy
a2enmod proxy_http
a2enmod rewrite
a2enmod ssl

# Habilitar el nuevo VirtualHost
a2ensite comunidadcampesinatpct.com.conf

# Deshabilitar el sitio por defecto si está activo
a2dissite 000-default.conf

# Verificar sintaxis de Apache
apache2ctl configtest
# Debe mostrar: "Syntax OK"

# Reiniciar Apache
systemctl restart apache2
```

---

## 4. Verificar que el Backend esté corriendo

```bash
# Revisar estado del servicio (si está configurado con systemd)
systemctl status comunidad-api

# O verificar si uvicorn está escuchando en puerto 8000
ss -tlnp | grep 8000

# Probar la API localmente
curl http://127.0.0.1:8000/api/health
# Debe retornar: {"status": "ok"}
```

### Si el backend no está corriendo:
```bash
cd /var/www/comunidad/backend

# Activar el entorno virtual
source venv/bin/activate

# Ejecutar el servidor
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
# O usar gunicorn: gunicorn -w 2 -b 127.0.0.1:8000 app.main:app
```

---

## 5. Compilar el Frontend (si necesario)

```bash
cd /var/www/comunidad/frontend

# Si no está compilado
npm run build

# Verificar que dist/ exista
ls -la dist/
```

---

## 6. Crear Usuario Admin (si aún no existe)

```bash
cd /var/www/comunidad/backend
source venv/bin/activate

python3 << 'EOF'
from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.auth import hash_password
from sqlalchemy.exc import IntegrityError

db = SessionLocal()

# Crear usuario admin
admin_user = Usuario(
    numero_dni="00000001",
    nombres="Admin",
    apellido_paterno="Sistema",
    apellido_materno="",
    email="admin@comunidad.local",
    password_hash=hash_password("admin123"),  # Cambiar después
    rol="admin",
    estado="activo"
)

try:
    db.add(admin_user)
    db.commit()
    print("✓ Usuario admin creado exitosamente")
except IntegrityError:
    db.rollback()
    print("⚠ El usuario admin ya existe")
except Exception as e:
    db.rollback()
    print(f"✗ Error: {e}")
finally:
    db.close()
EOF

deactivate
```

---

## 7. Ejecutar Script de Vinculación de Fotos

```bash
cd /var/www/comunidad/backend
source venv/bin/activate

# El script busca fotos en backend/uploads/usuarios/ 
# y las vincula a usuarios por DNI
python3 vincular_fotos.py

# Ejemplo de output:
# ✓ Vinculadas 45 fotos a usuarios
# ⚠ 3 fotos no encontraron usuario (DNI no existe)

deactivate
```

---

## 8. Verificar la Aplicación

### Prueba en Navegador
1. Ir a https://comunidadcampesinatpct.com
2. Ver que se carga el formulario de login
3. Intentar login con: 
   - DNI: `00000001`
   - Contraseña: `admin123`
4. Verificar que se redirige al dashboard

### Verificar Logs de Apache (si hay errores)
```bash
tail -f /var/apache_log_dir/comunidadcampesinatpct-error.log

# O si estás en /var/log/apache2:
tail -f /var/log/apache2/comunidadcampesinatpct-error.log
```

### Verificar Logs del Backend
```bash
# Si está corriendo con systemd:
journalctl -u comunidad-api -f

# O si está corriendo en terminal:
# Ver la salida directamente donde se ejecutó uvicorn
```

---

## 9. Solucionar Problemas Comunes

### "ProxyPass not allowed here" error
- Asegúrate de que `a2enmod proxy` y `a2enmod proxy_http` están habilitados
- Ejecuta `apache2ctl configtest` para verificar

### "Cannot connect to upstream http://127.0.0.1:8000"
- Verifica que el backend esté corriendo: `ss -tlnp | grep 8000`
- Verifica que no haya firewall bloqueando: `sudo ufw status`
- Habilita ProxyPass: `a2enmod proxy_http`

### "404 Not Found" al acceder a /api/
- Verifica ProxyPass en la config: `grep -n "ProxyPass /api/" /etc/apache2/sites-available/comunidadcampesinatpct.com.conf`
- Reinicia Apache: `systemctl restart apache2`

### SSL Certificate Issues
- Verifica certificados: `ls -la /etc/letsencrypt/live/comunidadcampesinatpct.com/`
- Si faltan, crear con certbot:
  ```bash
  certbot certonly --standalone -d comunidadcampesinatpct.com -d www.comunidadcampesinatpct.com
  ```

---

## Resumen de Puertos y Servicios

| Servicio | Puerto | Host | Acceso |
|----------|--------|------|--------|
| Apache (Frontend + Proxy) | 80/443 | `comunidadcampesinatpct.com` | Público |
| FastAPI Backend | 8000 | 127.0.0.1 | Interno (proxy vía Apache) |
| MySQL | 3306 | 127.0.0.1 | Interno |

---

## Checklist Final

- [ ] Apache VirtualHost configurado para `comunidadcampesinatpct.com`
- [ ] Módulos proxy habilitados (`a2enmod proxy proxy_http`)
- [ ] Backend corriendo en puerto 8000
- [ ] Frontend compilado en `dist/`
- [ ] SSL certificates configurados
- [ ] Usuario admin creado
- [ ] Script vincular_fotos.py ejecutado
- [ ] Login funciona correctamente
- [ ] API responde en https://comunidadcampesinatpct.com/api/health

---

## Comandos Rápidos

```bash
# Ver estado de todo
systemctl status apache2
systemctl status comunidad-api  # si existe
ss -tlnp | grep -E "80|443|8000"

# Reiniciar Apache y backend
systemctl restart apache2
systemctl restart comunidad-api

# Ver logs recientes
tail -30 /var/log/apache2/comunidadcampesinatpct-error.log
journalctl -u comunidad-api -n 30
```
