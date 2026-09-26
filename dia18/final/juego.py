import pygame
import random

pygame.init()

# -------------------------
# CONFIGURACIÓN
# -------------------------
ANCHO = 600
ALTO = 400

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Obstáculos")

reloj = pygame.time.Clock()

# Colores
NEGRO = (30, 30, 30)
BLANCO = (255, 255, 255)
AZUL = (50, 150, 255)
ROJO = (200, 50, 50)
VERDE = (0, 200, 0)
VERDE_PUNTO = (0, 255, 0)

fuente = pygame.font.SysFont(None, 30)
fuente_grande = pygame.font.SysFont(None, 70)

# -------------------------
# JUGADOR
# -------------------------
radio = 15

x_inicial = ANCHO // 2
y_inicial = ALTO - 40

x = x_inicial
y = y_inicial

velocidad = 5

# -------------------------
# META
# -------------------------
meta_ancho = 100
meta_alto = 30

meta_x = (ANCHO - meta_ancho) // 2
meta_y = 10

# -------------------------
# VARIABLES DEL JUEGO
# -------------------------
nivel = 1
vidas = 3
puntos = 0

# -------------------------
# CREAR OBSTÁCULOS
# -------------------------
def crear_obstaculos(nivel):

    obstaculos = []

    cantidad = 3 + nivel

    for i in range(cantidad):

        ancho = random.randint(80, 150)

        y = 60 + i * 65

        if y > 330:
            y = random.randint(60, 330)

        x = random.randint(0, ANCHO - ancho)

        velocidad_obstaculo = random.randint(2, 4) + nivel

        if random.choice([True, False]):
            velocidad_obstaculo *= -1

        obstaculos.append({
            "x": x,
            "y": y,
            "ancho": ancho,
            "alto": 20,
            "velocidad": velocidad_obstaculo
        })

    return obstaculos


# -------------------------
# CREAR PUNTOS VERDES
# -------------------------
def crear_puntos():

    puntos_verdes = []

    for i in range(5):

        puntos_verdes.append({
            "x": random.randint(30, ANCHO - 30),
            "y": random.randint(50, ALTO - 30)
        })

    return puntos_verdes


# Crear elementos iniciales
obstaculos = crear_obstaculos(nivel)
puntos_verdes = crear_puntos()

radio_punto = 8

# -------------------------
# FUNCIÓN PARA REINICIAR
# -------------------------
def reiniciar_juego():

    global x, y
    global nivel, vidas, puntos
    global obstaculos, puntos_verdes

    x = x_inicial
    y = y_inicial

    nivel = 1
    vidas = 3
    puntos = 0

    obstaculos = crear_obstaculos(nivel)
    puntos_verdes = crear_puntos()


# -------------------------
# ESTADO DEL JUEGO
# -------------------------
game_over = False

corriendo = True

