import pymysql

conn = pymysql.connect(host='localhost', user='root', db='comunidad')
cursor = conn.cursor()

try:
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='comunidad' AND TABLE_NAME='padron_eleccion'")
    if cursor.fetchone():
        print('[OK] Tabla padron_eleccion ya existe')
    else:
        print('[INFO] Creando tabla padron_eleccion...')
        cursor.execute("""
            CREATE TABLE padron_eleccion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                eleccion_id INT NOT NULL,
                usuario_id INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(eleccion_id, usuario_id),
                FOREIGN KEY(eleccion_id) REFERENCES elecciones(id) ON DELETE CASCADE,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        """)
        print('[OK] Tabla padron_eleccion creada')
        conn.commit()

finally:
    cursor.close()
    conn.close()
