import sqlite3
from datetime import datetime

# Agregar producto a inventario
def agregar_producto(codigo_barras, nombre, descripcion, stock, precio_unitario, costo_unitario, tipo):
    conn = sqlite3.connect("veterinaria.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO inventario (codigo_barras, nombre, descripcion, stock, precio_unitario, costo_unitario, tipo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (codigo_barras, nombre, descripcion, stock, precio_unitario, costo_unitario, tipo))

        conn.commit()
        print("✅ Producto agregado correctamente.")

    except sqlite3.IntegrityError:
        print("⚠️ El código de barras ya existe. No se puede duplicar.")
    
    finally:
        conn.close()

# Actualizar stock
def actualizar_stock(codigo_barras, cantidad):
    conn = sqlite3.connect("veterinaria.db")
    cursor = conn.cursor()

    cursor.execute("SELECT stock FROM inventario WHERE codigo_barras = ?", (codigo_barras,))
    resultado = cursor.fetchone()

    if resultado:
        stock_actual = resultado[0]
        nuevo_stock = stock_actual + cantidad

        if nuevo_stock < 0:
            print("❌ No hay suficiente stock para realizar esta venta.")
        else:
            cursor.execute("UPDATE inventario SET stock = ? WHERE codigo_barras = ?", (nuevo_stock, codigo_barras))
            conn.commit()
            print(f"✅ Stock actualizado. Nuevo stock: {nuevo_stock}")
    else:
        print("❌ Producto no encontrado. No se pudo actualizar el stock.")

    conn.close()

#Regustrar transacción
def registrar_transaccion(tipo, descripcion, monto, producto_id, cantidad):
    conn = sqlite3.connect("veterinaria.db")
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO transacciones (fecha, tipo, descripcion, monto, producto_id, cantidad)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (fecha, tipo, descripcion, monto, producto_id, cantidad))

    conn.commit()
    conn.close()
    print(f"📦 Transacción registrada: {tipo.upper()} de {cantidad} unidades.")

# Registrar compra
def registrar_compra(codigo_barras, cantidad_comprada):
    conn = sqlite3.connect("veterinaria.db")
    cursor = conn.cursor()

    # Obtener costo unitario
    cursor.execute("SELECT nombre, costo_unitario FROM inventario WHERE codigo_barras = ?", (codigo_barras,))
    resultado = cursor.fetchone()

    if resultado:
        nombre_producto, costo_unitario = resultado
        total = costo_unitario * cantidad_comprada

        actualizar_stock(codigo_barras, cantidad_comprada)
        registrar_transaccion("egreso", f"Compra de {nombre_producto}", total, codigo_barras, cantidad_comprada)
    else:
        print("❌ Producto no encontrado para registrar la compra.")

    conn.close()

#Registrar venta
def registrar_venta(codigo_barras, cantidad_vendida):
    conn = sqlite3.connect("veterinaria.db")
    cursor = conn.cursor()

    # Obtener precio unitario
    cursor.execute("SELECT nombre, precio_unitario FROM inventario WHERE codigo_barras = ?", (codigo_barras,))
    resultado = cursor.fetchone()

    if resultado:
        nombre_producto, precio_unitario = resultado
        total = precio_unitario * cantidad_vendida

        actualizar_stock(codigo_barras, -cantidad_vendida)
        registrar_transaccion("ingreso", f"Venta de {nombre_producto}", total, codigo_barras, cantidad_vendida)
    else:
        print("❌ Producto no encontrado para registrar la venta.")

    conn.close()