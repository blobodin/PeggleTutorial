
import commons
import pygame
import vector
import states
import entities
import images

from vector import *
from states import GameState, MenuState, PlayState
from ball import Ball
from peg import Peg
from bucket import Bucket
import numpy as np

def update():
    entities.update_balls()

def draw():
    commons.screen.fill((1,75,32))

    entities.draw_balls()
    entities.draw_pegs()
    entities.draw_buckets()

    pygame.draw.line(commons.screen, (100, 0, 0), (commons.screen_w / 2 - commons.screen_w / 4, commons.screen_h / 7), (commons.screen_w / 2 + commons.screen_w / 4, commons.screen_h / 7), 10)

    score_loc = (commons.screen_w / 35, commons.screen_h / 30)
    text_surface, rect = commons.font.render(f"Score: {states.score}", (0, 0, 0))
    commons.screen.blit(text_surface, score_loc)

    if states.peg_place:
        text_surface, rect = commons.font.render("Place Pegs with Right Click (Remove all with Spacebar)", (0, 0, 0))
        commons.screen.blit(text_surface, (score_loc[0], score_loc[1] + commons.screen_h / 30))

        text_surface, rect = commons.font.render("'Based' on what you know, score the number", (255, 192, 0))
        commons.screen.blit(text_surface, (score_loc[0], score_loc[1] + 2 * commons.screen_h / 30))

    if states.win:
        text_surface, rect = commons.font.render("Winner!", (255, 192, 200))
        commons.screen.blit(text_surface, (score_loc[0], score_loc[1] + 3 * commons.screen_h / 30))



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

commons.font = pygame.freetype.Font("res/fonts/Evogria.otf", 20)

# Level description
mid_x = int(commons.screen_w / 2)
rows = np.linspace(commons.screen_h / 5, commons.screen_h - commons.screen_h / 5, 10)
for i in range(len(rows)):
    shift = 7
    num = i + shift

    xs = np.linspace(mid_x - num * mid_x / 15, mid_x + num * mid_x / 15, num)
    y = rows[i]

    for x in xs:
        entities.level_pegs.append(Peg(Vector(x, y)))

# entities.light_pegs = [3, 9, 12, 19, 27, 30, 38, 39, 40, 50, 51, 63, 91]
entities.light_pegs += [1, 17, 37]
entities.light_pegs += [5, 6, 12, 14, 30, 32, 41, 42]
entities.light_pegs += [45, 47, 71, 72, 73, 103]
entities.light_pegs += [45 + 5, 46 + 5, 47 + 5, 64, 72 + 5, 92, 101 + 5, 102 + 5, 103 + 5]
entities.light_pegs += [46 + 9, 47 + 9, 67, 69, 95, 97, 102 + 9, 103 + 9]
# entities.light_pegs += [66, 67, 68, 80, 82, 94, 95, 96]
states.pegs_revealed = len(entities.light_pegs)

for i in entities.light_pegs:
    entities.level_pegs[i].peg_type = 1

entities.buckets.append(Bucket(Vector(mid_x, commons.screen_h - commons.screen_h/20), commons.screen_w / 16, commons.screen_h / 12, 10000))

shift1 = commons.screen_w * (1 / 32 + 1 / 16)
entities.buckets.append(Bucket(Vector(mid_x - shift1, commons.screen_h - commons.screen_h/20), commons.screen_w / 8, commons.screen_h / 12, 1000))
entities.buckets.append(Bucket(Vector(mid_x + shift1, commons.screen_h - commons.screen_h/20), commons.screen_w / 8, commons.screen_h / 12, 1000))

shift2 = commons.screen_w * (1/ 32 + 1 / 8 + 1/14)
entities.buckets.append(Bucket(Vector(mid_x - shift2, commons.screen_h - commons.screen_h/20), commons.screen_w / 7, commons.screen_h / 12, 100))
entities.buckets.append(Bucket(Vector(mid_x + shift2, commons.screen_h - commons.screen_h/20), commons.screen_w / 7, commons.screen_h / 12, 100))

shift3 = commons.screen_w * (1/ 32 + 1 / 8 + 1 / 7 + 1 / 10)
entities.buckets.append(Bucket(Vector(mid_x - shift3, commons.screen_h - commons.screen_h/20), commons.screen_w / 5, commons.screen_h / 12, 10))
entities.buckets.append(Bucket(Vector(mid_x + shift3, commons.screen_h - commons.screen_h/20), commons.screen_w / 5, commons.screen_h / 12, 10))

states.win_cond = [10, 10000, 10, 10, 10, 100]

while app_running:
    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app_running = False
            elif event.key == pygame.K_SPACE:
                entities.placed_pegs = []
        elif event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # if len(entities.balls) == 0:
                #     entities.balls.append(Ball(Vector(event.pos[0], event.pos[1]), Vector(0, 0)))
                # else:
                #     for b in entities.balls:
                #         d = dist(Vector(event.pos[0], event.pos[1]), b.position)
                #         if d > 2 * b.radius:
                #             print("Hello")
                if event.pos[1] < commons.screen_h / 7:
                    entities.balls.append(Ball(Vector(event.pos[0], event.pos[1]), Vector(0, 0)))
            elif event.button == pygame.BUTTON_RIGHT and states.peg_place:
                entities.placed_pegs.append(Peg(Vector(event.pos[0], event.pos[1])))


    update()
    draw()

    pygame.display.flip()

    commons.delta_time = 0.001 * clock.tick(144)

pygame.quit()
