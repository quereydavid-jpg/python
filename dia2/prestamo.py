ingreso_mensual = 4800000
historial_positivo = True
deuda_actual = 1200000
if historial_positivo and ingreso_mensual >= deuda_actual * 3:
    print("prestamo aprobado")
elif historial_positivo:
    print("aprobado con monto reducido")
else:
    print("prestamo rechazado")
