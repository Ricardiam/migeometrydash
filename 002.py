import pygame
import random
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 400
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Geometry Dash Mejorado")
RELOJ = pygame.time.Clock()
FUENTE = pygame.font.SysFont("Arial", 28)
FUENTE_GRANDE = pygame.font.SysFont("Arial", 48, bold=True)

# Colores por nivel
COLORES_FONDO = [(30, 30, 60), (30, 60, 30), (60, 30, 30)]
COLORES_OBS = [(0, 200, 255), (255, 180, 0), (255, 60, 60)]
COLOR_JUGADOR = (0, 120, 255)
COLOR_SUELO = (200, 200, 200)
COLOR_BARRA = (255, 255, 255)

# Parámetros de niveles
NIVELES = [
    {"vel": 6, "freq": 60, "obs_min": 40, "obs_max": 60, "alt_min": 40, "alt_max": 80},
    {"vel": 9, "freq": 45, "obs_min": 30, "obs_max": 60, "alt_min": 40, "alt_max": 120},
    {"vel": 13, "freq": 35, "obs_min": 25, "obs_max": 55, "alt_min": 60, "alt_max": 160},
]
PUNTOS_POR_NIVEL = 20
TOTAL_NIVELES = len(NIVELES)

# Jugador
JUG_ANCHO, JUG_ALTO = 40, 40
JUG_X = 100
SUELO_Y = ALTO - 60
GRAVEDAD = 1.1
SALTO = -17

# Estados del juego
INICIO, JUGANDO, TRANSICION, GAMEOVER, VICTORIA = range(5)

def dibujar_texto(texto, fuente, color, x, y, centrado=False):
    img = fuente.render(texto, True, color)
    rect = img.get_rect()
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    VENTANA.blit(img, rect)

