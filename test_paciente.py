import sqlite3
from datetime import datetime

DB = "veterinaria.db"

def get_or_create_cliente(nombre, telefono=None, correo=None, direccion=None):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    # ¿Ya existe?
    cursor.execute("SELECT id_cliente FROM clientes WHERE nombre = ?", (nombre,))
    row = cursor.fetchone()
    if row:
        conn.close()
        return row[0]
    # Crear
    cursor.execute("""
        INSERT INTO clientes (nombre, telefono, correo, direccion)
        VALUES (?, ?, ?, ?)
    """, (nombre, telefono, correo, direccion))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return nuevo_id

def crear_paciente(nombre, especie, raza, fecha_nacimiento, cliente_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    fecha_registro = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO pacientes (nombre, especie, raza, fecha_nacimiento, fecha_registro, cliente_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, especie, raza, fecha_nacimiento, fecha_registro, cliente_id))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return nuevo_id

if __name__ == "__main__":
    # Crear / obtener cliente
    cliente_id = get_or_create_cliente(
        nombre="Cliente Demo",
        telefono="555-123-4567",
        correo="demo@correo.com",
        direccion="Calle Falsa 123"
    )

    # Crear paciente asociado
    paciente_id = crear_paciente(
        nombre="Luna",
        especie="Perro",
        raza="Labrador",
        fecha_nacimiento="2022-05-10",  # YYYY-MM-DD
        cliente_id=cliente_id
    )

    print(f"✅ Cliente ID: {cliente_id} | Paciente ID: {paciente_id}")
