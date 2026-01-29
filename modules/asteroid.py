import pygame
from modules.circleshape import CircleShape
from modules.constants import *
from modules.asteroid import *
from modules.logger import *
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)
        self.shape = self.generate_shape()

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.update_shape(), LINE_WIDTH)

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

    def generate_shape(self):
        num_vertices = max(3, int(random.gauss(ASTEROID_AVG_VERTICES, ASTEROID_VERTICES_SIGMA)))
        base_rotation_angle = 360 / num_vertices

        vertex_list = []
        for i in range(num_vertices):
            rotation_angle = i * base_rotation_angle + random.randint(-10, 10)
            v = pygame.Vector2(0, self.radius).rotate(rotation_angle)
            vertex_list.append(v)
        return vertex_list
    
    def update_shape(self):
        new_verteces = []
        for vertex in self.shape:
           new_verteces.append(vertex + self.position)
        return new_verteces