while corriendo:

    # -------------------------
    # EVENTOS
    # -------------------------
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            corriendo = False

    # =================================================
    # GAME OVER
    # =================================================
    if game_over:

        ventana.fill(NEGRO)

        texto_game_over = fuente_grande.render(
            "GAME OVER",
            True,
            BLANCO
        )

        texto_reinicio = fuente.render(
            "Reiniciando el juego...",
            True,
            BLANCO
        )

        ventana.blit(
            texto_game_over,
            (
                ANCHO // 2 - texto_game_over.get_width() // 2,
                140
            )
        )

        ventana.blit(
            texto_reinicio,
            (
                ANCHO // 2 - texto_reinicio.get_width() // 2,
                220
            )
        )

        pygame.display.flip()

        # Esperar 3 segundos
        pygame.time.delay(3000)

        reiniciar_juego()

        game_over = False

        continue

    # =================================================
    # MOVIMIENTO DEL JUGADOR
    # =================================================

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        x -= velocidad

    if teclas[pygame.K_RIGHT]:
        x += velocidad

    if teclas[pygame.K_UP]:
        y -= velocidad

    if teclas[pygame.K_DOWN]:
        y += velocidad

    # -------------------------
    # LIMITAR AL JUGADOR
    # -------------------------

    if x - radio < 0:
        x = radio

    if x + radio > ANCHO:
        x = ANCHO - radio

    if y - radio < 0:
        y = radio

    if y + radio > ALTO:
        y = ALTO - radio

    # =================================================
    # MOVIMIENTO DE OBSTÁCULOS
    # =================================================

    for obstaculo in obstaculos:

        obstaculo["x"] += obstaculo["velocidad"]

        # Borde derecho
        if obstaculo["x"] + obstaculo["ancho"] >= ANCHO:

            obstaculo["x"] = ANCHO - obstaculo["ancho"]

            obstaculo["velocidad"] *= -1

        # Borde izquierdo
        if obstaculo["x"] <= 0:

            obstaculo["x"] = 0

            obstaculo["velocidad"] *= -1

    # =================================================
    # RECTÁNGULO DEL JUGADOR
    # =================================================

    jugador_rect = pygame.Rect(
        x - radio,
        y - radio,
        radio * 2,
        radio * 2
    )

    # =================================================
    # COLISIÓN CON OBSTÁCULOS
    # =================================================

    colision = False

    for obstaculo in obstaculos:

        obstaculo_rect = pygame.Rect(
            obstaculo["x"],
            obstaculo["y"],
            obstaculo["ancho"],
            obstaculo["alto"]
        )

        if jugador_rect.colliderect(obstaculo_rect):

            colision = True
            break

    # Si choca
    if colision:

        vidas -= 1

        # Volver al inicio
        x = x_inicial
        y = y_inicial

        # Si se quedan sin vidas
        if vidas <= 0:

            game_over = True

    # =================================================
    # RECOGER PUNTOS
    # =================================================

    puntos_recogidos = []

    for punto in puntos_verdes:

        distancia_x = x - punto["x"]
        distancia_y = y - punto["y"]

        distancia = (
            distancia_x ** 2 +
            distancia_y ** 2
        ) ** 0.5

        if distancia < radio + radio_punto:

            puntos += 10

            puntos_recogidos.append(punto)

    # Eliminar puntos recogidos
    for punto in puntos_recogidos:

        puntos_verdes.remove(punto)

    # =================================================
    # META
    # =================================================

    meta_rect = pygame.Rect(
        meta_x,
        meta_y,
        meta_ancho,
        meta_alto
    )

    if jugador_rect.colliderect(meta_rect):

        # Pasar al siguiente nivel
        nivel += 1

        # Volver al inicio
        x = x_inicial
        y = y_inicial

        # Si terminó el nivel 5
        if nivel > 5:

            nivel = 1

            # Reiniciar obstáculos
            obstaculos = crear_obstaculos(nivel)

            puntos_verdes = crear_puntos()

        else:

            # Crear nuevos obstáculos
            obstaculos = crear_obstaculos(nivel)

            # Crear nuevos puntos
            puntos_verdes = crear_puntos()

    # =================================================
    # DIBUJAR FONDO
    # =================================================

    ventana.fill(NEGRO)

    # =================================================
    # DIBUJAR META
    # =================================================

    pygame.draw.rect(
        ventana,
        VERDE,
        meta_rect
    )

    texto_meta = fuente.render(
        "META",
        True,
        BLANCO
    )

    ventana.blit(
        texto_meta,
        (
            meta_x + 28,
            meta_y + 3
        )
    )

    # =================================================
    # DIBUJAR OBSTÁCULOS
    # =================================================

    for obstaculo in obstaculos:

        pygame.draw.rect(
            ventana,
            ROJO,
            (
                obstaculo["x"],
                obstaculo["y"],
                obstaculo["ancho"],
                obstaculo["alto"]
            )
        )

    # =================================================
    # DIBUJAR PUNTOS VERDES
    # =================================================

    for punto in puntos_verdes:

        pygame.draw.circle(
            ventana,
            VERDE_PUNTO,
            (
                punto["x"],
                punto["y"]
            ),
            radio_punto
        )

    # =================================================
    # DIBUJAR JUGADOR
    # =================================================

    pygame.draw.circle(
        ventana,
        AZUL,
        (x, y),
        radio
    )

    # =================================================
    # INFORMACIÓN
    # =================================================

    texto_nivel = fuente.render(
        "Nivel: " + str(nivel) + " / 5",
        True,
        BLANCO
    )

    texto_puntos = fuente.render(
        "Puntos: " + str(puntos),
        True,
        BLANCO
    )

    texto_vidas = fuente.render(
        "Vidas: " + str(vidas),
        True,
        BLANCO
    )

    ventana.blit(
        texto_nivel,
        (10, 10)
    )

    ventana.blit(
        texto_puntos,
        (10, 40)
    )

    ventana.blit(
        texto_vidas,
        (10, 70)
    )

    # =================================================
    # ACTUALIZAR PANTALLA
    # =================================================

    pygame.display.flip()

    reloj.tick(60)


pygame.quit()