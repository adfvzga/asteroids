import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.rotational_speed = 0
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

    def accelerate_rotationally(self, dt):
        if dt > 0:
            if self.rotational_speed < PLAYER_MAX_ROTATION_SPEED:
                self.rotational_speed += PLAYER_ROTATIONAL_ACCELERATION * dt
            else:
                self.rotational_speed = PLAYER_ROTATIONAL_ACCELERATION
        else:
            if self.rotational_speed > -PLAYER_MAX_ROTATION_SPEED:
                self.rotational_speed += PLAYER_ROTATIONAL_ACCELERATION * dt
            else:
                self.rotational_speed = -PLAYER_ROTATIONAL_ACCELERATION

    def move(self, dt):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        movement_increment = rotated_vector * PLAYER_SPEED * dt
        
        # General position update
        self.position += movement_increment

        # X boundary condition check
        if self.position.x > SCREEN_WIDTH + 2 * self.radius:
            self.position.x -= SCREEN_WIDTH
        elif self.position.x < 0 - 2 * self.radius:
            self.position.x += SCREEN_WIDTH

        # Y boundary condition check
        if self.position.y > SCREEN_HEIGHT + 2 * self.radius:
            self.position.y -= SCREEN_HEIGHT
        elif self.position.y < 0 - 2 * self.radius:
            self.position.y += SCREEN_HEIGHT

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
        # Update the cooldown timer
        self.cooldown_timer -= dt

        # Check current player input and make adjustments
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.accelerate_rotationally(-dt)
        if keys[pygame.K_d]:
            self.accelerate_rotationally(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Calculate the current rotation
        self.rotation += self.rotational_speed * dt
