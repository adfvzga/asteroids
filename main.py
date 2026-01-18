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
    font = pygame.font.Font(None, 36)

    # Load the background picture
    background_surface = pygame.image.load('background_image.png')

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

    # Gameplay variables
    player_score = 0
    player_lives = 3

    while(1):
        # Log game state at the beggining of each frame 
        log_state()

        # Check if the user wants to quit the game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 

        # Update the positions of objects 
        updatable.update(dt)

        # Do collision detection on player vs asteroids
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if player_lives == 1:
                    log_event("player_hit")
                    print("Game over!")
                    sys.exit()
                else:
                    player_lives -= 1
                    for asteroid in asteroids:
                        asteroid.kill()
                    player.rotation = 0
                    player.rotational_speed = 0
                    player.position.x = SCREEN_WIDTH/2
                    player.position.y = SCREEN_HEIGHT/2
                    player.speed = 0
                    # print("lost life") # DEBUG ONLY

        # Do collision detection on asteroids vs shots
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    player_score += 1
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        # Draw the screen
        screen.blit(background_surface, (0, 0))

        # Draw drawable stuff 
        for drawable_item in drawable:
            drawable_item.draw(screen)
        
        # Draw score and lives
        score_surface = font.render(f"Score: {player_score}", True, (255, 255, 255))
        lives_surface = font.render(f"Lives: {player_lives}", True, (255, 255, 255))
        player_speed_surface = font.render(f"Player speed: {player.speed:.2f}", True, (255, 255, 255))
        player_rotational_speed_surface = font.render(f"Player rotational speed: {player.rotational_speed:.2f}", True, (255, 255, 255))
        screen.blit(score_surface, (20, 20))
        screen.blit(lives_surface, (20, 50))
        screen.blit(player_speed_surface, (20, 80))
        screen.blit(player_rotational_speed_surface, (20, 110))

        # Update the screen 
        pygame.display.flip()

        # Wait 1/60 of a second before proceeding with the new frame
        dt = clock.tick(60)/1000
 
if __name__ == "__main__":
    main()
