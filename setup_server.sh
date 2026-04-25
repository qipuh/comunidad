#!/bin/bash
# ============================================================
# Script de configuración - comunidad.adapptika.com
# Ejecutar como root en el servidor 38.250.161.113
# ============================================================

set -e
DOMAIN="comunidad.adapptika.com"
APP_DIR="/var/www/comunidad"
DB_NAME="comunidad"
DB_USER="root"
DB_PASS="4D4pptik@A1225"

echo "================================================"
echo " Configurando Sistema Comunidad en $DOMAIN"
echo "================================================"

# ── 1. Dependencias del sistema ──────────────────────────────
echo "[1/7] Instalando dependencias del sistema..."
apt-get update -qq
apt-get install -y python3 python3-pip python3-venv nodejs npm nginx git curl 2>/dev/null

# ── 2. Crear base de datos MySQL ─────────────────────────────
echo "[2/7] Creando base de datos MySQL..."
mysql -u root -p"$DB_PASS" <<SQL
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL
echo "  Base de datos lista."

# ── 3. Clonar/actualizar el repositorio ──────────────────────
echo "[3/7] Descargando código..."
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR" && git pull origin master
else
    git clone https://github.com/qipuh/comunidad.git "$APP_DIR"
fi
cd "$APP_DIR"

# ── 4. Configurar Backend (FastAPI) ──────────────────────────
echo "[4/7] Configurando backend..."
cd "$APP_DIR/backend"

python3 -m venv venv
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Archivo .env de producción
cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:4D4pptik%40A1225@localhost:3306/comunidad
SECRET_KEY=$(openssl rand -hex 32)
ENVIRONMENT=production
ALLOWED_ORIGINS=https://$DOMAIN,http://$DOMAIN
EOF

mkdir -p uploads/usuarios

# Crear tablas en MySQL
python3 -c "
from app.db.database import init_db
init_db()
print('  Tablas creadas en MySQL')
"

deactivate

# ── 5. Servicio systemd ──────────────────────────────────────
echo "[5/7] Configurando servicio systemd..."
chown -R www-data:www-data "$APP_DIR/backend"

cat > /etc/systemd/system/comunidad-api.service << EOF
[Unit]
Description=Comunidad FastAPI Backend
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=$APP_DIR/backend
Environment="PATH=$APP_DIR/backend/venv/bin"
EnvironmentFile=$APP_DIR/backend/.env
ExecStart=$APP_DIR/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable comunidad-api
systemctl restart comunidad-api
sleep 3

if systemctl is-active --quiet comunidad-api; then
    echo "  API backend: CORRIENDO"
else
    echo "  ERROR en API. Ver: journalctl -u comunidad-api -n 50"
    journalctl -u comunidad-api -n 20 --no-pager
fi

# ── 6. Compilar Frontend ─────────────────────────────────────
echo "[6/7] Compilando frontend Vue..."
cd "$APP_DIR/frontend"

# Apuntar API a ruta relativa (Nginx hace el proxy)
sed -i "s|http://localhost:8080/api|/api|g" src/services/api.ts
sed -i "s|http://localhost:8000/api|/api|g" src/services/api.ts

npm install --silent
npm run build
echo "  Frontend compilado en dist/"

# ── 7. Configurar Nginx ──────────────────────────────────────
echo "[7/7] Configurando Nginx..."
cat > /etc/nginx/sites-available/comunidad << 'EOF'
server {
    listen 80;
    listen 443 ssl;
    server_name comunidad.adapptika.com;

    # SSL (ya configurado previamente)
    ssl_certificate /etc/letsencrypt/live/comunidad.adapptika.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/comunidad.adapptika.com/privkey.pem;

    # Redirigir HTTP a HTTPS
    if ($scheme = http) {
        return 301 https://$host$request_uri;
    }

    # Frontend Vue compilado
    root /var/www/comunidad/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy al backend FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        client_max_body_size 20M;
    }

    # Fotos subidas
    location /uploads/ {
        alias /var/www/comunidad/backend/uploads/;
        expires 30d;
    }
}
EOF

ln -sf /etc/nginx/sites-available/comunidad /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

nginx -t && systemctl reload nginx
echo "  Nginx configurado OK"

echo ""
echo "================================================"
echo " CONFIGURACION COMPLETADA"
echo "================================================"
echo " URL:      https://$DOMAIN"
echo " API docs: https://$DOMAIN/api/docs"
echo " Health:   https://$DOMAIN/api/health"
echo ""
echo " Comandos utiles:"
echo "   Ver logs:      journalctl -u comunidad-api -f"
echo "   Reiniciar API: systemctl restart comunidad-api"
echo "   Estado:        systemctl status comunidad-api"
echo "================================================"
