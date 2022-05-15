import commons
import vector
import images
import pygame
import numpy as np

from peg import *
from vector import *
from enum import Enum
from pygame.locals import *
import entities
import states

class Bucket:
    def __init__(self, position: Vector, width: float = 150, height: float = 28, value: float = 0,
                 image: pygame.Surface = None):

        self.position = vector.copy(position)
        self.value = value
        self.width = width
        self.height = height

        self.image = image
        if self.image is None:
            self.image = images.bucket_default

        self.top_left = position - Vector(width / 2, height / 2)
        self.top_right = position + Vector(width / 2, -height / 2)

        self.left_wall = []
        self.right_wall = []

        for y in np.linspace(self.top_left.y, commons.screen_h, 5):
            peg = Peg(Vector(self.top_left.x, y))
            entities.level_pegs.append(peg)
            self.left_wall.append(peg)
        for y in np.linspace(self.top_right.y, commons.screen_h, 5):
            peg = Peg(Vector(self.top_right.x, y))
            entities.level_pegs.append(peg)
            self.right_wall.append(peg)

    def in_bucket(self, position):
        if position.x > self.top_left.x and position.x < self.top_right.x:
            return True
        return False

    def draw(self):
        for peg in self.left_wall:
            peg.draw()
        for peg in self.right_wall:
            peg.draw()

        text_surface, rect = commons.font.render(f"{self.value}", (255, 192, 200))
        commons.screen.blit(text_surface, self.position.make_int_tuple())
