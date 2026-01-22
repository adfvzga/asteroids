import pygame
from modules.circleshape import CircleShape
from modules.shot import Shot
from modules.constants import *
import random


class Player(CircleShape):
    def __init__(self, x, y, autocannon_snd, shotgun_snd):
        super().__init__(x,y,PLAYER_RADIUS)
        # Player position 
        self.rotation = 0
        self.speed = 0
        self.rotational_speed = 0
        self.autocannon_snd = autocannon_snd
        self.shotgun_snd = shotgun_snd

        # Armament
        self.autocannon_magazine = AUTOCANNON_MAGAZINE_CAPACITY
        self.shotgun_magazine = SHOTGUN_MAGAZINE_CAPACITY
        self.shotgun_cooldown = 0
        self.autocannon_reload_timer = 0 
        self.shotgun_reload_timer = 0

        # Player powerups
        self.shield_powerup = False

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "purple", self.triangle(), LINE_WIDTH)
        if self.shield_powerup is True:
            pygame.draw.circle(screen, "blue", self.position, SHIELD_RADIUS, LINE_WIDTH)

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

    def shoot_autocannon(self):
        if self.autocannon_magazine != 0:
            shot = Shot(self.position.x, self.position.y, AUTOCANNON_PROJECTILE_RADIUS)
            shot.velocity = pygame.Vector2(0,1)
            shot.velocity = shot.velocity.rotate(self.rotation)
            shot.velocity *= AUTOCANNON_PROJECTILE_SPEED + self.speed
            self.autocannon_magazine -= 1
            self.autocannon_snd.play()
        else:
            self.autocannon_reload_timer = AUTOCANNON_RELOAD_TIME_SECONDS
        
    def shoot_shotgun(self):
        if self.shotgun_magazine != 0:
                if self.shotgun_cooldown > 0:
                    pass
                else:
                    for i in range(0, SHOTGUN_PELLETS_PER_SHOT):
                        shot = Shot(self.position.x, self.position.y, SHOTGUN_PROJECTILE_RADIUS)
                        shot.velocity = pygame.Vector2(0,1)
                        shot.velocity = shot.velocity.rotate(self.rotation + random.randint(-25, 25))
                        shot.velocity *= SHOTGUN_PROJECTILE_SPEED + self.speed + random.randint(-50, 50)
                    self.shotgun_magazine -= 1
                    self.shotgun_cooldown = SHOTGUN_COOLDOWN_TIME_SECONDS
                    self.shotgun_snd.play()
        else:
            self.shotgun_reload_timer = SHOTGUN_RELOAD_TIME_SECONDS

    def update(self, dt):
        # Helper variables
        user_applying_rotational_acceleration = False
        user_applying_linear_acceleration = False

        # Update cooldown and reload timers
        self.shotgun_cooldown -= dt

        if self.autocannon_reload_timer > 0:
            self.autocannon_reload_timer -= dt
            if self.autocannon_reload_timer <= 0:
                self.autocannon_magazine = AUTOCANNON_MAGAZINE_CAPACITY

        if self.shotgun_reload_timer > 0:
            self.shotgun_reload_timer -= dt
            if self.shotgun_reload_timer <= 0:
                self.shotgun_magazine = SHOTGUN_MAGAZINE_CAPACITY

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
        if keys[pygame.K_j]:
            self.shoot_shotgun()
        if keys[pygame.K_SPACE]:
            self.shoot_autocannon()


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
