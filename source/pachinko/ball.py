
import commons
import vector
import images
import pygame
import numpy as np

from vector import *
from enum import Enum
from pygame.locals import *
import entities
import states

class BallType(Enum):
    DEFAULT = 0


class Ball:
    def __init__(self, position: Vector, velocity: Vector = Vector(0, 0), radius: float = 22,
                 ball_type: BallType = BallType.DEFAULT, image: pygame.Surface = None):

        self.position = vector.copy(position)
        self.velocity = vector.copy(velocity)

        self.radius = radius
        self.diameter = radius * 2.0

        self.ball_type = BallType(ball_type)

        self.image = image
        if self.image is None:
            self.image = images.ball_default

        self.bounding_box = Rect(0, 0, 1, 1)
        self.alive = True

    def update(self):
        self.velocity.y += commons.delta_time * commons.gravity
        self.position += self.velocity * commons.delta_time

        self.check_screen_collisions()

    def draw(self):
        top_left_position = self.position - self.radius
        commons.screen.blit(self.image, top_left_position.make_int_tuple())

    def check_screen_collisions(self):
        if self.position.x < self.radius or self.position.x > commons.screen_w - self.radius:
            self.velocity.x = -self.velocity.x

        if self.position.y < self.radius:
            self.velocity.y = -self.velocity.y
        elif self.position.y > commons.screen_h + self.radius:

            for b in entities.buckets:
                if b.in_bucket(self.position):
                    states.score += b.value

                    if states.win_cond[len(states.prev_scores)] == b.value:
                        if len(states.prev_scores) < len(states.win_cond):
                            states.prev_scores.append(b.value)
                            if len(states.prev_scores) == len(states.win_cond):
                                states.win = True
                    else:
                        states.prev_scores = []

            self.alive = False

        # for b in entities.balls:
        #     if b != self:
        #         d = dist(self.position, b.position)
        #         if d - self.radius <= b.radius:
        #             deltanorm = (self.position - b.position) / d
        #             self.position = self.position + deltanorm * (b.radius - (d - self.radius) + .1)
        #
        #             self.velocity = (self.velocity - deltanorm * (2 * (dot(deltanorm, self.velocity)))) * (.695 + np.random.uniform(-.1, .1))
        #             b.velocity = (b.velocity + deltanorm * (2 * (dot(deltanorm, self.velocity)))) * (.695 + np.random.uniform(-.1, .1))

        for p in entities.placed_pegs:
            d = dist(self.position, p.position)
            if d - self.radius <= p.radius:
                deltanorm = (self.position - p.position) / d
                self.position = self.position + deltanorm * (p.radius - (d - self.radius) + .1)
                self.velocity = (self.velocity - deltanorm * (2 * (dot(deltanorm, self.velocity)))) * (.695 + np.random.uniform(-.1, .1))

        for p in entities.level_pegs:
            d = dist(self.position, p.position)
            if d - self.radius <= p.radius:
                deltanorm = (self.position - p.position) / d
                self.position = self.position + deltanorm * (p.radius - (d - self.radius) + .1)
                self.velocity = (self.velocity - deltanorm * (2 * (dot(deltanorm, self.velocity)))) * (.695 + np.random.uniform(-.1, .1))

                if p.peg_type == 1:
                    p.peg_type = 0
                    p.image = pygame.image.load("res/images/pegs/28x28/lit_yellow_peg.png")
                    states.pegs_revealed -= 1
                    if states.pegs_revealed == 0:
                        states.peg_place = True
