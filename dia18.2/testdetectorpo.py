from urllib import request
from urllib.error import URLError
lpo = ["coño", "bobo", "culiao", "pinche", "estupido", "estupida"]

def verificar_web(url):
    try:
        f = request.urlopen(url)
    except URLError:
        return('¡La url ' + url + ' no existe!')
    else:
        aux = f.read()
        contenido = aux.split()
        palabras_encontradas = []
        cantidad_po = 0
        for l in lpo:
            for con in contenido:
                if l in con.decode() :
                    palabras_encontradas.append(l)
        return palabras_encontradas

url = 'https://es.scribd.com/doc/291603527/Diccionario-de-Insultos'
print("\n------------------------\n")
print("\nInforme de sitio:")
print(verificar_web(url))

