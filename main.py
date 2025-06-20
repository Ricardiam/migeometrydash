import pygame, sys

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

size = (800, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# ---- Cuadrado rojo ----
# -- coordenadas --
coord_x_rect_1 = 0
coord_y_rect_1 = 0

# -- velocidad --
speed_x_rect_1 = 0
speed_y_rect_1 = 0

# ---- Cuadrado azul ----
# -- coordenadas --
coord_x_rect_2 = 750
coord_y_rect_2 = 0

# -- velocidad --
speed_x_rect_2 = 0
speed_y_rect_2 = 0


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # --- logica de cuadrado rojo ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                speed_x_rect_1 = -3
            if event.key == pygame.K_d:
                speed_x_rect_1 = 3
            if event.key == pygame.K_w:
                speed_y_rect_1 = -3
            if event.key == pygame.K_s:
                speed_y_rect_1 = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                speed_x_rect_1 = 0
            if event.key == pygame.K_d:
                speed_x_rect_1 = 0
            if event.key == pygame.K_w:
                speed_y_rect_1 = 0
            if event.key == pygame.K_s:
                speed_y_rect_1 = 0

        # --- logica de cuadrado azul ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed_x_rect_2 = -3
            if event.key == pygame.K_RIGHT:
                speed_x_rect_2 = 3
            if event.key == pygame.K_UP:
                speed_y_rect_2 = -3
            if event.key == pygame.K_DOWN:
                speed_y_rect_2 = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                speed_x_rect_2 = 0
            if event.key == pygame.K_RIGHT:
                speed_x_rect_2 = 0
            if event.key == pygame.K_UP:
                speed_y_rect_2 = 0
            if event.key == pygame.K_DOWN:
                speed_y_rect_2 = 0

    screen.fill(WHITE)

    coord_x_rect_1 += speed_x_rect_1
    coord_y_rect_1 += speed_y_rect_1
    if coord_x_rect_1 < 0:
        coord_x_rect_1 = 0
    if coord_y_rect_1 < 0:
        coord_y_rect_1 = 0
    if coord_x_rect_1 + 50 > size[0]:
        coord_x_rect_1 = size[0] - 50
    if coord_y_rect_1 + 50 > size[1]:
        coord_y_rect_1 = size[1] - 50
    pygame.draw.rect(screen, RED, (coord_x_rect_1, coord_y_rect_1, 50, 50))

    coord_x_rect_2 += speed_x_rect_2
    coord_y_rect_2 += speed_y_rect_2
    if coord_x_rect_2 < 0:
        coord_x_rect_2 = 0
    if coord_y_rect_2 < 0:
        coord_y_rect_2 = 0
    if coord_x_rect_2 + 50 > size[0]:
        coord_x_rect_2 = size[0] - 50
    if coord_y_rect_2 + 50 > size[1]:
        coord_y_rect_2 = size[1] - 50
    pygame.draw.rect(screen, BLUE, (coord_x_rect_2, coord_y_rect_2, 50, 50))

    pygame.display.flip()
    clock.tick(60)