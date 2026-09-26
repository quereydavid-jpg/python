import pygame
import random
import math

# Inicializar Pygame
pygame.init()
ancho = 600
alto = 400
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego de Obstáculos - Círculo a la Meta")
reloj = pygame.time.Clock()

# --- Configuración del Círculo (Jugador) ---
size = 15
x_inicio = ancho // 2
y_inicio = alto - 30
x, y = x_inicio, y_inicio
velocidad = 4

# --- Configuración de la Meta ---
meta_ancho = 120
meta_alto = 35
meta_x = (ancho - meta_ancho) // 2
meta_y = 10
rect_meta = pygame.Rect(meta_x, meta_y, meta_ancho, meta_alto)

# --- Configuración de Obstáculos ---
filas_y = [80, 130, 180, 230, 280, 320]
nivel = 1
puntos = 0

def generar_obstaculos(dificultad):
    """ Genera obstaculos que cambian de ancho y velocidad segun el nivel """
    nuevos_obstaculos = []
    for pos_y in filas_y:
        # Ancho mínimo y máximo aumenta con el nivel
        min_w = min(50 + dificultad * 10, 150)
        max_w = min(100 + dificultad * 15, 220)
        obs_ancho = random.randint(min_w, max_w)
        obs_alto = 18
        obs_x = random.randint(0, ancho - obs_ancho)
        
        # Velocidad base aumenta con la dificultad
        vel_base = random.randint(2 + dificultad, 4 + dificultad * 2)
        obs_vel = random.choice([-1, 1]) * vel_base
        
        nuevos_obstaculos.append({
            'rect': pygame.Rect(obs_x, pos_y, obs_ancho, obs_alto),
            'vel': obs_vel
        })
    return nuevos_obstaculos

obstaculos = generar_obstaculos(nivel)
fuente = pygame.font.SysFont("arial", 18, bold=True)

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # --- Movimiento del Círculo (Teclas Flechas) ---
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        if x < ancho - size:
            x += velocidad
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        if x > size:
            x -= velocidad
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        if y > size:
            y -= velocidad
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        if y < alto - size:
            y += velocidad

    # --- Actualizar Posición de Obstáculos ---
    for obs in obstaculos:
        obs['rect'].x += obs['vel']
        # Rebotar en los bordes de la ventana
        if obs['rect'].left <= 0 or obs['rect'].right >= ancho:
            obs['vel'] *= -1

    # --- Detección de Colisiones (Círculo vs Rectángulos) ---
    for obs in obstaculos:
        rect = obs['rect']
        # Encontrar punto más cercano del rectángulo al centro del círculo
        cx = max(rect.left, min(x, rect.right))
        cy = max(rect.top, min(y, rect.bottom))
        
        distancia = math.hypot(x - cx, y - cy)
        
        # Si la distancia es menor que el radio, colisiona y regresa al inicio
        if distancia < size:
            x, y = x_inicio, y_inicio

    # --- Verificar si llega a la Meta ---
    if rect_meta.collidepoint(x, y):
        puntos += 1
        nivel += 1
        x, y = x_inicio, y_inicio
        # Al llegar a la meta, cambian el ancho y la velocidad de movimiento
        obstaculos = generar_obstaculos(nivel)

    # --- Renderizado / Dibujado ---
    ventana.fill((15, 23, 42))  # Fondo Oscuro Elegante

    # Meta
    pygame.draw.rect(ventana, (16, 185, 129), rect_meta, border_radius=8)
    texto_meta = fuente.render("META", True, (255, 255, 255))
    ventana.blit(texto_meta, (meta_x + 35, meta_y + 6))

    # Obstáculos
    for obs in obstaculos:
        pygame.draw.rect(ventana, (244, 63, 94), obs['rect'], border_radius=6)

    # Círculo Jugador
    pygame.draw.circle(ventana, (59, 130, 246), (int(x), int(y)), size)

    # HUD (Puntos y Nivel)
    texto_hud = fuente.render(f"Nivel: {nivel} | Puntos: {puntos}", True, (226, 232, 240))
    ventana.blit(texto_hud, (15, 15))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()