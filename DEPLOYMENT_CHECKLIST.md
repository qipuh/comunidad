# Checklist de Despliegue a Producción

## 📋 Resumen del Estado Actual

### ✅ Código Completado
- [x] Registro manual de asistencia con búsqueda en tiempo real
- [x] Sub-tabs dentro de "Asistentes" (Registrados/Faltaron)
- [x] Tab "Reporte" eliminado
- [x] Estadísticas y botón Excel movidos al header del sidebar
- [x] Mejoras UX: gradientes, animaciones, diseño mejorado
- [x] Fix en EleccionDetalleView.vue para export a Excel
- [x] Todos los cambios committeados

### ⚠️ Acciones Pendientes en Producción

---

## 🚀 Pasos de Despliegue (En orden)

### 1️⃣ Configurar Apache VirtualHost
**Ubicación:** Servidor 38.250.161.113  
**Usuario:** root  
**Archivo:** `/etc/apache2/sites-available/comunidadcampesinatpct.com.conf`

**Acción:**
```bash
# Copiar o crear el archivo usando el contenido de "comunidadcampesinatpct.com.conf"
# Luego ejecutar:
a2enmod proxy proxy_http rewrite ssl
a2ensite comunidadcampesinatpct.com.conf
apache2ctl configtest  # Verificar sintaxis
systemctl restart apache2
```

**Verificación:**
```bash
# Acceder a https://comunidadcampesinatpct.com
# Debe cargar la página (aunque el login falle si el backend no responde)
```

---

### 2️⃣ Verificar Backend
**En el servidor:**

```bash
# ¿El backend está corriendo?
ss -tlnp | grep 8000

# Si no está corriendo, iniciar:
cd /var/www/comunidad/backend
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Si está como servicio systemd:
systemctl status comunidad-api
systemctl restart comunidad-api
```

**Prueba de conectividad:**
```bash
curl -I http://127.0.0.1:8000/api/health
# Debe retornar: HTTP/1.1 200 OK
```

---

### 3️⃣ Verificar Frontend Compilado
**En el servidor:**

```bash
ls -la /var/www/comunidad/frontend/dist/index.html
# Debe existir

# Si no existe, compilar:
cd /var/www/comunidad/frontend
npm run build
```

---

### 4️⃣ Crear Usuario Admin (si no existe)
**En el servidor:**

```bash
cd /var/www/comunidad/backend
source venv/bin/activate

python3 << 'EOF'
from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.utils.auth import hash_password
from sqlalchemy.exc import IntegrityError

db = SessionLocal()

admin_user = Usuario(
    numero_dni="00000001",
    nombres="Admin",
    apellido_paterno="Sistema",
    apellido_materno="",
    email="admin@comunidad.local",
    password_hash=hash_password("admin123"),  # CAMBIAR DESPUÉS
    rol="admin",
    estado="activo"
)

try:
    db.add(admin_user)
    db.commit()
    print("✓ Usuario admin creado")
except IntegrityError:
    print("⚠ Usuario admin ya existe")
except Exception as e:
    db.rollback()
    print(f"✗ Error: {e}")
finally:
    db.close()
EOF

deactivate
```

**Credenciales temporales:**
- DNI: `00000001`
- Contraseña: `admin123`
- ⚠️ CAMBIAR PASSWORD DESPUÉS EN LA APP

---

### 5️⃣ Ejecutar Script de Vinculación de Fotos
**En el servidor:**

```bash
cd /var/www/comunidad/backend
source venv/bin/activate

# Asegúrate de que las fotos estén en:
# /var/www/comunidad/backend/uploads/usuarios/DNI.jpg

python3 vincular_fotos.py
# Ejemplo de output:
# ✓ Vinculadas 45 fotos a usuarios
# ⚠ 3 fotos sin usuario coincidente

deactivate
```

---

### 6️⃣ Pruebas en Navegador
**URL:** https://comunidadcampesinatpct.com

#### Test de Login
1. Abrir https://comunidadcampesinatpct.com
2. Ver formulario de login
3. Ingresar:
   - DNI: `00000001`
   - Contraseña: `admin123`
4. Clickear "Entrar"
5. ✅ Debe redirigir al dashboard

#### Test de Asistencia Manual
1. En dashboard, navegar a Reuniones
2. Crear reunión de prueba (o usar existente)
3. Cambiar estado a "en_curso"
4. Clickear "Ver" → Tab "Asistencia"
5. Clickear botón "Registrar Manual"
6. Buscar usuario por nombre/DNI
7. Seleccionar usuario
8. Clickear "Registrar"
9. ✅ Debe aparecer confirmación y aparecer en Tab "Asistentes"

