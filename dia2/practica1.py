saldo_disponible = 450000
monto_transferencia = int(input("Ingrese monto a transferir: "))

if monto_transferencia > saldo_disponible: 
 print("saldo insuficiente")
else:

 saldo_disponible = saldo_disponible - monto_transferencia
 print("transferencia realizada con exito")
 print("su actual es: " + str(saldo_disponible))
