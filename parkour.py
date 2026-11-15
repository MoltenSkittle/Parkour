"""
PLAN:
- Add a starting platform and ascending things over lava
"""

import pygame
import sys

game_width = 1500
game_height = 1000

def check_vertical_landing(player, platform, velocity): # hitting roof / touching floor

    horizontal_overlap = (player.right > platform.left and player.left < platform.right)
    if horizontal_overlap and player.bottom == platform.top:
        return player, 0, True

    if player.colliderect(platform) == False:
        return player, velocity, False

    # Hit bottom of platform when jumping
    if player.colliderect(platform) and velocity > 0:
        player.top = platform.bottom
        velocity = 0
        return player, velocity, False

    # Landed on top
    if player.colliderect(platform) and velocity < 0:
        player.bottom = platform.top
        velocity = 0
        return player, velocity, True

def check_horizontal_landing(player, platform, direction): # hitting wall to the side.

    if player.colliderect(platform) and direction == "left":
        player.left = platform.right

    if player.colliderect(platform) and direction == "right":
        player.right = platform.left

    return player

pygame.init()

screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Parkour")
clock = pygame.time.Clock()
game_surface = pygame.Surface((game_width, game_height))
screen_colour = (0, 15, 135)
wall_colour = (153, 81, 0)

player_colour = (0, 135, 6)

velocity = 0
gravity = 1
jump_strength = 22
move_speed = 5

player = pygame.Rect(100, 400, 40, 40)

floor = pygame.Rect(0, 900, 1500, 100)
wallleft = pygame.Rect(0, 0, 50, 1000)
wallright = pygame.Rect(1450, 0, 50, 1000)
platform1 = pygame.Rect(700, 850, 50, 10)
ceiling = pygame.Rect(0, 0, 1500, 100)


platforms = [
    floor, 
    wallleft, 
    wallright, 
    platform1, 
    ceiling
    ]

running = True
blocked_left = False
blocked_right = False

while running:
    screen.fill(screen_colour) # background

    player.y -= velocity

    grounded = False

    for platform in platforms:
        player, velocity, landed = check_vertical_landing(player, platform, velocity)
        if landed:
            grounded = True

    if not grounded:
        velocity -= gravity

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
            if event.key == pygame.K_w and grounded:
                velocity += jump_strength
                grounded = False

    
    # Get the state of all keys
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        player.x -= move_speed

        for platform in platforms:
            player = check_horizontal_landing(player, platform, "left")

    if keys[pygame.K_d]:
        player.x += move_speed
        
        for platform in platforms:
            player = check_horizontal_landing(player, platform, "right")

    
    floor = pygame.Rect(0, 900, 1500, 100)
    pygame.draw.rect(screen, wall_colour, floor)
    ceiling = pygame.Rect(0, 0, 1500, 100)
    pygame.draw.rect(screen, wall_colour, ceiling)
    platform1 = pygame.Rect(700, 850, 50, 10)
    pygame.draw.rect(screen, wall_colour, platform1)
    pygame.draw.rect(screen, wall_colour, wallleft)
    pygame.draw.rect(screen, wall_colour, wallright)
    pygame.draw.rect(screen, player_colour, player)
    clock.tick(60)
    pygame.display.flip()