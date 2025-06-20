import pygame
import sys
import random
import math

# Inicializar pygame
pygame.init()

# Constantes del juego
ANCHO, ALTO = 1000, 600
FPS = 60

# Colores profesionales
COLORES = {
    'fondo_menu': (25, 25, 35),
    'fondo_nivel1': (30, 40, 60),
    'fondo_nivel2': (45, 30, 50),
    'fondo_nivel3': (50, 35, 35),
    'jugador': (0, 150, 255),
    'jugador_sombra': (0, 100, 200),
    'obstaculo_nivel1': (255, 100, 100),
    'obstaculo_nivel2': (255, 150, 50),
    'obstaculo_nivel3': (200, 50, 255),
    'suelo': (80, 80, 90),
    'texto_principal': (255, 255, 255),
    'texto_secundario': (200, 200, 200),
    'texto_titulo': (100, 200, 255),
    'progreso': (50, 255, 50),
    'warning': (255, 200, 0)
}

# Física del juego
GRAVEDAD = 0.7
SALTO_FUERZA = -14
ALTURA_SUELO = 80

# Configuración de niveles (balanceados para presentación)
CONFIGURACION_NIVELES = {
    1: {
        'nombre': 'NIVEL 1 - APRENDIZAJE',
        'descripcion': 'Nivel de práctica con obstáculos básicos',
        'velocidad_obstaculo': 4,
        'frecuencia_spawn': 120,  # Muy espaciado para facilitar
        'altura_obstaculos': [60, 70],
        'ancho_obstaculos': [25],
        'puntos_objetivo': 20,
        'color_obstaculo': COLORES['obstaculo_nivel1'],
        'color_fondo': COLORES['fondo_nivel1']
    },
    2: {
        'nombre': 'NIVEL 2 - INTERMEDIO',
        'descripcion': 'Mayor velocidad y obstáculos variados',
        'velocidad_obstaculo': 7,
        'frecuencia_spawn': 80,  # Más frecuente
        'altura_obstaculos': [60, 80, 100],
        'ancho_obstaculos': [25, 35],
        'puntos_objetivo': 40,
        'color_obstaculo': COLORES['obstaculo_nivel2'],
        'color_fondo': COLORES['fondo_nivel2']
    },
    3: {
        'nombre': 'NIVEL 3 - EXPERTO',
        'descripcion': 'Máxima dificultad con obstáculos complejos',
        'velocidad_obstaculo': 10,
        'frecuencia_spawn': 60,  # Muy frecuente
        'altura_obstaculos': [70, 90, 110, 130],
        'ancho_obstaculos': [25, 35, 45],
        'puntos_objetivo': 60,
        'color_obstaculo': COLORES['obstaculo_nivel3'],
        'color_fondo': COLORES['fondo_nivel3']
    }
}

class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -2)
        self.color = color
        self.vida = 60
        self.vida_max = 60
    
    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.vida -= 1
    
    def dibujar(self, pantalla):
        alpha = int(255 * (self.vida / self.vida_max))
        color_con_alpha = (*self.color, alpha)
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), 3)