#### Test de Sub-tabs
1. En Tab "Asistentes" del sidebar
2. Ver sub-tabs: "Registrados" y "Faltaron"
3. ✅ "Registrados" debe mostrar asistentes con hora y método
4. ✅ "Faltaron" debe mostrar inasistentes

#### Test de Excel
1. En sidebar, clickear botón "Excel"
2. ✅ Debe descargar archivo XLSX con datos de asistentes e inasistentes

---

## 🔍 Troubleshooting Rápido

### Error: "Cannot GET /"
- [ ] Verificar que Apache está corriendo: `systemctl status apache2`
- [ ] Verificar que ProxyPass está configurado: `grep ProxyPass /etc/apache2/sites-available/comunidadcampesinatpct.com.conf`
- [ ] Verificar módulos: `a2enmod proxy proxy_http`

### Error: "502 Bad Gateway" / "Cannot connect to upstream"
- [ ] Verificar backend: `ss -tlnp | grep 8000`
- [ ] Iniciar backend: `systemctl restart comunidad-api`
- [ ] Ver logs: `journalctl -u comunidad-api -f`

### Error: "POST /auth/login" - No response
- [ ] Verificar Apache proxy: `apache2ctl configtest`
- [ ] Reiniciar Apache: `systemctl restart apache2`
- [ ] Verificar backend logs: `journalctl -u comunidad-api -n 20`

### Error: "SSL certificate not found"
- [ ] Generar certificado: `certbot certonly --standalone -d comunidadcampesinatpct.com`
- [ ] Verificar path en config: `/etc/letsencrypt/live/comunidadcampesinatpct.com/`

### Error: "ProxyPass not allowed here"
- [ ] Habilitar módulos: `a2enmod proxy proxy_http`
- [ ] Reiniciar Apache: `systemctl restart apache2`

---

## 📊 Comandos Útiles

```bash
# Estado de servicios
systemctl status apache2
systemctl status comunidad-api
systemctl status mysql

# Ver logs recientes (últimos 30 líneas)
tail -30 /var/log/apache2/comunidadcampesinatpct-error.log
journalctl -u comunidad-api -n 30

# Ver logs en tiempo real
journalctl -u comunidad-api -f
tail -f /var/log/apache2/comunidadcampesinatpct-error.log

# Reiniciar todos los servicios
systemctl restart apache2 comunidad-api mysql

# Verificar puertos
ss -tlnp | grep -E "80|443|8000"

# Revisar configuración Apache
apache2ctl configtest
apache2ctl -S
```

---

## ✅ Checklist Final

- [ ] Apache VirtualHost configurado para comunidadcampesinatpct.com
- [ ] Módulos proxy, rewrite, ssl habilitados en Apache
- [ ] Backend corriendo en puerto 8000
- [ ] Frontend compilado en `/var/www/comunidad/frontend/dist/`
- [ ] Usuario admin creado (DNI: 00000001)
- [ ] Script vincular_fotos.py ejecutado
- [ ] SSL certificates en lugar correcto
- [ ] Login funciona: https://comunidadcampesinatpct.com → login → dashboard
- [ ] Registro manual funciona: crear reunión → en_curso → registrar usuario → aparece en asistentes
- [ ] Sub-tabs funcionan: Registrados/Faltaron mostrar datos correctos
- [ ] Excel descarga correctamente con asistentes e inasistentes
- [ ] Logs sin errores en Apache y Backend

---

## 📞 En caso de problemas

Si después de seguir estos pasos algo no funciona:

1. **Verificar logs:**
   ```bash
   tail -50 /var/log/apache2/comunidadcampesinatpct-error.log
   journalctl -u comunidad-api -n 50
   ```

2. **Verificar conectividad:**
   ```bash
   curl -I http://127.0.0.1:8000/api/health
   curl -I http://localhost/api/health
   ```

3. **Verificar que el código está actualizado:**
   ```bash
   cd /var/www/comunidad
   git log -1 --oneline  # Debe ser "e7baa16 ahora si"
   ```

---

## 🎉 Cuando todo esté funcionando

1. Cambiar contraseña del usuario admin en la app
2. Importar usuarios de padrones/censos
3. Crear reuniones y comenzar a usar el sistema
4. Configurar respaldos periódicos de la base de datos
5. Monitorear logs regularmente

---

**Última actualización:** 2026-05-17  
**Commit actual:** e7baa16  
**Dominio:** comunidadcampesinatpct.com  
**Servidor:** 38.250.161.113
