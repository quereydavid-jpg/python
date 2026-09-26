# programa para calcular IMC
print ("Calculadora de IMC")
peso = float(input("Ingrese su peso en kg: "))
estatura = float(input("Ingrese su estatura en metros: "))

imc = peso / (estatura * estatura)

print("Tu IMC es: " + str(imc))