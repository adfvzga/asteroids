import pygame
from modules.circleshape import CircleShape
from modules.constants import *


class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x,y,radius)
        # Shot allowed to wrap around the screen, but only once
        # otherwise the thing turns into a total shitshow
        self.crossed_screen_boundary_once = 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        # General position update
        self.position += self.velocity * dt

        # X boundary condition check
        if self.position.x > SCREEN_WIDTH + 2 * self.radius:
            if self.crossed_screen_boundary_once == 0:
                self.position.x -= SCREEN_WIDTH
                self.crossed_screen_boundary_once = 1
            else:
                self.kill()
        elif self.position.x < 0 - 2 * self.radius:
            if self.crossed_screen_boundary_once == 0:
                self.position.x += SCREEN_WIDTH
                self.crossed_screen_boundary_once = 1
            else:
                self.kill()

        # Y boundary condition check
        if self.position.y > SCREEN_HEIGHT + 2 * self.radius:
            if self.crossed_screen_boundary_once == 0:        
                self.position.y -= SCREEN_HEIGHT
                self.crossed_screen_boundary_once = 1
            else:
                self.kill()             
        elif self.position.y < 0 - 2 * self.radius:
            if self.crossed_screen_boundary_once == 0:
                self.position.y += SCREEN_HEIGHT
                self.crossed_screen_boundary_once = 1
            else:
                self.kill()
