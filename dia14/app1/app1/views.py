from django.http import HttpResponse

lista = ["fiorela","camila", "vanessa","sofia"]

def listar(request):
    return HttpResponse(lista)

from django.http import HttpResponse

def saludar(request):

    texto = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Curso de Python con Django</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f4f7;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .mensaje {
                background-color: white;
                padding: 40px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }

            h1 {
                color: #1e3a8a;
                margin-bottom: 15px;
            }

            p {
                color: #555;
                font-size: 18px;
            }
        </style>
    </head>

    <body>
        <div class="mensaje">
            <h1>🐍 ¡Bienvenidos!</h1>
            <p>Hola, bienvenidos al <strong>curso de Python con Django</strong>.</p>
        </div>
    </body>
    </html>
    """

    return HttpResponse(texto)

def saludar_nombre(request, nombre):
    texto = f"Hola {nombre}"
    return HttpResponse(texto)

def factorial(request, numero):
    resultado = 1
    for i in range(1, numero + 1):
        resultado = resultado * i

    return HttpResponse(f"El factorial de {numero} es {resultado}")

from django.shortcuts import render
def inicio_render(request):
    return render(request, 'app1/inicio.html')