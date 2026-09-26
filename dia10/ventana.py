import tkinter as tk
import os

def ejecutar():
    os.system(campo.get())

ventana = tk.Tk()
ventana.title("SNPP")
ventana.geometry("300x100")

campo = tk.Entry(ventana)
campo.pack(pady=10)

boton = tk.Button(ventana, text = "Aceptar", command=ejecutar)
boton.pack(pady = 5)

ventana.mainloop()
