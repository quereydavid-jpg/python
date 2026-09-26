productos = ["Arroz", "Aceite", "Fideo", "Azucar"]

with open("archivo.txt", "a") as archivo:
    for p in productos:
        archivo.write(f"{p} \n")

print("Lista de productos desde el archivo")
with open("archivo.txt", "r") as archivo:
    lineas = archivo.readlines()

    for p in lineas:
        print(f"{p.strip()}")
