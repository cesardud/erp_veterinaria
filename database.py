import sqlite3

def crear_tablas():
    conn = sqlite3.connect("veterinaria.db")
    cursor = conn.cursor()

    # Tabla de inventario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            codigo_barras TEXT PRIMARY KEY,
            nombre TEXT,
            descripcion TEXT,
            stock INTEGER,
            precio_unitario REAL,
            costo_unitario REAL,
            tipo TEXT
        )
    ''')

    # Tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT,
            correo TEXT,
            direccion TEXT
        )
    ''')

    # Tabla de pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            especie TEXT,
            raza TEXT,
            sexo TEXT,
            peso INTEGER,
            color TEXT,
            fecha_nacimiento TEXT,
            fecha_registro TEXT,
            cliente_id INTEGER,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id_cliente)
        )
    ''')

    #Tabla historial clínico
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS historial_clinico (
        id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        fecha TEXT,
        diagnostico TEXT,
        tratamiento TEXT,
        notas TEXT,
        
        diarrea TEXT,
        vomito TEXT,
        estreñimiento TEXT,
        perdida_apetito TEXT,
        esterilizado TEXT,
        pulgas TEXT,
        
        enfermedad_actual TEXT,
        enfermedad_pasada TEXT,
        toma_medicamentos TEXT,
        cirugias TEXT,
        
        ultima_estetica TEXT,
        proxima_estetica TEXT,
        
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id_paciente)
    )
''')

    # Tabla de transacciones (ingresos y egresos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacciones (
            id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            tipo TEXT,
            descripcion TEXT,
            monto REAL,
            producto_id TEXT,
            cantidad INTEGER,
            FOREIGN KEY(producto_id) REFERENCES inventario(codigo_barras)
        )
    ''')


    conn.commit()
    conn.close()

# Ejecutar función cuando se corra este archivo
if __name__ == "__main__":
    crear_tablas()
    print("Base de datos creada correctamente.")
