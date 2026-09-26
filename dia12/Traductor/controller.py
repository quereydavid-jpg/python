from model import ModeloTraduccion

class ControladorTraduccion:
    def __init__(self):
        self.modelo = ModeloTraduccion()

    def cargar_palabra(self, esp, ing):
        self.modelo.agregar_palabra(esp, ing)

    def traducir(self, palabra):
        resultado = self.modelo.buscar_palabra(palabra)
        if resultado is not None:
            return resultado[2]

        return None

