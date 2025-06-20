import pygame
import sys

# Inicializar pygame
pygame.init()

# Constantes
ANCHO, ALTO = 600, 400
COLOR_FONDO = (30, 30, 30)
COLOR_JUGADOR = (0, 200, 255)
COLOR_OBSTACULO = (255, 80, 80)
GRAVEDAD = 0.6
SALTO = -10
FPS = 60

# Ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Geometry Dash Didáctico")

# Jugador
jugador = pygame.Rect(50, ALTO - 60, 40, 40)
velocidad_y = 0
en_suelo = True

# Obstáculos
obstaculos = []
contador = 0
fuente = pygame.font.SysFont(None, 36)

def crear_obstaculo():
    alto = 60
    ancho = 20
    x = ANCHO
    y = ALTO - alto
    return pygame.Rect(x, y, ancho, alto)

# Reloj
clock = pygame.time.Clock()
tiempo = 0
juego_activo = True

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if juego_activo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and en_suelo:
                velocidad_y = SALTO
                en_suelo = False
        if not juego_activo and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                # Reiniciar juego
                jugador.y = ALTO - 60
                velocidad_y = 0
                en_suelo = True
                obstaculos.clear()
                tiempo = 0
                contador = 0
                juego_activo = True

    if juego_activo:
        # Movimiento jugador
        velocidad_y += GRAVEDAD
        jugador.y += velocidad_y
        if jugador.y >= ALTO - 60:
            jugador.y = ALTO - 60
            velocidad_y = 0
            en_suelo = True

        # Obstáculos
        if len(obstaculos) == 0 or obstaculos[-1].x < ANCHO - 200:
            obstaculos.append(crear_obstaculo())
        for obstaculo in obstaculos:
            obstaculo.x -= 5
        if obstaculos and obstaculos[0].x < -40:
            obstaculos.pop(0)
            contador += 1

        # Colisiones
        for obstaculo in obstaculos:
            if jugador.colliderect(obstaculo):
                juego_activo = False

        # Contador de tiempo
        tiempo += 1 / FPS

    # Dibujar
    pantalla.fill(COLOR_FONDO)
    pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador)
    for obstaculo in obstaculos:
        pygame.draw.rect(pantalla, COLOR_OBSTACULO, obstaculo)

    texto_contador = fuente.render(f"Puntos: {contador}", True, (255,255,255))
    pantalla.blit(texto_contador, (10, 10))
    texto_tiempo = fuente.render(f"Tiempo: {int(tiempo)}s", True, (255,255,255))
    pantalla.blit(texto_tiempo, (10, 40))

    if not juego_activo:
        texto = fuente.render("¡Perdiste! Pulsa R para reiniciar", True, (255,255,0))
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 20))

    pygame.display.flip()
    clock.tick(FPS)