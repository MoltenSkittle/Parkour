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
lava_colour = (173, 30, 0)
player_colour = (0, 135, 6)
death_screen_colour = (255, 243, 208)
blue = (42, 116, 255)
red = (204, 0, 0)
green = (0, 176, 48)
gold_yellow = (245, 204, 3)

black = (0, 0, 0)
p_main_font = pygame.font.SysFont('calibri', 70)

d_main_text = p_main_font.render("You Died!", True, black)
d_button_font = pygame.font.SysFont('calibri', 55)
d_playagain_text = d_button_font.render("Play Again", True, black)
d_quit_text = d_button_font.render("Quit", True, black)

w_main_text = p_main_font.render("You Win!", True, black)
w_button_font = pygame.font.SysFont('calibri', 45)
w_playagain_text = w_button_font.render("Play Again", True, black)
w_quit_text = w_button_font.render("Quit", True, black)
w_nextlevel_text = w_button_font.render("Next Level", True, black)



velocity = 0
gravity = 1
jump_strength = 12
move_speed = 5

# Starting Screen (NOT ADDED YET)

# Win Screen
w_playagain_button = pygame.Rect(300, 650, 233, 100)
w_quit_button = pygame.Rect(633, 650, 233, 100)
w_nextlevel_button = pygame.Rect(967, 650, 233, 100)


# Death Screen
death_screen = pygame.Rect(200, 200, 1100, 600)
d_playagain_button = pygame.Rect(300, 650, 400, 100)
d_quit_button = pygame.Rect(800, 650, 400, 100)


# Game Screen Starts Here
# Player
player = pygame.Rect(80, 400, 25, 25)

# Platforms
floor = pygame.Rect(0, 950, 1500, 50)
wallleft = pygame.Rect(0, 0, 50, 1000)
wallright = pygame.Rect(1450, 0, 50, 1000)

platform1 = pygame.Rect(0, 850, 135, 150)
platform2 = pygame.Rect(200, 820, 50, 10)
platform3 = pygame.Rect(315, 790, 50, 10)
platform4 = pygame.Rect(430, 760, 50, 10)
platform5 = pygame.Rect(560, 730, 50, 10)
platform6 = pygame.Rect(590, 670, 50, 10)
platform7 = pygame.Rect(620, 610, 50, 10)
platform8 = pygame.Rect(720, 580, 50, 10)
platform9 = pygame.Rect(820, 550, 50, 10)
platform10 = pygame.Rect(940, 520, 50, 10)
platform11 = pygame.Rect(1040, 480, 50, 10)
platform12 = pygame.Rect(1180, 440, 50, 10)
platform13 = pygame.Rect(1300, 380, 50, 10)
platform14 = pygame.Rect(1400, 310, 50, 10)

ceiling = pygame.Rect(0, 0, 1500, 100)

platforms = [
    floor, 
    wallleft, 
    wallright,  
    platform1,  platform2, platform3, platform4, platform5, platform6, platform7, platform8, platform9, platform10, platform11, platform12, platform13, platform14, 
    ceiling
    ]

# Winning Coin (Uses rectangular hitbox)
coin1 = pygame.Rect(1415, 265, 20, 20)

# Lava
lava = pygame.Rect(0, 900, 1500, 50)
# Game Screen Ends Here

running = True
blocked_left = False
blocked_right = False
game_active = True
alive = True
win = False

# Game Loop
running = True
while running:


    if not game_active and not alive:
        # Player is not in a game right now; on loading screen

        # Handling exiting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


    if not game_active and alive: 
        # Pause Screen
        
        # Handling exiting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    if game_active and alive and win:
        pygame.draw.circle(screen, screen_colour, (1425, 275), 10)
        pygame.draw.rect(screen, player_colour, player)
        # Win Screen
        # Using death screen features just for convenience. May change later.
        pygame.draw.rect(screen, death_screen_colour, death_screen)
        screen.blit(w_main_text, (600, 275))
        pygame.draw.rect(screen, blue, w_playagain_button)
        screen.blit(w_playagain_text, (325, 675))
        pygame.draw.rect(screen, red, w_quit_button)
        screen.blit(w_quit_text, (693.3, 675))
        pygame.draw.rect(screen, green, w_nextlevel_button)
        screen.blit(w_nextlevel_text, (991.7, 675))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x in range(300, 533) and mouse_y in range(650, 750):
                        win = False
                        blocked_left = False
                        blocked_right = False
                        velocity = 0
                        player = pygame.Rect(80, 400, 25, 25)
                    if mouse_x in range(633, 867) and mouse_y in range(650, 750):
                        pass # Started screen not added yet!
                    if mouse_x in range(967, 1200) and mouse_y in range(650, 750):
                        pass # New levels have not been added yet!

    if game_active and not alive and not win: 
        # Death Screen
        pygame.draw.rect(screen, death_screen_colour, death_screen)
        screen.blit(d_main_text, (600, 275))
        pygame.draw.rect(screen, blue, d_playagain_button)
        screen.blit(d_playagain_text, (375, 670))
        pygame.draw.rect(screen, red, d_quit_button)
        screen.blit(d_quit_text, (950, 670))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x in range(300, 700) and mouse_y in range(650, 750):
                        alive = True
                        blocked_left = False
                        blocked_right = False
                        velocity = 0
                        player = pygame.Rect(80, 400, 25, 25)
                    if mouse_x in range(800, 1200) and mouse_y in range(650, 750):
                        pass # Started screen not added yet!


            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    if game_active and alive and not win:
        # Player is alive
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
            
                if event.key == pygame.K_w:
                    if grounded:
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

        if player.colliderect(coin1):
            win = True

        if player.colliderect(lava):
            alive = False

        pygame.draw.rect(screen, lava_colour, lava)
        for platform in platforms:
            pygame.draw.rect(screen, wall_colour, platform)

        pygame.draw.rect(screen, player_colour, player)
        pygame.draw.circle(screen, gold_yellow, (1425, 275), 10)
    clock.tick(60)
    pygame.display.flip()