"""
PLAN:
- Week 1, Use pygame.
- Week 2, Try out Godot.
"""

import pygame
import sys

game_width = 1500
game_height = 1000

def check_vertical_landing(player, platform, velocity_n):
    ground_check = player.move(0, 1)
    if ground_check.colliderect(platform):
        velocity_n = 0
        player.y = platform[1] - 20
        grounded = True
    else:
        velocity_n -= gravity
        grounded = False
    return player, velocity_n, grounded

pygame.init()

screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Parkour")
clock = pygame.time.Clock()
game_surface = pygame.Surface((game_width, game_height))
screen_colour = (0, 15, 135)
board_colour = (153, 81, 0)

player_colour = (0, 135, 6)

velocity_n = -1
gravity = 1
jump_strength = 15

player = pygame.Rect(500, 800, 20, 20)
floor = pygame.Rect(0, 900, 1500, 100)
ceiling = pygame.Rect(0, 0, 1500, 100)
platform1 = pygame.Rect(700, 850, 50, 10)


running = True

while running:
    screen.fill(screen_colour) # background

    player.y -= velocity_n

    player, velocity_n, grounded = check_vertical_landing(player, floor, velocity_n)
    if not grounded:
        player, velocity_n, grounded = check_vertical_landing(player, platform1, velocity_n)

    if player.colliderect(ceiling):
        velocity_n = 0
        player.y = 100


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
            if event.key == pygame.K_w and grounded:
                velocity_n += jump_strength
                grounded = False

    
    # Get the state of all keys
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        player.x -= 3

    if keys[pygame.K_d]:
        player.x += 3

    
    pygame.draw.rect(screen, player_colour, player)
    floor = pygame.Rect(0, 900, 1500, 100)
    pygame.draw.rect(screen, board_colour, floor)
    ceiling = pygame.Rect(0, 0, 1500, 100)
    pygame.draw.rect(screen, board_colour, ceiling)
    platform1 = pygame.Rect(700, 850, 50, 10)
    pygame.draw.rect(screen, board_colour, platform1)
    clock.tick(60)
    pygame.display.flip()