class JuegoGeometryDash:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Geometry Dash Educativo - Proyecto Académico")
        
        # Fuentes profesionales
        self.fuente_titulo = pygame.font.Font(None, 48)
        self.fuente_subtitulo = pygame.font.Font(None, 36)
        self.fuente_texto = pygame.font.Font(None, 28)
        self.fuente_pequeña = pygame.font.Font(None, 24)
        
        # Estado del juego
        self.estado = 'menu'  # menu, jugando, pausa, game_over
        self.nivel_actual = 1
        self.puntos = 0
        self.tiempo_juego = 0
        self.mejor_puntuacion = 0
        
        # Jugador
        self.jugador_size = 45
        self.jugador = pygame.Rect(100, ALTO - ALTURA_SUELO - self.jugador_size, 
                                   self.jugador_size, self.jugador_size)
        self.velocidad_y = 0
        self.en_suelo = True
        self.animacion_jugador = 0
        
        # Obstáculos y efectos
        self.obstaculos = []
        self.particulas = []
        self.spawn_timer = 0
        self.transicion_nivel = False
        self.tiempo_transicion = 0
        
        # Estadísticas
        self.saltos_realizados = 0
        self.tiempo_supervivencia = 0
        
        self.clock = pygame.time.Clock()
    
    def mostrar_menu(self):
        self.pantalla.fill(COLORES['fondo_menu'])
        
        # Título principal con efecto
        titulo = self.fuente_titulo.render("GEOMETRY DASH EDUCATIVO", True, COLORES['texto_titulo'])
        self.pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
        
        # Subtítulo
        subtitulo = self.fuente_subtitulo.render("Proyecto de Programación en Python", True, COLORES['texto_secundario'])
        self.pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 150))
        
        # Información del proyecto
        info_lineas = [
            "CARACTERÍSTICAS DEL PROYECTO:",
            "• Sistema de niveles progresivos",
            "• Física realista con gravedad",
            "• Interfaz gráfica profesional",
            "• Sistema de puntuación y estadísticas",
            "",
            "OBJETIVO: Alcanza 20 puntos en cada nivel para avanzar",
            "",
            "CONTROLES:",
            "ESPACIO - Saltar",
            "P - Pausar juego",
            "",
            "Presiona ENTER para comenzar"
        ]
        
        y_offset = 220
        for linea in info_lineas:
            if linea.startswith("•"):
                color = COLORES['texto_secundario']
                fuente = self.fuente_pequeña
            elif linea.startswith("CARACTERÍSTICAS") or linea.startswith("OBJETIVO") or linea.startswith("CONTROLES"):
                color = COLORES['texto_titulo']
                fuente = self.fuente_texto
            else:
                color = COLORES['texto_principal']
                fuente = self.fuente_texto
            
            texto = fuente.render(linea, True, color)
            self.pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, y_offset))
            y_offset += 25
        
        # Mejor puntuación
        if self.mejor_puntuacion > 0:
            mejor = self.fuente_texto.render(f"Mejor Puntuación: {self.mejor_puntuacion}", True, COLORES['warning'])
            self.pantalla.blit(mejor, (ANCHO//2 - mejor.get_width()//2, y_offset + 20))
    
    def crear_obstaculo(self):
        config = CONFIGURACION_NIVELES[self.nivel_actual]
        altura = random.choice(config['altura_obstaculos'])
        ancho = random.choice(config['ancho_obstaculos'])
        
        x = ANCHO + 50
        y = ALTO - ALTURA_SUELO - altura
        
        return pygame.Rect(x, y, ancho, altura)
    
    def actualizar_fisica(self):
        # Física del jugador
        if not self.en_suelo:
            self.velocidad_y += GRAVEDAD
        
        self.jugador.y += self.velocidad_y
        
        # Verificar colisión con suelo
        if self.jugador.y >= ALTO - ALTURA_SUELO - self.jugador_size:
            self.jugador.y = ALTO - ALTURA_SUELO - self.jugador_size
            self.velocidad_y = 0
            self.en_suelo = True
        
        # Animación del jugador
        self.animacion_jugador += 5
    
    def actualizar_obstaculos(self):
        config = CONFIGURACION_NIVELES[self.nivel_actual]
        
        # Crear nuevos obstáculos
        self.spawn_timer += 1
        if self.spawn_timer >= config['frecuencia_spawn']:
            self.obstaculos.append(self.crear_obstaculo())
            self.spawn_timer = 0
        
        # Mover obstáculos
        for obstaculo in self.obstaculos[:]:
            obstaculo.x -= config['velocidad_obstaculo']
            
            # Eliminar obstáculos fuera de pantalla y contar puntos
            if obstaculo.x < -100:
                self.obstaculos.remove(obstaculo)
                self.puntos += 1
        
        # Verificar colisiones
        for obstaculo in self.obstaculos:
            if self.jugador.colliderect(obstaculo):
                self.crear_particulas_explosion(self.jugador.centerx, self.jugador.centery)
                self.estado = 'game_over'
    
    def crear_particulas_explosion(self, x, y):
        for _ in range(15):
            self.particulas.append(Particula(x, y, COLORES['jugador']))
    
    def actualizar_particulas(self):
        for particula in self.particulas[:]:
            particula.actualizar()
            if particula.vida <= 0:
                self.particulas.remove(particula)
    
    def verificar_cambio_nivel(self):
        config = CONFIGURACION_NIVELES[self.nivel_actual]
        
        if self.puntos >= config['puntos_objetivo'] and self.nivel_actual < 3:
            self.nivel_actual += 1
            self.transicion_nivel = True
            self.tiempo_transicion = 180  # 3 segundos
            self.obstaculos.clear()
            self.spawn_timer = 0
    
    def dibujar_juego(self):
        config = CONFIGURACION_NIVELES[self.nivel_actual]
        
        # Fondo con gradiente
        self.pantalla.fill(config['color_fondo'])
        
        # Suelo con diseño
        pygame.draw.rect(self.pantalla, COLORES['suelo'], 
                        (0, ALTO - ALTURA_SUELO, ANCHO, ALTURA_SUELO))
        
        # Líneas decorativas en el suelo
        for i in range(0, ANCHO, 100):
            pygame.draw.line(self.pantalla, (100, 100, 110), 
                           (i, ALTO - ALTURA_SUELO), (i + 50, ALTO - ALTURA_SUELO + 20), 2)
        
        # Jugador con efecto rotación
        rotacion = math.sin(self.animacion_jugador * 0.1) * 10
        color_jugador = COLORES['jugador']
        
        # Sombra del jugador
        sombra = pygame.Rect(self.jugador.x + 3, self.jugador.y + 3, 
                           self.jugador.width, self.jugador.height)
        pygame.draw.rect(self.pantalla, COLORES['jugador_sombra'], sombra)
        
        # Jugador principal
        pygame.draw.rect(self.pantalla, color_jugador, self.jugador)
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.jugador, 2)
        
        # Obstáculos con efecto 3D
        for obstaculo in self.obstaculos:
            # Sombra del obstáculo
            sombra_obs = pygame.Rect(obstaculo.x + 2, obstaculo.y + 2, 
                                   obstaculo.width, obstaculo.height)
            pygame.draw.rect(self.pantalla, (50, 50, 50), sombra_obs)
            
            # Obstáculo principal
            pygame.draw.rect(self.pantalla, config['color_obstaculo'], obstaculo)
            pygame.draw.rect(self.pantalla, (255, 255, 255), obstaculo, 2)
        
        # Partículas
        for particula in self.particulas:
            particula.dibujar(self.pantalla)
    
    def dibujar_interfaz(self):
        config = CONFIGURACION_NIVELES[self.nivel_actual]
        
        # Panel de información superior
        pygame.draw.rect(self.pantalla, (0, 0, 0, 100), (0, 0, ANCHO, 120))
        
        # Información del nivel
        nivel_texto = self.fuente_subtitulo.render(config['nombre'], True, COLORES['texto_titulo'])
        self.pantalla.blit(nivel_texto, (20, 10))
        
        desc_texto = self.fuente_pequeña.render(config['descripcion'], True, COLORES['texto_secundario'])
        self.pantalla.blit(desc_texto, (20, 45))
        
        # Estadísticas
        stats = [
            f"Puntos: {self.puntos}/{config['puntos_objetivo']}",
            f"Nivel: {self.nivel_actual}/3",
            f"Tiempo: {int(self.tiempo_juego)}s",
            f"Saltos: {self.saltos_realizados}"
        ]
        
        x_offset = ANCHO - 300
        for i, stat in enumerate(stats):
            texto = self.fuente_texto.render(stat, True, COLORES['texto_principal'])
            self.pantalla.blit(texto, (x_offset, 15 + i * 25))
        
        # Barra de progreso
        if self.nivel_actual < 3:
            progreso = min(self.puntos / config['puntos_objetivo'], 1.0)
            barra_ancho = 300
            barra_alto = 15
            
            # Fondo de la barra
            pygame.draw.rect(self.pantalla, (50, 50, 50), 
                           (20, 75, barra_ancho, barra_alto))
            
            # Progreso
            pygame.draw.rect(self.pantalla, COLORES['progreso'], 
                           (20, 75, int(barra_ancho * progreso), barra_alto))
            
            # Borde
            pygame.draw.rect(self.pantalla, COLORES['texto_principal'], 
                           (20, 75, barra_ancho, barra_alto), 2)
    
    def mostrar_transicion_nivel(self):
        if self.tiempo_transicion > 0:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.pantalla.blit(overlay, (0, 0))
            
            config = CONFIGURACION_NIVELES[self.nivel_actual]
            
            # Texto de nuevo nivel
            titulo = self.fuente_titulo.render("¡NUEVO NIVEL!", True, COLORES['warning'])
            self.pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//2 - 80))
            
            nombre = self.fuente_subtitulo.render(config['nombre'], True, COLORES['texto_titulo'])
            self.pantalla.blit(nombre, (ANCHO//2 - nombre.get_width()//2, ALTO//2 - 30))
            
            desc = self.fuente_texto.render(config['descripcion'], True, COLORES['texto_principal'])
            self.pantalla.blit(desc, (ANCHO//2 - desc.get_width()//2, ALTO//2 + 10))
            
            self.tiempo_transicion -= 1
            if self.tiempo_transicion <= 0:
                self.transicion_nivel = False
    
    def mostrar_game_over(self):
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        # Actualizar mejor puntuación
        if self.puntos > self.mejor_puntuacion:
            self.mejor_puntuacion = self.puntos
        
        # Texto de game over
        game_over = self.fuente_titulo.render("JUEGO TERMINADO", True, (255, 100, 100))
        self.pantalla.blit(game_over, (ANCHO//2 - game_over.get_width()//2, ALTO//2 - 100))
        
        # Estadísticas finales
        stats_finales = [
            f"Puntuación Final: {self.puntos}",
            f"Nivel Alcanzado: {self.nivel_actual}",
            f"Tiempo de Supervivencia: {int(self.tiempo_juego)}s",
            f"Saltos Realizados: {self.saltos_realizados}",
            f"Mejor Puntuación: {self.mejor_puntuacion}"
        ]
        
        y_offset = ALTO//2 - 40
        for stat in stats_finales:
            texto = self.fuente_texto.render(stat, True, COLORES['texto_principal'])
            self.pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, y_offset))
            y_offset += 30
        
        # Instrucciones
        reiniciar = self.fuente_texto.render("Presiona R para reiniciar o ESC para volver al menú", 
                                           True, COLORES['warning'])
        self.pantalla.blit(reiniciar, (ANCHO//2 - reiniciar.get_width()//2, y_offset + 40))
    
    def reiniciar_juego(self):
        self.nivel_actual = 1
        self.puntos = 0
        self.tiempo_juego = 0
        self.saltos_realizados = 0
        self.jugador.y = ALTO - ALTURA_SUELO - self.jugador_size
        self.velocidad_y = 6
        self.en_suelo = True
        self.obstaculos.clear()
        self.particulas.clear()
        self.spawn_timer = 0
        self.transicion_nivel = False
        self.tiempo_transicion = 0
        self.estado = 'jugando'
    
    def ejecutar(self):
        ejecutando = True
        
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                elif evento.type == pygame.KEYDOWN:
                    if self.estado == 'menu':
                        if evento.key == pygame.K_RETURN:
                            self.reiniciar_juego()
                    
                    elif self.estado == 'jugando':
                        if evento.key == pygame.K_SPACE and self.en_suelo:
                            self.velocidad_y = SALTO_FUERZA
                            self.en_suelo = False
                            self.saltos_realizados += 1
                        elif evento.key == pygame.K_p:
                            self.estado = 'pausa'
                    
                    elif self.estado == 'game_over':
                        if evento.key == pygame.K_r:
                            self.reiniciar_juego()
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado = 'menu'
                    
                    elif self.estado == 'pausa':
                        if evento.key == pygame.K_p:
                            self.estado = 'jugando'
            
            # Lógica del juego
            if self.estado == 'jugando' and not self.transicion_nivel:
                self.actualizar_fisica()
                self.actualizar_obstaculos()
                self.verificar_cambio_nivel()
                self.tiempo_juego += 1/FPS
            
            # Actualizar partículas siempre
            self.actualizar_particulas()
            
            # Renderizado
            if self.estado == 'menu':
                self.mostrar_menu()
            else:
                self.dibujar_juego()
                self.dibujar_interfaz()
                
                if self.transicion_nivel:
                    self.mostrar_transicion_nivel()
                elif self.estado == 'game_over':
                    self.mostrar_game_over()
                elif self.estado == 'pausa':
                    overlay = pygame.Surface((ANCHO, ALTO))
                    overlay.set_alpha(150)
                    overlay.fill((0, 0, 0))
                    self.pantalla.blit(overlay, (0, 0))
                    
                    pausa_texto = self.fuente_titulo.render("PAUSA", True, COLORES['warning'])
                    self.pantalla.blit(pausa_texto, (ANCHO//2 - pausa_texto.get_width()//2, ALTO//2))
                    
                    continuar = self.fuente_texto.render("Presiona P para continuar", True, COLORES['texto_principal'])
                    self.pantalla.blit(continuar, (ANCHO//2 - continuar.get_width()//2, ALTO//2 + 50))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    juego = JuegoGeometryDash()
    juego.ejecutar()