
import commons
import pygame
import vector
import states
import entities

from vector import Vector
from states import GameState, MenuState, PlayState
from ball import Ball
from peg import Peg
import numpy as np

def update():
    entities.update_balls()

def draw():
    commons.screen.fill((50, 50, 50))

    entities.draw_balls()
    entities.draw_pegs()


pygame.init()

commons.screen = pygame.display.set_mode((commons.screen_w, commons.screen_h))

pygame.display.set_caption("Peggle Tutorial")

icon_image = pygame.image.load("res/images/icons/ball.png").convert_alpha()
icon_image.set_colorkey((255, 0, 255))
pygame.display.set_icon(icon_image)

app_running = True
delta_time = 0.0
clock = pygame.time.Clock()

mouse_position = (0, 0)


mid_x = int(commons.screen_w / 2)
rows = np.linspace(commons.screen_h / 5, commons.screen_h - commons.screen_h / 5, 10)
for i in range(len(rows)):
    shift = 7
    num = i + shift

    xs = np.linspace(mid_x - num * mid_x / 15, mid_x + num * mid_x / 15, num)
    y = rows[i]

    for x in xs:
        entities.level_pegs.append(Peg(Vector(x, y)))

while app_running:
    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app_running = False
        elif event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                entities.balls.append(Ball(Vector(event.pos[0], event.pos[1]), Vector(0, 0)))
            if event.button == pygame.BUTTON_RIGHT:
                entities.pegs.append(Peg(Vector(event.pos[0], event.pos[1])))


    update()
    draw()

    pygame.display.flip()

    commons.delta_time = 0.001 * clock.tick(144)

pygame.quit()
