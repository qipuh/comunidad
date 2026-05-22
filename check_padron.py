#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')

from app.db.database import SessionLocal
from app.models.usuario import Usuario

db = SessionLocal()

# Obtener los primeros 122 usuarios ordenados por ID
usuarios = db.query(Usuario).order_by(Usuario.id).limit(122).all()

print(f"Total de usuarios encontrados: {len(usuarios)}")

# Contar cuántos tienen num_padron
con_padron = sum(1 for u in usuarios if u.num_padron)
sin_padron = len(usuarios) - con_padron

print(f"Usuarios CON num_padron: {con_padron}")
print(f"Usuarios SIN num_padron: {sin_padron}")

# Mostrar los primeros 10
print("\nPrimeros 10 usuarios:")
for u in usuarios[:10]:
    print(f"  ID: {u.id}, DNI: {u.numero_dni}, Nombre: {u.nombres}, num_padron: {u.num_padron}")

# Mostrar los últimos 10
print("\nÚltimos 10 usuarios (índices 112-122):")
for u in usuarios[-10:]:
    print(f"  ID: {u.id}, DNI: {u.numero_dni}, Nombre: {u.nombres}, num_padron: {u.num_padron}")

# Buscar específicamente el 04412242
usuario_especifico = db.query(Usuario).filter(Usuario.numero_dni == "04412242").first()
if usuario_especifico:
    print(f"\nUsuario con DNI 04412242:")
    print(f"  ID: {usuario_especifico.id}")
    print(f"  Nombre: {usuario_especifico.nombres}")
    print(f"  num_padron: {usuario_especifico.num_padron}")
else:
    print(f"\nNo se encontró usuario con DNI 04412242")

# Buscar números de padron que contengan los dígitos específicos
print(f"\nEjemplos de usuarios con num_padron:")
usuarios_con_padron = db.query(Usuario).filter(Usuario.num_padron != None).filter(Usuario.num_padron != '').limit(10).all()
if usuarios_con_padron:
    for u in usuarios_con_padron:
        print(f"  ID: {u.id}, num_padron: {u.num_padron}, DNI: {u.numero_dni}")
else:
    print("No hay usuarios con num_padron establecido")

db.close()
