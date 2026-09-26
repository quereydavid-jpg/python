import google.generativeai as genai

genai.configure(api_key= "AQ.Ab8RN6J_n8HbMdFXGX4JwxmQJuHQNpCMXiICHG-mZgXFZ7HNng")
modelo = genai.GenerativeModel("gemini-3.6-flash")

class ChatBot:
    def __init__(self, nombre):
        self.nombre = nombre
        self.base_conocimiento = {
            "hola": "Hola, ¿qué puedo hacer por ti?",
        }
        self.historial = []

    def responder(self, mensaje):
        mensaje = mensaje.lower().strip()
        self.historial.append(mensaje)


        for clave, respuesta in self.base_conocimiento.items():
            if clave in mensaje:
                return respuesta

        try:
            resultado = modelo.generate_content(mensaje)
            return resultado.text
        except Exception:
            return "No entendi tu mensaje, ¿Podrias reformularlo?"

    def agregar_conocimiento(self, clave, respuesta):
        self.base_conocimiento[clave.lower()] = respuesta


def main():
    bot = ChatBot("Miki")
    print(f"{bot.nombre}: Hola, En que puedo ayudarte?")

    while True:
        entrada = input("Tú: ")

        if entrada.lower().strip() == "salir":
            print("Hasta luego")
            break

        respuesta = bot.responder(entrada)
        print(f"{bot.nombre}: {respuesta}")

if __name__ == "__main__":
    main()          

    