import pygame
import random
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva los obstáculos - Pygame Pro")

# Colores (RGB)
BLANCO = (255, 255, 255)
AZUL = (50, 150, 250)
ROJO = (220, 60, 60)
VERDE = (46, 204, 113)
AMARILLO = (241, 196, 15)
NEGRO = (20, 20, 20)
GRIS = (200, 200, 200)

# Reloj y fuente
reloj = pygame.time.Clock()
FPS = 60
fuente = pygame.font.SysFont(None, 36)
fuente_grande = pygame.font.SysFont(None, 48)

# Archivo para guardar el puntaje
ARCHIVO_PUNTAJE = "mejor_puntaje.txt"

def cargar_mejor_puntaje():
    if os.path.exists(ARCHIVO_PUNTAJE):
        try:
            with open(ARCHIVO_PUNTAJE, "r") as f:
                return int(f.read().strip())
        except ValueError:
            return 0
    return 0

def guardar_mejor_puntaje(puntaje):
    actual = cargar_mejor_puntaje()
    if puntaje > actual:
        with open(ARCHIVO_PUNTAJE, "w") as f:
            f.write(str(puntaje))

def pantalla_inicio():
    mejor_puntaje = cargar_mejor_puntaje()
    while True:
        pantalla.fill(NEGRO)
        
        titulo = fuente_grande.render("ESQUIVA LOS OBSTÁCULOS", True, AZUL)
        texto_record = fuente.render(f"Mejor Puntaje: {mejor_puntaje}", True, VERDE)
        texto_instrucciones = fuente.render("Usa las Flechas o A/D para moverte", True, BLANCO)
        texto_jugar = fuente.render("Presiona 'ESPACIO' para Comenzar", True, GRIS)

        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 3 - 50))
        pantalla.blit(texto_record, (ANCHO // 2 - texto_record.get_width() // 2, ALTO // 3 + 20))
        pantalla.blit(texto_instrucciones, (ANCHO // 2 - texto_instrucciones.get_width() // 2, ALTO // 2 + 20))
        pantalla.blit(texto_jugar, (ANCHO // 2 - texto_jugar.get_width() // 2, ALTO // 2 + 80))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    main_juego()

def main_juego():
    # Variables del jugador
    jugador_ancho = 80
    jugador_alto = 20
    jugador_x = ANCHO // 2 - jugador_ancho // 2
    jugador_y = ALTO - 50
    jugador_velocidad_base = 7
    vidas = 3

    # Sistema de invulnerabilidad (en milisegundos)
    invulnerable = False
    tiempo_invulnerable = 0
    duracion_invulnerabilidad = 1000  # 1 segundo

    # Power-up Verde (Ralentizar bloques)
    ralentizado = False
    tiempo_ralentizado = 0
    duracion_ralentizado = 3000

    # Power-up Amarillo (Doble velocidad de movimiento)
    rapido = False
    tiempo_rapido = 0
    duracion_rapido = 3000

    # Power-up Blanco (Destruir bloques)
    destructor = False
    tiempo_destructor = 0
    duracion_destructor = 3000

    # Listas de elementos
    obstaculos = []
    power_ups_verdes = []
    power_ups_amarillos = []
    power_ups_blancos = []
    
    # Variables de dificultad y tiempo
    tiempo_transcurrido = 0
    puntuacion = 0
    velocidad_obstaculo_base = 5
    frecuencia_spawn = 45
    contador_spawn = 0
    contador_pu_verde = 0
    contador_pu_amarillo = 0
    contador_pu_blanco = 0

    jugando = True
    while jugando:
        tiempo_actual = pygame.time.get_ticks()

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Velocidad del jugador
        velocidad_jugador_actual = jugador_velocidad_base * 2 if rapido else jugador_velocidad_base

        # Controles del jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jugador_x -= velocidad_jugador_actual
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jugador_x += velocidad_jugador_actual

        # Limitar al jugador dentro de la pantalla
        if jugador_x < 0:
            jugador_x = 0
        elif jugador_x > ANCHO - jugador_ancho:
            jugador_x = ANCHO - jugador_ancho

        # Control de tiempos de Power-ups y Estados
        if invulnerable and tiempo_actual - tiempo_invulnerable > duracion_invulnerabilidad:
            invulnerable = False
        if ralentizado and tiempo_actual - tiempo_ralentizado > duracion_ralentizado:
            ralentizado = False
        if rapido and tiempo_actual - tiempo_rapido > duracion_rapido:
            rapido = False
        if destructor and tiempo_actual - tiempo_destructor > duracion_destructor:
            destructor = False

        # Incrementar dificultad y puntuación
        tiempo_transcurrido += 1
        puntuacion = tiempo_transcurrido // 10
        velocidad_actual = velocidad_obstaculo_base + (tiempo_transcurrido // 250)

        if ralentizado:
            velocidad_actual = max(2, velocidad_actual // 2)

        # Generar obstáculos
        contador_spawn += 1
        intervalo_actual = max(15, frecuencia_spawn - (tiempo_transcurrido // 150))
        if contador_spawn >= intervalo_actual:
            obs_ancho = random.randint(30, 80)
            obs_alto = 20
            obs_x = random.randint(0, ANCHO - obs_ancho)
            obstaculos.append(pygame.Rect(obs_x, -obs_alto, obs_ancho, obs_alto))
            contador_spawn = 0

        # Generar Power-up Verde (Ralentizar)
        contador_pu_verde += 1
        if contador_pu_verde >= 350:
            pu_ancho, pu_alto = 25, 25
            pu_x = random.randint(0, ANCHO - pu_ancho)
            power_ups_verdes.append(pygame.Rect(pu_x, -pu_alto, pu_ancho, pu_alto))
            contador_pu_verde = 0

        # Generar Power-up Amarillo (Velocidad)
        contador_pu_amarillo += 1
        if contador_pu_amarillo >= 450:
            pu_ancho, pu_alto = 25, 25
            pu_x = random.randint(0, ANCHO - pu_ancho)
            power_ups_amarillos.append(pygame.Rect(pu_x, -pu_alto, pu_ancho, pu_alto))
            contador_pu_amarillo = 0

        # Generar Power-up Blanco (Destructor)
        contador_pu_blanco += 1
        if contador_pu_blanco >= 600:
            pu_ancho, pu_alto = 25, 25
            pu_x = random.randint(0, ANCHO - pu_ancho)
            power_ups_blancos.append(pygame.Rect(pu_x, -pu_alto, pu_ancho, pu_alto))
            contador_pu_blanco = 0

        # Mover obstáculos
        for obs in obstaculos[:]:
            obs.y += velocidad_actual
            if obs.y > ALTO:
                obstaculos.remove(obs)

        # Mover power-ups
        for pu in power_ups_verdes[:]:
            pu.y += 4
            if pu.y > ALTO:
                power_ups_verdes.remove(pu)

        for pu in power_ups_amarillos[:]:
            pu.y += 4
            if pu.y > ALTO:
                power_ups_amarillos.remove(pu)

        for pu in power_ups_blancos[:]:
            pu.y += 4
            if pu.y > ALTO:
                power_ups_blancos.remove(pu)

        # Rectángulo del jugador
        rect_jugador = pygame.Rect(jugador_x, jugador_y, jugador_ancho, jugador_alto)

        # Colisiones con obstáculos
        for obs in obstaculos[:]:
            if rect_jugador.colliderect(obs):
                if destructor:
                    # Si tiene el modo destructor activo, destruye el bloque al tocarlo y da puntos extra
                    obstaculos.remove(obs)
                    puntuacion += 10
                elif not invulnerable:
                    # Si no, pierde vida
                    vidas -= 1
                    invulnerable = True
                    tiempo_invulnerable = tiempo_actual
                    obstaculos.remove(obs)
                    if vidas <= 0:
                        jugando = False

        # Colisiones con Power-ups verdes
        for pu in power_ups_verdes[:]:
            if rect_jugador.colliderect(pu):
                puntuacion += 50
                tiempo_transcurrido += 500
                ralentizado = True
                tiempo_ralentizado = tiempo_actual
                power_ups_verdes.remove(pu)

        # Colisiones con Power-ups amarillos
        for pu in power_ups_amarillos[:]:
            if rect_jugador.colliderect(pu):
                puntuacion += 50
                tiempo_transcurrido += 500
                rapido = True
                tiempo_rapido = tiempo_actual
                power_ups_amarillos.remove(pu)

        # Colisiones con Power-ups blancos
        for pu in power_ups_blancos[:]:
            if rect_jugador.colliderect(pu):
                puntuacion += 50
                tiempo_transcurrido += 500
                destructor = True
                tiempo_destructor = tiempo_actual
                power_ups_blancos.remove(pu)

        guardar_mejor_puntaje(puntuacion)

        # Renderizado
        pantalla.fill(NEGRO)

        # Color del jugador según sus estados activos
        if not invulnerable or (tiempo_actual // 100) % 2 == 0:
            if destructor:
                color_jugador = BLANCO
            elif rapido:
                color_jugador = AMARILLO
            else:
                color_jugador = AZUL
            pygame.draw.rect(pantalla, color_jugador, rect_jugador)

        # Dibujar obstáculos
        for obs in obstaculos:
            pygame.draw.rect(pantalla, ROJO, obs)

        # Dibujar power-ups
        for pu in power_ups_verdes:
            pygame.draw.rect(pantalla, VERDE, pu)
        for pu in power_ups_amarillos:
            pygame.draw.rect(pantalla, AMARILLO, pu)
        for pu in power_ups_blancos:
            pygame.draw.rect(pantalla, BLANCO, pu)

        # Mostrar Puntuación y Vidas
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        texto_vidas = fuente.render(f"Vidas: {'❤ ' * vidas}", True, ROJO)
        
        pantalla.blit(texto_puntuacion, (20, 20))
        pantalla.blit(texto_vidas, (20, 60))

        # Indicadores de Power-ups activos
        offset_y = 20
        if ralentizado:
            pantalla.blit(fuente.render("¡BLOQUES LENTOS!", True, VERDE), (ANCHO - 230, offset_y))
            offset_y += 40

        if rapido:
            pantalla.blit(fuente.render("¡DOBLE VELOCIDAD!", True, AMARILLO), (ANCHO - 245, offset_y))
            offset_y += 40

        if destructor:
            pantalla.blit(fuente.render("¡MODO DESTRUCTOR!", True, BLANCO), (ANCHO - 250, offset_y))

        pygame.display.flip()
        reloj.tick(FPS)

    mostrar_game_over(puntuacion)

def mostrar_game_over(puntuacion):
    guardar_mejor_puntaje(puntuacion)
    mejor_puntaje = cargar_mejor_puntaje()

    while True:
        pantalla.fill(NEGRO)
        
        texto_game_over = fuente_grande.render("¡JUEGO TERMINADO!", True, ROJO)
        texto_score = fuente.render(f"Puntuación final: {puntuacion}", True, BLANCO)
        texto_record = fuente.render(f"Mejor Puntaje: {mejor_puntaje}", True, VERDE)
        texto_reiniciar = fuente.render("Presiona 'R' para reiniciar o 'ESC' para salir", True, GRIS)

        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 80))
        pantalla.blit(texto_score, (ANCHO // 2 - texto_score.get_width() // 2, ALTO // 2 - 20))
        pantalla.blit(texto_record, (ANCHO // 2 - texto_record.get_width() // 2, ALTO // 2 + 20))
        pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 80))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    pantalla_inicio()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    pantalla_inicio()