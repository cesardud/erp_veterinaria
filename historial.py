import sqlite3
from datetime import datetime

#Registrar historial clínico
def registrar_historial(paciente_id,
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
    ultima_estetica,
    proxima_estetica
):
    conn = sqlite3.connect('veterinaria.db')
    cursor= conn.cursor()

    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    try:
        cursor.execute("""
            INSERT INTO historial_clinico (
                paciente_id,
                fecha,
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
                ultima_estetica,
                proxima_estetica
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            paciente_id,
            fecha_actual,
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
            ultima_estetica,
            proxima_estetica
        ))
        
        conn.commit()
        print("✅ Historial clínico registrado exitosamente")

    except Exception as e:
        print(f"Error al registrar el historial {e}")
    
    finally:
        conn.close()