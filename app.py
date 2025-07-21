import streamlit as st
import sqlite3
import pandas as pd
from inventario import registrar_venta
from inventario import registrar_compra
from historial import registrar_historial


st.title("🐾 ERP Veterinaria La Roncha")

# Conexión a la base de datos
conn = sqlite3.connect("veterinaria.db")

# --- Formulario de venta ---
st.subheader("💵 Registrar venta")

with st.form("venta_form"):
    codigo_v = st.text_input("Código de barras del producto (venta)", key = "venta_codigo")
    cantidad_v = st.number_input("Cantidad a vender", min_value=1, step=1, key = "venta_cantidad")
    enviar_v = st.form_submit_button("Vender")

    if enviar_v:
        try:
            registrar_venta(codigo_v, cantidad_v)
            st.success(f"✅ Venta registrada correctamente de {cantidad_v} unidades.")
        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")

# --- Formulario de compra ---
st.subheader("🛒 Registrar compra")

with st.form("compra_form"):
    codigo_c = st.text_input("Código de barras del producto (compra)", key = "compra_codigo")
    cantidad_c = st.number_input("Cantidad a comprar", min_value=1, step=1, key = "compra_cantidad")
    enviar_c = st.form_submit_button("Comprar")

    if enviar_c:
        try:
            registrar_compra(codigo_c, cantidad_c)
            st.success(f"✅ Compra registrada correctamente de {cantidad_c} unidades.")
        except Exception as e:
            st.error(f"❌ Ocurrió un error: {e}")

# --- Inventario actual ---
st.subheader("📋 Inventario actual")
df_inv = pd.read_sql_query("SELECT * FROM inventario", conn)
st.dataframe(df_inv)

# --- Transacciones ---
st.subheader("📊 Transacciones recientes")
df_trans = pd.read_sql_query("SELECT * FROM transacciones ORDER BY fecha DESC", conn)
st.dataframe(df_trans)

# --- Historial clínico---
st.subheader("🩺 Historial clínico")
df_historial= pd.read_sql_query("""
    SELECT hc.id_historial, hc.fecha, p.nombre AS paciente, hc.diagnostico, hc.tratamiento,
           hc.diarrea, hc.vomito, hc.estreñimiento, hc.perdida_apetito, hc.esterilizado,
           hc.pulgas, hc.enfermedad_actual, hc.toma_medicamentos,
           hc.ultima_estetica, hc.proxima_estetica
    FROM historial_clinico hc
    JOIN pacientes p ON hc.paciente_id = p.id_paciente
    ORDER BY hc.fecha DESC
""", conn)
st.dataframe(df_historial)

# --- Formulario historial ---
pacientes_df = pd.read_sql_query("SELECT id_paciente, nombre FROM pacientes", conn)
nombres_pacientes = pacientes_df["nombre"].tolist()

st.subheader("📝 Registrar historial clínico")

with st.form("form_historial"):
    nombre_seleccionado = st.selectbox("Paciente", nombres_pacientes)

    diagnostico = st.text_input("Diagnóstico")
    tratamiento = st.text_area("Tratamiento")
    notas = st.text_area("Notas")

    diarrea = st.selectbox("¿Tiene diarrea?", ["Sí", "No"])
    vomito = st.selectbox("¿Tiene vómito?", ["Sí", "No"])
    estreñimiento = st.selectbox("¿Tiene estreñimiento?", ["Sí", "No"])
    perdida_apetito = st.selectbox("¿Ha perdido el apetito?", ["Sí", "No"])
    esterilizado = st.selectbox("¿Está esterilizado?", ["Sí", "No"])
    pulgas = st.selectbox("¿Tiene pulgas?", ["Sí", "No"])

    enfermedad_actual = st.text_input("¿Padece alguna enfermedad actual?")
    enfermedad_pasada = st.text_input("¿Ha padecido alguna enfermedad importante?")
    toma_medicamentos = st.text_input("¿Toma algún medicamento?")
    cirugias = st.text_input("¿Le han practicado alguna cirugía?")

    ultima_estetica = st.date_input("Última visita a estética")
    proxima_estetica = st.date_input("Próxima visita a estética")

    enviar_hc = st.form_submit_button("Registrar historial")

    if enviar_hc:
        try:
            paciente_id = pacientes_df[pacientes_df["nombre"] == nombre_seleccionado]["id_paciente"].values[0]
            registrar_historial(
                paciente_id,
                diagnostico,
                tratamiento,
                notas,
                diarrea,
                vomito,
                estreñimiento,
                perdida_apetito,
                esterilizado,
                pulgas,
                enfermedad_actual,
                enfermedad_pasada,
                toma_medicamentos,
                cirugias,
                ultima_estetica.strftime("%Y-%m-%d"),
                proxima_estetica.strftime("%Y-%m-%d")
            )
            st.success("✅ Historial clínico registrado correctamente.")
        except Exception as e:
            st.error(f"❌ Error al registrar el historial: {e}")
 
 # --- Registrar nuevo paciente ---
