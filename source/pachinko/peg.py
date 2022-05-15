import commons
import vector
import images
import pygame

from vector import Vector
from enum import Enum
from pygame.locals import *

class PegType(Enum):
    DEFAULT = 0

class Peg:
    def __init__(self, position: Vector, radius: float = 14,
                 peg_type: PegType = PegType.DEFAULT, image: pygame.Surface = None):

        self.position = vector.copy(position)

        self.radius = radius
        self.diameter = radius * 2.0

        self.peg_type = PegType(peg_type)

        self.image = image
        if self.image is None:
            self.image = images.peg_default

        self.bounding_box = Rect(0, 0, 1, 1)

    def draw(self):
        top_left_position = self.position - self.radius
        commons.screen.blit(self.image, top_left_position.make_int_tuple())
