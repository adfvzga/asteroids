import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys



def main():
    # Environment setup
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    # Generate object containers 
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
     
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    dt = 0

    while(1):
        # Log game state at the beggining of each frame 
        log_state()

        # Check if the user wants to quit the game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            
        # Draw the screen
        screen.fill("black")

        # Update the positions of objects 
        updatable.update(dt)

        # Do collision detection on player vs asteroids
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # Do collision detection on asteroids vs shots
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        for drawable_item in drawable:
            drawable_item.draw(screen)
        pygame.display.flip()

        # Wait 1/60 of a second before proceeding with the new frame
        dt = clock.tick(60)/1000
 
if __name__ == "__main__":
    main()
