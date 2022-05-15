from ball import Ball
from peg import Peg

balls = []
pegs = []
level_pegs = []

def update_balls():
    for i in range(len(balls) - 1, -1, -1):
        balls[i].update()
        if not balls[i].alive:
            balls.pop(i)

def draw_balls():
    for i in range(len(balls)):
        balls[i].draw()

def draw_pegs():
    for i in range(len(pegs)):
        pegs[i].draw()

    for i in range(len(level_pegs)):
        level_pegs[i].draw()
