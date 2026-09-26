#ecuacion cuadratica
print("resolver ecuaciones con la ec. cuadratica")
a = float(input("ingrese el coeficiente de x2"))
b = float(input("ingrese el coeficientede x"))
c = float(input("ingrese el termino independiente"))

x1 = (-b + (b**2 -4 * a * c)**(0.5))/ (2*a)
x2 = (-b - (b**2 -4 * a * c)**(0.5))/ (2*a)

print (f"solucion x1: {x1}, {x2}" )