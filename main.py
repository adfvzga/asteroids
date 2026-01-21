import pygame
from modules.constants import *
from modules.logger import log_state, log_event
from modules.player import Player
from modules.asteroid import Asteroid
from modules.asteroidfield import AsteroidField
from modules.shot import Shot
import sys
import os



def main():
    # Environment setup
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize all relevant modules
    pygame.init()
    if "SDL_AUDIODRIVER" not in os.environ:
        os.environ["SDL_AUDIODRIVER"] = "pulse" 
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)
    font = pygame.font.Font(None, 36)

    # Load the background picture
    background_surface = pygame.image.load('images/background_image.png')

    # Load the sounds
    autocannon_snd = pygame.mixer.Sound("sounds/autocannon.wav")
    shotgun_snd = pygame.mixer.Sound("sounds/shotgun.mp3")

    autocannon_snd.set_volume(0.25)
    shotgun_snd.set_volume(0.35)

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
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, autocannon_snd, shotgun_snd)
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
                    player.autocannon_magazine = AUTOCANNON_MAGAZINE_CAPACITY
                    player.shotgun_magazine = SHOTGUN_MAGAZINE_CAPACITY
                    player.autocannon_reload_timer = 0
                    player.shotgun_reload_timer = 0

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
        player_speed_surface = font.render(f"LIN SPD: {player.speed:.2f}", True, (255, 255, 255))
        player_rotational_speed_surface = font.render(f"ROT SPD: {player.rotational_speed:.2f}", True, (255, 255, 255))
        if player.autocannon_magazine > 0:
            autocannon_rounds_surface = font.render(f"ATCN: {player.autocannon_magazine}", True, (144, 238, 144))
        else:
            autocannon_rounds_surface = font.render(f"RELOADING ATCN: {player.autocannon_reload_timer:.0f}", True, (255, 165, 0))
        if player.shotgun_magazine > 0:  
            shotgun_rounds_surface = font.render(f"SHTGN: {player.shotgun_magazine}", True, (144, 238, 144))
        else:
            shotgun_rounds_surface = font.render(f"RELOADING SHTGN: {player.shotgun_reload_timer:.0f}", True, (255, 165, 0))
        screen.blit(score_surface, (20, 20))
        screen.blit(lives_surface, (20, 50))
        screen.blit(player_speed_surface, (20, 80))
        screen.blit(player_rotational_speed_surface, (20, 110))
        screen.blit(autocannon_rounds_surface, (20, 140))
        screen.blit(shotgun_rounds_surface, (20, 170))

        # Update the screen 
        pygame.display.flip()

        # Wait 1/60 of a second before proceeding with the new frame
        dt = clock.tick(60)/1000
 
if __name__ == "__main__":
    main()
