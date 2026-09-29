#!/bin/bash

HOST="38.250.161.113"
USER="root"
PASS='4D4pptik@A1225'
PATH_PROD="/var/www/comunidad"

echo "🚀 Iniciando despliegue a producción..."
echo "Host: $HOST"
echo "Usuario: $USER"
echo "Ruta: $PATH_PROD"
echo ""

# Usar expect para manejar la autenticación
expect << 'EXPECT_SCRIPT'
set timeout 30
set host [lindex $argv 0]
set user [lindex $argv 1]
set pass [lindex $argv 2]
set path [lindex $argv 3]

spawn ssh -o StrictHostKeyChecking=no $user@$host

expect "password:"
send "$pass\r"

expect "~#"
send "cd $path && git pull origin master\r"

expect "~#"
send "cd frontend && npm install --legacy-peer-deps\r"

expect "~#"
send "npm run build\r"

expect "~#"
send "echo '✅ Despliegue completado'\r"

expect "~#"
send "exit\r"

expect eof
EXPECT_SCRIPT