def pantalla_inicio():
    VENTANA.fill((20, 20, 40))
    dibujar_texto("Geometry Dash Mejorado", FUENTE_GRANDE, (0, 200, 255), ANCHO//2, 80, True)
    dibujar_texto("Presiona ESPACIO para saltar", FUENTE, (255,255,255), ANCHO//2, 160, True)
    dibujar_texto("Evita los obstáculos y avanza niveles", FUENTE, (255,255,255), ANCHO//2, 200, True)
    dibujar_texto("¡Llega al final para ganar!", FUENTE, (255,255,255), ANCHO//2, 240, True)
    dibujar_texto("Presiona ENTER para comenzar", FUENTE, (255,255,0), ANCHO//2, 320, True)
    pygame.display.flip()

def pantalla_transicion(nivel):
    VENTANA.fill(COLORES_FONDO[nivel])
    dibujar_texto(f"Nivel {nivel+1}", FUENTE_GRANDE, (255,255,255), ANCHO//2, ALTO//2-30, True)
    dibujar_texto("¡Prepárate!", FUENTE, (255,255,255), ANCHO//2, ALTO//2+30, True)
    pygame.display.flip()
    pygame.time.delay(1200)

def pantalla_gameover(puntos, nivel):
    VENTANA.fill((40, 0, 0))
    dibujar_texto("¡Perdiste!", FUENTE_GRANDE, (255,60,60), ANCHO//2, 100, True)
    dibujar_texto(f"Puntos: {puntos}", FUENTE, (255,255,255), ANCHO//2, 180, True)
    dibujar_texto(f"Nivel alcanzado: {nivel+1}", FUENTE, (255,255,255), ANCHO//2, 220, True)
    dibujar_texto("Presiona ENTER para reiniciar", FUENTE, (255,255,0), ANCHO//2, 320, True)
    pygame.display.flip()

def pantalla_victoria():
    VENTANA.fill((0, 80, 0))
    dibujar_texto("¡Victoria!", FUENTE_GRANDE, (0,255,100), ANCHO//2, 120, True)
    dibujar_texto("¡Completaste todos los niveles!", FUENTE, (255,255,255), ANCHO//2, 200, True)
    dibujar_texto("Presiona ENTER para jugar de nuevo", FUENTE, (255,255,0), ANCHO//2, 320, True)
    pygame.display.flip()

def barra_progreso(puntos, nivel):
    ancho_total = 300
    x = ANCHO//2 - ancho_total//2
    y = 30
    prog = min(puntos % PUNTOS_POR_NIVEL, PUNTOS_POR_NIVEL)
    pygame.draw.rect(VENTANA, COLOR_BARRA, (x, y, ancho_total, 18), 2)
    pygame.draw.rect(VENTANA, COLOR_BARRA, (x, y, int(ancho_total * prog / PUNTOS_POR_NIVEL), 18))

def main():
    estado = INICIO
    nivel = 0
    puntos = 0
    jugador_y = SUELO_Y - JUG_ALTO
    vel_y = 0
    en_suelo = True
    obstaculos = []
    frame_obs = 0

    while True:
        if estado == INICIO:
            pantalla_inicio()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    estado = TRANSICION
                    nivel = 0
                    puntos = 0
                    jugador_y = SUELO_Y - JUG_ALTO
                    vel_y = 0
                    en_suelo = True
                    obstaculos = []
                    frame_obs = 0
        elif estado == TRANSICION:
            pantalla_transicion(nivel)
            estado = JUGANDO
        elif estado == JUGANDO:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    if en_suelo:
                        vel_y = SALTO
                        en_suelo = False

            # Físicas del jugador
            vel_y += GRAVEDAD
            jugador_y += vel_y
            if jugador_y >= SUELO_Y - JUG_ALTO:
                jugador_y = SUELO_Y - JUG_ALTO
                vel_y = 0
                en_suelo = True

            # Obstáculos
            frame_obs += 1
            params = NIVELES[nivel]
            if frame_obs >= params["freq"]:
                frame_obs = 0
                ancho = random.randint(params["obs_min"], params["obs_max"])
                alto = random.randint(params["alt_min"], params["alt_max"])
                obs_y = SUELO_Y - alto
                obstaculos.append([ANCHO, obs_y, ancho, alto])

            for obs in obstaculos:
                obs[0] -= params["vel"]

            # Colisiones
            jugador_rect = pygame.Rect(JUG_X, int(jugador_y), JUG_ANCHO, JUG_ALTO)
            colision = False
            for obs in obstaculos:
                obs_rect = pygame.Rect(obs[0], obs[1], obs[2], obs[3])
                if jugador_rect.colliderect(obs_rect):
                    colision = True
                    break

            if colision:
                estado = GAMEOVER

            # Quitar obstáculos fuera de pantalla y sumar puntos
            obstaculos = [obs for obs in obstaculos if obs[0] + obs[2] > 0]
            for obs in obstaculos:
                if obs[0] + obs[2] < JUG_X and not obs[-1:] == [True]:
                    puntos += 1
                    obs.append(True)  # Marcar como contado

            # Cambio de nivel
            if puntos >= (nivel+1)*PUNTOS_POR_NIVEL:
                nivel += 1
                if nivel >= TOTAL_NIVELES:
                    estado = VICTORIA
                else:
                    obstaculos = []
                    frame_obs = 0
                    jugador_y = SUELO_Y - JUG_ALTO
                    vel_y = 0
                    en_suelo = True
                    estado = TRANSICION

            # Dibujo
            VENTANA.fill(COLORES_FONDO[nivel])
            pygame.draw.rect(VENTANA, COLOR_SUELO, (0, SUELO_Y, ANCHO, 8))
            for obs in obstaculos:
                pygame.draw.rect(VENTANA, COLORES_OBS[nivel], (obs[0], obs[1], obs[2], obs[3]))
            pygame.draw.rect(VENTANA, COLOR_JUGADOR, (JUG_X, int(jugador_y), JUG_ANCHO, JUG_ALTO))
            barra_progreso(puntos, nivel)
            dibujar_texto(f"Nivel: {nivel+1}/{TOTAL_NIVELES}", FUENTE, (255,255,255), 20, 20)
            dibujar_texto(f"Puntos: {puntos}", FUENTE, (255,255,255), 20, 60)
            dibujar_texto("Salta: ESPACIO", FUENTE, (200,200,200), ANCHO-220, 20)
            pygame.display.flip()
            RELOJ.tick(60)
        elif estado == GAMEOVER:
            pantalla_gameover(puntos, nivel)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    estado = INICIO
        elif estado == VICTORIA:
            pantalla_victoria()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    estado = INICIO

if __name__ == "__main__":
    main()