st.subheader("🐶 Registrar paciente")

conn = sqlite3.connect("veterinaria.db")

# Obtener lista de clientes
clientes_df = pd.read_sql_query("SELECT id_cliente, nombre FROM clientes", conn)

if clientes_df.empty:
    st.warning("⚠️ No hay clientes registrados. Por favor, registra uno antes de añadir pacientes.")
else:
    with st.form("form_paciente"):
        nombre_pac = st.text_input("Nombre del paciente")
        especie = st.selectbox("Especie", ["Perro", "Gato", "Otro"])
        raza = st.text_input("Raza")
        sexo = st.selectbox("Sexo", ["Macho", "Hembra"])
        peso = st.number_input("Peso (kg)", min_value=0.0, step=0.01)
        color = st.text_input("Color")
        fecha_nacimiento = st.date_input("Fecha de nacimiento")
        fecha_registro = st.date_input("Fecha de registro")

        nombres_clientes = clientes_df["nombre"].tolist()
        cliente_seleccionado = st.selectbox("Cliente (propietario)", nombres_clientes)

        # CALCULAR ID del cliente seleccionado
        cliente_id = clientes_df[clientes_df["nombre"] == cliente_seleccionado]["id_cliente"].values[0]

        enviar_paciente = st.form_submit_button("Registrar paciente")

        if enviar_paciente:
            try:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT * FROM pacientes 
                    WHERE nombre = ? AND cliente_id = ?
                """, (nombre_pac, cliente_id))
                existe = cursor.fetchone()

                if existe:
                    st.warning("⚠️ Este paciente ya está registrado para este cliente.")
                else:
                    cursor.execute("""
                        INSERT INTO pacientes (nombre, especie, raza, sexo, peso, color, fecha_nacimiento, fecha_registro, cliente_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        nombre_pac,
                        especie,
                        raza,
                        sexo,
                        peso,
                        color,
                        fecha_nacimiento.strftime("%Y-%m-%d"),
                        fecha_registro.strftime("%Y-%m-%d"),
                        cliente_id
                    ))
                    conn.commit()
                    st.success(f"✅ Paciente '{nombre_pac}' registrado correctamente.")
            except Exception as e:
                st.error(f"❌ Error al registrar paciente: {e}")

conn.close()

# --- Mostrar pacientes registrados por cliente ---
st.subheader("📋 Pacientes registrados por cliente")

conn = sqlite3.connect("veterinaria.db")

# Selecciona cliente para consultar pacientes
cliente_filtrado = st.selectbox("Selecciona un cliente para ver sus pacientes", clientes_df["nombre"].tolist(), key="paciente_vista")
cliente_id_filtrado = clientes_df[clientes_df["nombre"] == cliente_filtrado]["id_cliente"].values[0]

# Obtener pacientes del cliente
pacientes_cliente = pd.read_sql_query("""
    SELECT nombre, especie, raza, sexo, peso, color, fecha_nacimiento
    FROM pacientes
    WHERE cliente_id = ?
""", conn, params=(cliente_id_filtrado,))

# Mostrar tabla o mensaje
if pacientes_cliente.empty:
    st.info("📭 Este cliente aún no tiene pacientes registrados.")
else:
    st.dataframe(pacientes_cliente)

conn.close()

# --- Registrar nuevo cliente ---
st.subheader("👤 Registrar cliente")

with st.form("form_cliente"):
    nombre_cli = st.text_input("Nombre del cliente")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo electrónico")

    enviar_cliente = st.form_submit_button("Registrar cliente")

    if enviar_cliente:
        try:
            conn = sqlite3.connect("veterinaria.db")
            cursor = conn.cursor()

            # Verificar si el cliente ya existe
            cursor.execute("SELECT * FROM clientes WHERE nombre = ? AND telefono = ?", (nombre_cli, telefono))
            existe = cursor.fetchone()

            if existe:
                st.warning("⚠️ Este cliente ya está registrado.")
            else:
                cursor.execute("""
                    INSERT INTO clientes (nombre, telefono, correo)
                    VALUES (?, ?, ?)
                """, (nombre_cli, telefono, correo))
                conn.commit()
                st.success(f"✅ Cliente '{nombre_cli}' registrado correctamente.")

            conn.close()

        except Exception as e:
            st.error(f"❌ Error al registrar cliente: {e}")





