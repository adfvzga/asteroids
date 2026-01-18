import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.speed = 0
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
                self.rotational_speed = PLAYER_MAX_ROTATION_SPEED
        else:
            if self.rotational_speed > -PLAYER_MAX_ROTATION_SPEED:
                self.rotational_speed += PLAYER_ROTATIONAL_ACCELERATION * dt
            else:
                self.rotational_speed = -PLAYER_MAX_ROTATION_SPEED

    def accelerate_linearly(self, dt):
        if dt > 0:
            if self.speed < PLAYER_MAX_SPEED:
                self.speed += PLAYER_LINEAR_ACCELERATION * dt
            else:
                self.speed = PLAYER_MAX_SPEED
        else:
            if self.speed > -PLAYER_MAX_SPEED:
                self.speed += PLAYER_LINEAR_ACCELERATION * dt
            else:
                self.speed = -PLAYER_MAX_SPEED

    def shoot(self):
        if (self.cooldown_timer > 0):
            pass
        else:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0,1)
            shot.velocity = shot.velocity.rotate(self.rotation)
            shot.velocity *= PLAYER_SHOOT_SPEED + self.speed
            self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

    def update(self, dt):
        # Helper variables
        user_applying_rotational_acceleration = False
        user_applying_linear_acceleration = False
        # Update the cooldown timer
        self.cooldown_timer -= dt

        # Check current player input and make adjustments
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.accelerate_rotationally(-dt)
            user_applying_rotational_acceleration = True
        if keys[pygame.K_d]:
            self.accelerate_rotationally(dt)
            user_applying_rotational_acceleration = True
        if keys[pygame.K_w]:
            self.accelerate_linearly(dt)
            user_applying_linear_acceleration = True 
        if keys[pygame.K_s]:
            self.accelerate_linearly(-dt)
            user_applying_linear_acceleration = True 
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Calculate the current rotation
        # Take environmental drag into account
        if user_applying_rotational_acceleration is False: 
            self.rotational_speed *= PLAYER_ROTATIONAL_DRAG_DECELEARTION_COEFFICIENT
        self.rotation += self.rotational_speed * dt

        # Calculate the current position
        # Take environmental drag into account
        if user_applying_linear_acceleration is False:
            self.speed *= PLAYER_LINEAR_DRAG_DECELERATION_COEFFICIENT
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_vector *= self.speed
        self.position += rotated_vector * dt

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
