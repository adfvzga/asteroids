import pygame
import random
from modules.asteroid import Asteroid
from modules.speed_powerup import SpeedPowerUP
from modules.shield_powerup import ShieldPowerUp
from modules.constants import *



class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.asteroid_spawn_timer = 0.0
        self.shield_powerup_spawn_timer = 0.0
        self.speed_powerup_spawn_timer = 0.0

    def spawn(self, object_type):
        # Spawn a new object at a random edge
        edge = random.choice(self.edges)
        speed = random.randint(40, 100)
        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        position = edge[1](random.uniform(0, 1))
        kind = random.randint(1, ASTEROID_SIZES)

        if object_type == "asteroid":
            asteroid = Asteroid(position.x, position.y, ASTEROID_MIN_RADIUS * kind)
            asteroid.velocity = velocity

        if object_type == "speed_powerup":
            speed_powerup = SpeedPowerUP(position.x, position.y, ASTEROID_MIN_RADIUS * kind)
            speed_powerup.velocity = velocity

        if object_type == "shield_powerup":
            shield_powerup = ShieldPowerUp(position.x, position.y, ASTEROID_MIN_RADIUS * kind)
            shield_powerup.velocity = velocity

    def update(self, dt):
        self.asteroid_spawn_timer += dt
        self.speed_powerup_spawn_timer += dt
        self.shield_powerup_spawn_timer += dt

        if self.asteroid_spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.asteroid_spawn_timer = 0
            self.spawn("asteroid")

        if self.speed_powerup_spawn_timer > SPEED_POWERUP_GENERAL_SPAWN_RATE_SECONDS:
            self.speed_powerup_spawn_timer = 0
            self.spawn("speed_powerup")

        if self.shield_powerup_spawn_timer > SHIELD_POWERUP_GENERAL_SPAWN_RATE_SECONDS:
            self.shield_powerup_spawn_timer = 0
            self.spawn("shield_powerup")
