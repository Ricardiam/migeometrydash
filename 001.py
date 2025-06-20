import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Constantes
ANCHO, ALTO = 800, 500
COLOR_FONDO = (30, 30, 30)
COLOR_JUGADOR = (0, 200, 255)
COLOR_OBSTACULO = (255, 80, 80)
COLOR_OBSTACULO_NIVEL2 = (255, 150, 50)
COLOR_OBSTACULO_NIVEL3 = (150, 50, 255)
GRAVEDAD = 0.6
SALTO = -12
FPS = 60

# Configuración de niveles
NIVELES = {
    1: {
        'nombre': 'Nivel 1 - Principiante',
        'velocidad': 5,
        'frecuencia': 180,
        'color_obstaculo': COLOR_OBSTACULO,
        'color_fondo': (30, 30, 30)
    },
    2: {
        'nombre': 'Nivel 2 - Intermedio',
        'velocidad': 7,
        'frecuencia': 150,
        'color_obstaculo': COLOR_OBSTACULO_NIVEL2,
        'color_fondo': (30, 40, 30)
    },
    3: {
        'nombre': 'Nivel 3 - Avanzado',
        'velocidad': 9,
        'frecuencia': 120,
        'color_obstaculo': COLOR_OBSTACULO_NIVEL3,
        'color_fondo': (40, 30, 40)
    }
}

# Ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Geometry Dash Didáctico - Niveles")

# Variables del juego
nivel_actual = 1
puntos_para_siguiente_nivel = 20

# Jugador (posicionado en la parte inferior)
jugador_ancho, jugador_alto = 40, 40
jugador = pygame.Rect(80, ALTO - jugador_alto - 10, jugador_ancho, jugador_alto)
velocidad_y = 0
en_suelo = True

# Obstáculos
obstaculos = []
contador = 0
contador_frames = 0
fuente = pygame.font.SysFont(None, 36)
fuente_grande = pygame.font.SysFont(None, 48)

def crear_obstaculo(nivel):
    """Crea obstáculos con diferentes características según el nivel"""
    if nivel == 1:
        alto = random.choice([60, 80])
        ancho = 25
    elif nivel == 2:
        alto = random.choice([60, 80, 100])
        ancho = random.choice([25, 35])
    else:  # nivel 3
        alto = random.choice([60, 80, 100, 120])
        ancho = random.choice([25, 35, 45])
    
    x = ANCHO
    y = ALTO - alto - 10  # Ajustado para que esté en la parte inferior
    return pygame.Rect(x, y, ancho, alto)

