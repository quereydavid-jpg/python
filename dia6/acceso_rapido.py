import os

while True:
    print(f"1. bloc \n2. calculadora \n3. apagar \n4.cancelar apagado \n0.salir")
    resp = input("elige: ")
    if resp == "1":
        os.system("notepad")
    elif resp == "2":
        os.system("calc")
    elif resp == "3":
        os.system("shutdown -s -t 300")
    elif resp == "4":
        os.system("shutdown -a")
    elif resp == "0":
        break
    else:
        print("no se entiende la orden")