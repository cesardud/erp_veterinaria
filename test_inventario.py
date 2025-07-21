from inventario import agregar_producto, registrar_compra, registrar_venta

# Solo agregamos el producto si aún no existe
agregar_producto(
    codigo_barras="1112223334445",
    nombre="Desparasitante Felino",
    descripcion="Pastillas para desparasitar gatos",
    stock=10,
    precio_unitario=200.00,
    costo_unitario=120.00,
    tipo="medicina"
)

# Simulamos una compra de 5 unidades más
registrar_compra("1112223334445", 5)

# Simulamos una venta de 3 unidades
registrar_venta("1112223334445", 3)