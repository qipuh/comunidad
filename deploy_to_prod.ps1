# Deployment script for production server

$host_addr = "38.250.161.113"
$username = "root"
$password = "4D4pptik@A1225"

Write-Host "🚀 Iniciando despliegue a producción en $host_addr..."

# Create SSH commands
$commands = @"
cd /var/www/comunidad && \
echo '📦 Actualizando código...' && \
git pull origin master && \
echo '✅ Código actualizado' && \
\
echo '📦 Instalando dependencias Python...' && \
cd backend && \
pip install -r requirements.txt && \
echo '✅ Dependencias Python instaladas' && \
\
echo '📦 Instalando Chromium para Playwright...' && \
playwright install chromium && \
echo '✅ Chromium instalado' && \
\
echo '📦 Instalando dependencias del sistema...' && \
playwright install-deps && \
echo '✅ Dependencias del sistema instaladas' && \
\
echo '🔄 Reiniciando backend...' && \
python restart_backend.py && \
echo '✅ Backend reiniciado' && \
\
cd /var/www/comunidad/frontend && \
echo '📦 Compilando frontend...' && \
npm run build && \
echo '✅ Frontend compilado' && \
\
echo '✅✅✅ ¡Despliegue completado exitosamente!'
"@

# Execute via SSH using sshpass if available, otherwise use PowerShell SSH
if (Get-Command sshpass -ErrorAction SilentlyContinue) {
    Write-Host "Usando sshpass para autenticación..."
    sshpass -p $password ssh -o StrictHostKeyChecking=no $username@$host_addr $commands
} else {
    Write-Host "Usando OpenSSH nativo de Windows..."
    # Create a temporary script file
    $scriptContent = @"
#!/bin/bash
$commands
"@
    
    $scriptPath = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.sh'
    Set-Content -Path $scriptPath -Value $scriptContent
    
    # Execute with expect for password
    $expectScript = @"
#!/usr/bin/env expect
set timeout 300
spawn ssh -o StrictHostKeyChecking=no $username@$host_addr < $scriptPath
expect "password:"
send "$password\r"
expect eof
"@
    
    $expectPath = [System.IO.Path]::GetTempFileName() -replace '\.tmp$', '.exp'
    Set-Content -Path $expectPath -Value $expectScript
    
    expect $expectPath
}

Write-Host "✅ Despliegue completado!"
