"""
PLAN:
- Add proper hitboxes for left/right side of a platform.
- Then learn and set up git
- Add a starting platform and ascending things over lava
- I need a way to (possibly) iterate through every platform to see if anything is colliding with the player. 
"""

import pygame
import sys

game_width = 1500
game_height = 1000

def check_vertical_landing(player, platform, velocity): # hitting roof / touching floor
    if player.colliderect(platform) == False:
        return player, velocity, False
    if velocity < 0:
        player.bottom = platform.top
        velocity = 0
        return player, velocity, True

    elif velocity > 0:
        player.top = platform.bottom
        velocity = 0

    return player, velocity, False

def check_horizontal_landing(player, platform, blocked_left, blocked_right): # hitting wall to the side.
    left_check = player.move(-1, 0) # think critically about this design.
    if left_check.colliderect(platform):
        player.left = platform.right
        blocked_left = True
        print('left')
    else:
        blocked_left = False

    
    right_check = player.move(1, 0)
    if right_check.colliderect(platform):
        player.right = platform.left
        blocked_right = True
        print('right')
    else:
        blocked_right = False

    return player, blocked_left, blocked_right

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

player = pygame.Rect(100, 400, 40, 40)

floor = pygame.Rect(0, 900, 1500, 100)
wallleft = pygame.Rect(0, 0, 50, 1000)
wallright = pygame.Rect(1450, 0, 50, 1000)
platform1 = pygame.Rect(700, 850, 50, 10)

ceiling = pygame.Rect(0, 0, 1500, 100)

running = True
grounded = False
blocked_left = False
blocked_right = False

while running:
    screen.fill(screen_colour) # background

    player.y -= velocity

    player, velocity, grounded = check_vertical_landing(player, floor, velocity)
    if not grounded:
        player, velocity, grounded = check_vertical_landing(player, platform1, velocity)
    if not grounded:
        velocity -= gravity
    
    player, blocked_left, blocked_right = check_horizontal_landing(player, wallleft, blocked_left, blocked_right)
    player, blocked_left, blocked_right = check_horizontal_landing(player, wallright, blocked_left, blocked_right)
    player, blocked_left, blocked_right = check_horizontal_landing(player, platform1, blocked_left, blocked_right)



    if player.colliderect(ceiling):
        velocity = 0
        player.y = 100


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
    
    if keys[pygame.K_a] and not blocked_left:
        player.x -= 3

    if keys[pygame.K_d] and not blocked_right:
        player.x += 3

    
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