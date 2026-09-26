numeros = []
for i in range(5):
    num = float(input(f"Ingrese el numero {i + 1}: "))
    numeros.append(num)

print("Lista de numeros:", numeros)
print("Suma de los numeros:", sum(numeros))
