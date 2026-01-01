import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "purple", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        movement_increment = rotated_vector * PLAYER_SPEED * dt
        # X cordinate update 
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x -= SCREEN_WIDTH
        elif self.position.x < 0 - self.radius:
            self.position.x += SCREEN_WIDTH
        else:
            self.position.x += movement_increment.x

        # Y cordinate update 
        if self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y -= SCREEN_HEIGHT
        elif self.position.y < 0 - self.radius:
            self.position.y += SCREEN_HEIGHT
        else:
            self.position.y += movement_increment.y

    def shoot(self):
        if (self.cooldown_timer > 0):
            pass
        else:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0,1)
            shot.velocity = shot.velocity.rotate(self.rotation)
            shot.velocity *= PLAYER_SHOOT_SPEED
            self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

    def update(self, dt):
        self.cooldown_timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
