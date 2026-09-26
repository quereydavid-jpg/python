#control de temperatura
temp = 25
while temp > 0:
    temp = float(input("ingrese temp: "))
    if temp >= 28:
        print("encender AA")
    elif temp <= 17:
        print("encender la calefaccion")
    else:
        print("temperatura agradable")