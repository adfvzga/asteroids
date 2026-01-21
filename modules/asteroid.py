import pygame
from modules.circleshape import CircleShape
from modules.constants import *
from modules.asteroid import *
from modules.logger import *
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius == ASTEROID_MIN_RADIUS:
            # If asteroid already the smallest one just return 
            return
        else:
            # Else split into two smaller ones
            log_event("asteroid_split")
            split_angle = random.uniform(20,50)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_velocity1 = self.velocity.rotate(split_angle)
            new_velocity2 = self.velocity.rotate(-split_angle)
            new_asteroid1 = Asteroid(self.position.x,self.position.y,new_radius)
            new_asteroid2 = Asteroid(self.position.x,self.position.y,new_radius)
            new_asteroid1.velocity = 1.2 * new_velocity1
            new_asteroid2.velocity = 1.2 * new_velocity2
            