def calcular_cuota(capital, tasa_anual, cantidad_cuota):
    interes_total = capital * (tasa_anual/100)
    monto_total = capital + interes_total
    cuota = monto_total / cantidad_cuota
    return cuota

while True:
    print("calculadora de cuotas")
    c = int(input("ingrese en monto a prestar: "))
    t = float(input("ingrese la tasa anual"))
    cu = int(input("ingrese la cantidad de cuotas"))

    print(f"su cuota mensual sera de: {calcular_cuota(c,t,cu)}")