def mostrar_transicion_nivel(nivel):
    """Muestra una pantalla de transición entre niveles"""
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    pantalla.blit(overlay, (0, 0))
    
    texto_nivel = fuente_grande.render(f"¡{NIVELES[nivel]['nombre']}!", True, (255, 255, 0))
    texto_info = fuente.render("¡Preparate para más velocidad!", True, (255, 255, 255))
    
    pantalla.blit(texto_nivel, (ANCHO//2 - texto_nivel.get_width()//2, ALTO//2 - 40))
    pantalla.blit(texto_info, (ANCHO//2 - texto_info.get_width()//2, ALTO//2 + 20))
    
    pygame.display.flip()
    pygame.time.wait(2000)  # Pausa de 2 segundos

# Reloj
clock = pygame.time.Clock()
tiempo = 0
juego_activo = True
mostrar_transicion = False

# Mostrar pantalla inicial
texto_inicio = fuente.render("¡Presiona ESPACIO para saltar! Llega a 20 puntos para pasar de nivel", True, (255, 255, 255))
pantalla.fill(COLOR_FONDO)
pantalla.blit(texto_inicio, (ANCHO//2 - texto_inicio.get_width()//2, ALTO//2))
pygame.display.flip()
pygame.time.wait(3000)

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
                jugador.y = ALTO - jugador_alto - 10
                velocidad_y = 0
                en_suelo = True
                obstaculos.clear()
                tiempo = 0
                contador = 0
                contador_frames = 0
                nivel_actual = 1
                juego_activo = True

    if juego_activo:
        # Verificar cambio de nivel
        if contador >= puntos_para_siguiente_nivel and nivel_actual < 3:
            nivel_actual += 1
            puntos_para_siguiente_nivel += 20
            mostrar_transicion_nivel(nivel_actual)
            # Limpiar obstáculos al cambiar de nivel
            obstaculos.clear()
            contador_frames = 0

        # Movimiento jugador (con gravedad mejorada)
        velocidad_y += GRAVEDAD
        jugador.y += velocidad_y
        
        # Mantener jugador en la parte inferior
        if jugador.y >= ALTO - jugador_alto - 10:
            jugador.y = ALTO - jugador_alto - 10
            velocidad_y = 0
            en_suelo = True

        # Crear obstáculos según la frecuencia del nivel
        contador_frames += 1
        frecuencia_actual = NIVELES[nivel_actual]['frecuencia']
        
        if contador_frames % frecuencia_actual == 0 or len(obstaculos) == 0:
            obstaculos.append(crear_obstaculo(nivel_actual))

        # Mover obstáculos con la velocidad del nivel
        velocidad_actual = NIVELES[nivel_actual]['velocidad']
        for obstaculo in obstaculos:
            obstaculo.x -= velocidad_actual

        # Eliminar obstáculos fuera de pantalla y contar puntos
        if obstaculos and obstaculos[0].x < -50:
            obstaculos.pop(0)
            contador += 1

        # Colisiones
        for obstaculo in obstaculos:
            if jugador.colliderect(obstaculo):
                juego_activo = False

        # Contador de tiempo
        tiempo += 1 / FPS

    # Dibujar con el color de fondo del nivel actual
    color_fondo_actual = NIVELES[nivel_actual]['color_fondo']
    pantalla.fill(color_fondo_actual)
    
    # Dibujar suelo
    pygame.draw.rect(pantalla, (100, 100, 100), (0, ALTO - 10, ANCHO, 10))
    
    # Dibujar jugador
    pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador)
    
    # Dibujar obstáculos con el color del nivel
    color_obstaculo_actual = NIVELES[nivel_actual]['color_obstaculo']
    for obstaculo in obstaculos:
        pygame.draw.rect(pantalla, color_obstaculo_actual, obstaculo)

    # Interfaz de usuario
    texto_contador = fuente.render(f"Puntos: {contador}", True, (255, 255, 255))
    pantalla.blit(texto_contador, (10, 10))
    
    texto_nivel = fuente.render(f"{NIVELES[nivel_actual]['nombre']}", True, (255, 255, 100))
    pantalla.blit(texto_nivel, (10, 40))
    
    texto_objetivo = fuente.render(f"Objetivo: {puntos_para_siguiente_nivel} puntos", True, (255, 255, 255))
    pantalla.blit(texto_objetivo, (10, 70))
    
    texto_tiempo = fuente.render(f"Tiempo: {int(tiempo)}s", True, (255, 255, 255))
    pantalla.blit(texto_tiempo, (ANCHO - 150, 10))

    # Barra de progreso para el siguiente nivel
    if nivel_actual < 3:
        progreso = contador / puntos_para_siguiente_nivel
        pygame.draw.rect(pantalla, (100, 100, 100), (10, 100, 200, 10))
        pygame.draw.rect(pantalla, (0, 255, 0), (10, 100, int(200 * progreso), 10))

    # Pantalla de game over
    if not juego_activo:
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        pantalla.blit(overlay, (0, 0))
        
        texto_perdiste = fuente_grande.render("¡Perdiste!", True, (255, 100, 100))
        texto_puntos = fuente.render(f"Puntos conseguidos: {contador}", True, (255, 255, 255))
        texto_nivel_alcanzado = fuente.render(f"Nivel alcanzado: {nivel_actual}", True, (255, 255, 255))
        texto_reiniciar = fuente.render("Pulsa R para reiniciar", True, (255, 255, 0))
        
        pantalla.blit(texto_perdiste, (ANCHO//2 - texto_perdiste.get_width()//2, ALTO//2 - 60))
        pantalla.blit(texto_puntos, (ANCHO//2 - texto_puntos.get_width()//2, ALTO//2 - 20))
        pantalla.blit(texto_nivel_alcanzado, (ANCHO//2 - texto_nivel_alcanzado.get_width()//2, ALTO//2 + 10))
        pantalla.blit(texto_reiniciar, (ANCHO//2 - texto_reiniciar.get_width()//2, ALTO//2 + 50))

    # Victoria (llegar al nivel 3 con suficientes puntos)
    if contador >= 60 and nivel_actual == 3:
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(150)
        overlay.fill((0, 50, 0))
        pantalla.blit(overlay, (0, 0))
        
        texto_victoria = fuente_grande.render("¡FELICIDADES!", True, (0, 255, 0))
        texto_completado = fuente.render("¡Has completado todos los niveles!", True, (255, 255, 255))
        texto_reiniciar = fuente.render("Pulsa R para jugar de nuevo", True, (255, 255, 0))
        
        pantalla.blit(texto_victoria, (ANCHO//2 - texto_victoria.get_width()//2, ALTO//2 - 40))
        pantalla.blit(texto_completado, (ANCHO//2 - texto_completado.get_width()//2, ALTO//2))
        pantalla.blit(texto_reiniciar, (ANCHO//2 - texto_reiniciar.get_width()//2, ALTO//2 + 40))

    pygame.display.flip()
    clock.tick(FPS)