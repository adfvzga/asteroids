import pygame
from modules.shot import Shot
from modules.constants import *
import random



class Bomb(Shot):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def explode(self):
        num_fragments = int(random.gauss(BOMB_FRAGMENTS_AVG, BOMB_FRAGMENTS_DIST_SIGMA))
        for i in range(0, num_fragments):
            shot = Shot(self.position.x, self.position.y, BOMB_FRAGMENT_RADIUS)
            shot.velocity = pygame.Vector2(0,1)
            shot.velocity = shot.velocity.rotate(random.randint(-180, 180))
            shot.velocity *= BOMB_FRAGMENT_SPEED + self.velocity.length() + random.randint(-50, 50)