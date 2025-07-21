from historial import registrar_historial

# Cambia este ID por uno que exista en tu base
paciente_id = 11

registrar_historial(
    paciente_id=paciente_id,
    diagnostico="Pérdida de apetito y vómito leve",
    tratamiento="Omeprazol y dieta controlada",
    notas="Se recomienda evaluación en 3 días",
    diarrea="No",
    vomito="Sí",
    estreñimiento="No",
    perdida_apetito="Sí",
    esterilizado="No",
    pulgas="No",
    enfermedad_actual="Gastritis leve",
    enfermedad_pasada="Ninguna",
    toma_medicamentos="No",
    cirugias="No",
    ultima_estetica="2024-06-01",
    proxima_estetica="2024-08-15"
)
