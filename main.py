import pygame
import sys

from pathlib import Path
from random import randint


# screen resolution
RES_X = 800
RES_Y = 600
BG_COLOR = (32, 52, 71)

# images paths
SPACESHIP_PATH = Path('./images/spaceship.png')
ALIEN_PATH = Path('./images/alien.png')
FIREBALL_PATH = Path('./images/fireball.png')

SPACESHIP_STEP_X = 10
FIREBALL_STEP_Y = 0.3
alien_step_y = 0.03

pygame.init()
killed = 0
game_font = pygame.font.Font(None, 30)

screen = pygame.display.set_mode((RES_X, RES_Y))
pygame.display.set_caption('Alien vs Cosmoboy')
pygame.key.set_repeat(300, 10)

# while not game over
is_game = True

spaceship_image = pygame.image.load(SPACESHIP_PATH)
spaceship_width, spaceship_height = spaceship_image.get_size()
spaceship_x = (RES_X - spaceship_width) / 2
spaceship_y = RES_Y - spaceship_height

fireball_image = pygame.image.load(FIREBALL_PATH)
fireball_width, fireball_height = fireball_image.get_size()
fireball_x, fireball_y = 0.0, 0.0

# while fireball is visible
is_fireball = False

alien_image = pygame.image.load(ALIEN_PATH)
alien_width, alien_height = alien_image.get_size()
alien_x, alien_y = randint(0, RES_X - alien_width), 0.0

# while alien is visible
is_alien = True

alien2_x = randint(0, RES_X - alien_width)
alien2_y = -alien_height / 2.0
# while alien 2 is visible
is_alien2 = True


while is_game:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_LEFT:
                spaceship_x -= SPACESHIP_STEP_X
            if key == pygame.K_RIGHT:
                spaceship_x += SPACESHIP_STEP_X
            if key == pygame.K_SPACE:
                is_fireball = True
                fireball_x = (
                    spaceship_x + (spaceship_width - fireball_width) / 2.0)
                fireball_y = spaceship_y - fireball_height

            if spaceship_x + spaceship_width > RES_X:
                spaceship_x = RES_X - spaceship_width
            if spaceship_x < 0:
                spaceship_x = 0

    killed_text = game_font.render(f'Killed: {killed}', True, 'white')
    screen.blit(killed_text, (20, 20))

    screen.blit(spaceship_image, (spaceship_x, spaceship_y))

    alien_y += alien_step_y
    alien2_y += alien_step_y

    if is_fireball:
        screen.blit(fireball_image, (fireball_x, fireball_y))
        fireball_y -= FIREBALL_STEP_Y
    if is_alien:
        screen.blit(alien_image, (alien_x, alien_y))

    if is_alien2:
        screen.blit(alien_image, (alien2_x, alien2_y))

    pygame.display.update()

    if alien_y + alien_height >= spaceship_y:
        is_game = False

    if alien2_y + alien_height >= spaceship_y:
        is_game = False

    if (is_fireball and
            (alien_x < fireball_x < alien_x + alien_width - fireball_width and
             alien_y < fireball_y < alien_y + alien_height - fireball_height)):
        is_fireball = False
        alien_x, alien_y = randint(0, RES_X - alien_width), 0
        killed += 1
        if killed % 5 == 0:
            alien_step_y += 0.01

    if (is_fireball and
            (alien2_x < fireball_x < alien2_x + alien_width -
             fireball_width and
             alien2_y < fireball_y < alien2_y + alien_height -
             fireball_height)):
        is_fireball = False
        alien2_x, alien2_y = randint(0, RES_X - alien_width), 0
        killed += 1
        if killed % 5 == 0:
            alien_step_y += 0.01


game_over_text = game_font.render('Game Over', True, 'white')
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (int(RES_X / 2), int(RES_Y / 2))
screen.blit(game_over_text, game_over_rect)
pygame.display.update()
pygame.time.wait(5000)
pygame.quit()
