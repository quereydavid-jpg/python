producto = {
    "nombre" : "arroz 1 kg",
    "precio" : 6500,
    "stock"  : 120
}

cantidad_vendida = 15
producto["stock"] = producto["stock"] - cantidad_vendida
total = producto["precio"] * cantidad_vendida

print(f"venta registrada: {cantidad_vendida} de unid. de {producto["nombre"]}")
print(f"monto total: {total} gs.")
print(f"stock restante: {producto["stock"]} unidades.")