dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
ventas = [1200,1450, 980,1600,1750,2100,1330]

total = sum(ventas)

promedio = sum(ventas) / len(ventas)

indice_mayor = ventas.index(max(ventas))
print(f"total de ventas de la semana: {total}")
print(f"promedio de ventas diarias: {promedio: .2f}")
print(f"el dia con mas ventas: {dias[indice_mayor]}")
