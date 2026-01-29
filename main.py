import pygame
from modules.constants import *
from modules.logger import log_state, log_event
from modules.player import Player
from modules.asteroid import Asteroid
from modules.asteroidfield import AsteroidField
from modules.shot import Shot
from modules.bomb import Bomb
from modules.shield_powerup import ShieldPowerUp
from modules.speed_powerup import SpeedPowerUP
import sys
import os
import time



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
    bomb_snd = pygame.mixer.Sound("sounds/bomb.mp3")
    shield_powerup_snd = pygame.mixer.Sound("sounds/shield_powerup.mp3")
    speed_powerup_snd = pygame.mixer.Sound("sounds/speed_powerup.mp3")
    lost_life_snd = pygame.mixer.Sound("sounds/lost_life.mp3")
    lost_game_snd = pygame.mixer.Sound("sounds/game_lost.mp3")
    pygame.mixer.music.load("sounds/background_music.mp3")

    # Configure the sounds 
    autocannon_snd.set_volume(0.25)
    shotgun_snd.set_volume(0.35)
    bomb_snd.set_volume(0.6)
    shield_powerup_snd.set_volume(0.5)
    speed_powerup_snd.set_volume(0.5)
    lost_life_snd.set_volume(0.15)
    lost_game_snd.set_volume(0.25)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    # Generate object containers 
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    speed_powerups = pygame.sprite.Group()
    shield_powerups = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    SpeedPowerUP.containers = (speed_powerups, updatable, drawable)
    ShieldPowerUp.containers = (shield_powerups, updatable, drawable)
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

        # Do collision detection on asteroids
        for asteroid in asteroids:
            # Asteroids vs player
            if player.shield_powerup_timer > 0:
                pass
            else: 
                if asteroid.collides_with(player):
                    if player_lives == 1:
                        log_event("player_hit")
                        print("Game over!")
                        lost_game_snd.play()
                        time.sleep(1.5)
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
                        player.bomb_magazine = BOMB_MAGAZINE_CAPACITY
                        player.autocannon_reload_timer = 0
                        player.shotgun_reload_timer = 0
                        player.bomb_reload_timer = 0
                        lost_life_snd.play()

            # Asteroids vs shots
            for shot in shots:
                if asteroid.collides_with(shot):
                    player_score += 1
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    if isinstance(shot, Bomb):
                        shot.explode()
                        bomb_snd.play()

        # Do collision detection on speed powerups
        for speed_powerup in speed_powerups:
            # Speed powerups vs player
            if speed_powerup.collides_with(player):
                speed_powerup.kill()
                speed_powerup_snd.play()
                player.speed_powerup_timer = SPEED_POWERUP_ACTIVE_TIME_SECONDS
            # Speed powerups vs shots
            for shot in shots:
                if speed_powerup.collides_with(shot):
                    shot.kill()
                    speed_powerup.kill()
                    speed_powerup_snd.play()
                    player.speed_powerup_timer = SPEED_POWERUP_ACTIVE_TIME_SECONDS

        # Do collision detection on shield powerups
        for shield_powerup in shield_powerups:
            # Speed powerups vs player
            if shield_powerup.collides_with(player):
                shield_powerup.kill()
                shield_powerup_snd.play()
                player.shield_powerup_timer = SHIELD_POWERUP_ACTIVE_TIME_SECONDS
            # Speed powerups vs shots
            for shot in shots:
                if shield_powerup.collides_with(shot):
                    shot.kill()
                    shield_powerup.kill()
                    shield_powerup_snd.play()
                    player.shield_powerup_timer = SHIELD_POWERUP_ACTIVE_TIME_SECONDS

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
        if player.bomb_magazine > 0:  
            bombs_surface = font.render(f"BMBS: {player.bomb_magazine}", True, (144, 238, 144))
        else:
            bombs_surface = font.render(f"RELOADING BMBS: {player.bomb_reload_timer:.0f}", True, (255, 165, 0))
        screen.blit(score_surface, (20, 20))
        screen.blit(lives_surface, (20, 50))
        screen.blit(player_speed_surface, (20, 80))
        screen.blit(player_rotational_speed_surface, (20, 110))
        screen.blit(autocannon_rounds_surface, (20, 140))
        screen.blit(shotgun_rounds_surface, (20, 170))
        screen.blit(bombs_surface, (20, 200))

        # Update the screen 
        pygame.display.flip()

        # Wait 1/60 of a second before proceeding with the new frame
        dt = clock.tick(60)/1000
 
if __name__ == "__main__":
    main()
