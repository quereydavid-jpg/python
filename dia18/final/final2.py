num1 = (float(input("Ingrese el primer numero: ")))
num2 = (float(input("Ingrese el segundo numero: ")))

print(f"Suma: {num1 + num2}")
print(f"Resta: {num1 - num2}")
print(f"Multiplicacion: {num1 * num2}")
print(f"Division: {num1 / num2 if num2 != 0 else 'No se puede dividir entre 0'}")