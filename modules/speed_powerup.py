import pygame
from modules.circleshape import CircleShape
from modules.constants import *
from modules.asteroid import *
from modules.logger import *
import random


class SpeedPowerUP(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "green", self.position, self.radius, LINE_WIDTH)
            