import pygame
import sys

""" 
Changes to make:
- Continue developing individual levels
    - Winscreens and basically all non-default screens have platform/player/lava/coin values with hardcoded integration. That will need to change.
    - Add/develop more accelerator/booster pads
- Add levels screen
- Add tutorial
- Consider moving the levels to different files
- Add art
    - Make the pause button look like a pause button
    - Maybe make it go daytime to nighttime (and travel to different biomes) 
"""

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
colours = {
    "screen_colour": (0, 15, 135),
    "wall_colour": (153, 81, 0),
    "lava_colour": (173, 30, 0),
    "player_colour": (0, 135, 6),
    "death_screen_colour": (255, 243, 208),
    "blue": (42, 116, 255),
    "red": (204, 0, 0),
    "green": (0, 176, 48),
    "gold_yellow": (245, 204, 3),
    "skyblue": (0, 184, 255),
    "grey": (150, 150, 150),
    "black": (0, 0, 0),
    "bouncy_colour": (255, 159, 0),
}
p_main_font = pygame.font.SysFont('calibri', 70) # FOR GENERAL USE

# Death Text
d_main_text = p_main_font.render("You Died!", True, colours["black"])
d_button_font = pygame.font.SysFont('calibri', 55)
d_playagain_text = d_button_font.render("Play Again", True, colours["black"])
d_quit_text = d_button_font.render("Quit", True, colours["black"])

# Win Text
w_main_text = p_main_font.render("You Win!", True, colours["black"])
w_button_font = pygame.font.SysFont('calibri', 45)
w_playagain_text = w_button_font.render("Play Again", True, colours["black"])
w_quit_text = w_button_font.render("Quit", True, colours["black"])
w_nextlevel_text = w_button_font.render("Next Level", True, colours["black"])

# Pause Text
p_main_text = p_main_font.render("Game Paused", True, colours["black"])
# Uses win font
p_restart_text = w_button_font.render("Restart", True, colours["black"])
p_quit_text = w_button_font.render("Quit", True, colours["black"])
p_resume_text = w_button_font.render("Resume", True, colours["black"])


velocity = 0
gravity = 1
jump_strength = 12
move_speed = 5

# Starting Screen
starting_screen_bg = pygame.Rect(0, 0, 1500, 1000)
title_font = pygame.font.SysFont('calibri', 100)
title_text = title_font.render("ParkourPro", True, colours["black"])
play_button = pygame.Rect(400, 400, 700, 100)
play_bt_font = pygame.font.SysFont('calibri', 55)
play_bt_text = play_bt_font.render("Play", True, colours["black"])

# Levels Screen
# Note: Uses starting screen bg
levels_title_text = title_font.render("Levels", True, colours["black"])
# Maybe I can store all the levels in a dictionary?
# Find a way to demo the levels. Perhaps I can make some art and make it like a super mario 3d world (a LOT SIMPLER) or something.

# Win Screen
w_playagain_button = pygame.Rect(300, 650, 233, 100)
w_quit_button = pygame.Rect(633, 650, 233, 100)
w_nextlevel_button = pygame.Rect(967, 650, 233, 100)


# Death Screen
death_screen = pygame.Rect(200, 200, 1100, 600)
d_playagain_button = pygame.Rect(300, 650, 400, 100)
d_quit_button = pygame.Rect(800, 650, 400, 100)


# Game Screen Starts Here
# Pause Button
pause_button = pygame.Rect(1440, 10, 50, 50) # NOTE This could be the point where I begin adding images

# Platforms

# Level 1
level1_platforms = {
    "floor": pygame.Rect(0, 950, 1500, 50),
    "wallleft": pygame.Rect(0, 0, 50, 1000),
    "wallright": pygame.Rect(1450, 0, 50, 1000),
    "ceiling": pygame.Rect(0, 0, 1500, 100),
    "platform1": pygame.Rect(0, 850, 135, 150),
    "platform2": pygame.Rect(200, 820, 50, 10),
    "platform3": pygame.Rect(315, 790, 50, 10),
    "platform4": pygame.Rect(430, 760, 50, 10),
    "platform5": pygame.Rect(560, 730, 50, 10),
    "platform6": pygame.Rect(590, 670, 50, 10),
    "platform7": pygame.Rect(620, 610, 50, 10),
    "platform8": pygame.Rect(720, 580, 50, 10),
    "platform9": pygame.Rect(820, 550, 50, 10),
    "platform10": pygame.Rect(940, 520, 50, 10),
    "platform11": pygame.Rect(1040, 480, 50, 10),
    "platform12": pygame.Rect(1180, 440, 50, 10),
    "platform13": pygame.Rect(1300, 380, 50, 10),
    "platform14": pygame.Rect(1400, 310, 50, 10),
}
level1_bouncy_platforms = {}
level1_player = pygame.Rect(80, 400, 25, 25)
# Winning Coin (Uses rectangular hitbox)
level1_coin_hitbox = pygame.Rect(1415, 265, 20, 20)
level1_coin_graphic = (1425, 275)
# Lava
level1_lava = pygame.Rect(0, 900, 1500, 50)

# Level 2
level2_platforms = {
    "wallleft": pygame.Rect(0, 0, 50, 1000),
    "wallright": pygame.Rect(1450, 0, 50, 1000),
    "ceiling": pygame.Rect(0, 0, 1500, 100),
    "floorleft": pygame.Rect(0, 950, 400, 50),
    "platform1": pygame.Rect(400, 200, 33, 800),
    "platform2": pygame.Rect(833, 100, 33, 750),
    # actually build the rest of the level
    "platform3": pygame.Rect(200, 890, 50, 10),
    "platform4": pygame.Rect(300, 830, 50, 10),
    "platform5": pygame.Rect(200, 770, 50, 10),
    "platform6": pygame.Rect(100, 710, 50, 10),
    "platform7": pygame.Rect(50, 650, 50, 10),
    "platform8": pygame.Rect(50, 590, 40, 10),
    "platform9": pygame.Rect(50, 530, 30, 10),
    "platform10": pygame.Rect(125, 470, 50, 10),
    "platform11": pygame.Rect(250, 410, 50, 10),
    "platform12": pygame.Rect(150, 350, 50, 10),
    "platform13": pygame.Rect(250, 290, 50, 10),
    "platform14": pygame.Rect(150, 230, 50, 10),
    "platform15": pygame.Rect(50, 200, 50, 10),
    "platform16": pygame.Rect(100, 140, 333, 10),
    "platform17": pygame.Rect(433, 320, 330, 10),
    "platform18": pygame.Rect(753, 200, 10, 120),
    "platform19": pygame.Rect(507, 620, 330, 10),
    "platform20": pygame.Rect(507, 460, 10, 160),
    "platform21": pygame.Rect(520, 825, 100, 10),
    "platform22": pygame.Rect(657, 925, 50, 10),
    "platform23": pygame.Rect(813, 930, 53, 10),
    "platform24": pygame.Rect(1400, 850, 50, 10),
    "platform25": pygame.Rect(1410, 790, 40, 10),
    "platform26": pygame.Rect(1420, 730, 30, 10),
    "platform27": pygame.Rect(866, 710, 457, 10),
    "platform28": pygame.Rect(933, 450, 517, 10),
    "platform29": pygame.Rect(1128, 500, 10, 210),
    "platform30": pygame.Rect(1250, 565, 50, 10),
    "platform31": pygame.Rect(1128, 500, 50, 10),
    "platform32": pygame.Rect(1087, 390, 50, 10),
    "platform33": pygame.Rect(975, 340, 50, 10),
    "platform34": pygame.Rect(1087, 295, 50, 10),
    "platform35": pygame.Rect(975, 250, 50, 10),
    "platform36": pygame.Rect(1087, 205, 50, 10),
    "platform37": pygame.Rect(1400, 240, 50, 10),
}
level2_bouncy_platforms = {
    "platform1": pygame.Rect(713, 300, 40, 20),
    "platform2": pygame.Rect(713, 560, 40, 20),
    "platform3": pygame.Rect(585, 445, 40, 20),
    "platform4": pygame.Rect(433, 750, 74, 20),
    "platform5": pygame.Rect(950, 920, 50, 10),
    "platform6": pygame.Rect(1100, 900, 50, 10),
    "platform7": pygame.Rect(1275, 900, 50, 10),
    "platform8": pygame.Rect(1138, 650, 50, 10),
    "platform9": pygame.Rect(866, 650, 50, 10),
    "platform10": pygame.Rect(866, 575, 50, 10),
    "platform11": pygame.Rect(866, 500, 50, 10),
    "platform12": pygame.Rect(1260, 230, 50, 10),
}
level2_player = pygame.Rect(80, 900, 25, 25)
level2_coin_hitbox = pygame.Rect(1415, 220, 20, 20)
level2_coin_graphic = (1425, 230)
level2_lava = pygame.Rect(433, 950, 1017, 50)


# Game Screen Ends Here

running = True
blocked_left = False
blocked_right = False

active_screen = {
    "death": False,
    "levels": False,
    "lose": False,
    "main": False,
    "pause": False,
    "pause": False,
    "play": True,
    "win": False,
}

active_level = {
    1: False,
    2: True,
    3: False,
    4: False,
    5: False,
}

def change_screen(current, new, active_screen):
    active_screen[current] = False
    active_screen[new] = True
    return active_screen

def change_level(active_level):
    for level in active_level:
        if active_level[level]:
            new_level = level + 1
            active_level[level] = False
    active_level[new_level] = True
    return active_level

def identify_level(active_level):
    for level in active_level:
        if active_level[level]:
            return level

# Game Loop
running = True
while running:

# Main Screen
    if active_screen["main"]:
        pygame.draw.rect(screen, colours["skyblue"], starting_screen_bg)
        screen.blit(title_text, (450, 100))
        pygame.draw.rect(screen, colours["green"], play_button)
        screen.blit(play_bt_text, (450, 450))

        # Handling exiting the game
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x in range(play_button[0], play_button[0] + play_button[2]) and mouse_y in range(play_button[1], play_button[1] + play_button[3]):
                        active_screen = change_screen("main", "play", active_screen) # NOTE levels isn't fully developed, so play is temporarily used instead.
                        blocked_left = False
                        blocked_right = False
                        velocity = 0
                        if active_level[1]:
                            level1_player = pygame.Rect(80, 400, 25, 25)
                        if active_level[2]:
                            level2_player = pygame.Rect(80, 900, 25, 25)

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Pause Screen
    if active_screen["pause"]:
        pygame.draw.rect(screen, colours["death_screen_colour"], death_screen)
        screen.blit(p_main_text, (600, 275))
        pygame.draw.rect(screen, colours["blue"], w_playagain_button)
        screen.blit(p_restart_text, (325, 675))
        pygame.draw.rect(screen, colours["red"], w_quit_button)
        screen.blit(p_quit_text, (693.3, 675))
        pygame.draw.rect(screen, colours["green"], w_nextlevel_button)
        screen.blit(p_resume_text, (991.7, 675))

        # Handling exiting the game
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x in range(w_playagain_button[0], w_playagain_button[0] + w_playagain_button[2]) and mouse_y in range(w_playagain_button[1], w_playagain_button[1] + w_playagain_button[3]):
                        active_screen = change_screen("pause", "play", active_screen)
                        blocked_left = False
                        blocked_right = False
                        velocity = 0
                        if active_level[1]:
                            level1_player = pygame.Rect(80, 400, 25, 25)
                        if active_level[2]:
                            level2_player = pygame.Rect(80, 900, 25, 25)
                    if mouse_x in range(w_quit_button[0], w_quit_button[0] + w_quit_button[2]) and mouse_y in range(w_quit_button[1], w_quit_button[1] + w_quit_button[3]):
                        active_screen = change_screen("pause", "main", active_screen)
                    if mouse_x in range(w_nextlevel_button[0], w_nextlevel_button[0] + w_nextlevel_button[2]) and mouse_y in range(w_nextlevel_button[1], w_nextlevel_button[1] + w_nextlevel_button[3]):
                        active_screen = change_screen("pause", "play", active_screen)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
# Win Screen
    if active_screen["win"]:
        pygame.draw.circle(screen, colours["screen_colour"], (1425, 275), 10)
        pygame.draw.rect(screen, colours["player_colour"], player)
        # Using death screen features just for convenience. May change later.
        pygame.draw.rect(screen, colours["death_screen_colour"], death_screen)
        screen.blit(w_main_text, (600, 275))
        pygame.draw.rect(screen, colours["blue"], w_playagain_button)
        screen.blit(w_playagain_text, (325, 675))
        pygame.draw.rect(screen, colours["red"], w_quit_button)
        screen.blit(w_quit_text, (693.3, 675))
        pygame.draw.rect(screen, colours["green"], w_nextlevel_button)
        screen.blit(w_nextlevel_text, (991.7, 675))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x in range(300, 533) and mouse_y in range(650, 750):
                        active_screen = change_screen("win", "play", active_screen)
                        blocked_left = False
                        blocked_right = False
                        velocity = 0
                        if active_level[1]:
                            level1_player = pygame.Rect(80, 400, 25, 25)
                        if active_level[2]:
                            level2_player = pygame.Rect(80, 900, 25, 25)
                    if mouse_x in range(633, 867) and mouse_y in range(650, 750):
                        active_screen = change_screen("win", "main", active_screen)
                    if mouse_x in range(967, 1200) and mouse_y in range(650, 750):
                        active_level = change_level(active_level)
                        active_screen = change_screen("win", "play", active_screen)
                        # Add a way to create and store more levels.
                        # Currently, the level switches, but I don't really have more levels.

# Death Screen
    if active_screen["death"]:
        pygame.draw.rect(screen, colours["death_screen_colour"], death_screen)
        screen.blit(d_main_text, (600, 275))
        pygame.draw.rect(screen, colours["blue"], d_playagain_button)
        screen.blit(d_playagain_text, (375, 670))
        pygame.draw.rect(screen, colours["red"], d_quit_button)
        screen.blit(d_quit_text, (950, 670))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x in range(300, 700) and mouse_y in range(650, 750):
                        active_screen = change_screen("death", "play", active_screen)
                        blocked_left = False
                        blocked_right = False
                        velocity = 0
                        if active_level[1]:
                            level1_player = pygame.Rect(80, 400, 25, 25)
                        if active_level[2]:
                            level2_player = pygame.Rect(80, 900, 25, 25)
                    if mouse_x in range(800, 1200) and mouse_y in range(650, 750):
                        active_screen = change_screen("death", "main", active_screen)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Playing
    if active_screen["play"]:
        screen.fill(colours["screen_colour"]) # background

        if active_level[1]:
            platforms = level1_platforms.copy()
            bouncy_platforms = level1_bouncy_platforms.copy()
            player = level1_player
            coin_hitbox = level1_coin_hitbox
            coin_graphic = level1_coin_graphic
            lava = level1_lava
        elif active_level[2]:
            platforms = level2_platforms.copy()
            bouncy_platforms = level2_bouncy_platforms.copy()
            player = level2_player
            coin_hitbox = level2_coin_hitbox
            coin_graphic = level2_coin_graphic
            lava = level2_lava
            """
        elif active_level[3]:
            platforms = level3_platforms.copy()
        elif active_level[4]:
            platforms = level4_platforms.copy()
        elif active_level[5]:
            platforms = level5_platforms.copy()
            """

        player.y -= velocity
        grounded = False

        for platform in platforms:
            player, velocity, landed = check_vertical_landing(player, platforms[platform], velocity)
            if landed:
                grounded = True

        for platform in bouncy_platforms:
            if player.colliderect(bouncy_platforms[platform]):
                velocity = 17
                grounded = False

        if not grounded:
            velocity -= gravity

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_w, pygame.K_UP):
                    if grounded:
                        velocity += jump_strength
                        grounded = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x in range(pause_button[0], pause_button[0] + pause_button[2]) and mouse_y in range(pause_button[1], pause_button[1] + pause_button[3]):
                        active_screen = change_screen("play", "pause", active_screen)

        # Get the state of all keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.x -= move_speed
            for platform in platforms:
                player = check_horizontal_landing(player, platforms[platform], "left")

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.x += move_speed
            for platform in platforms:
                player = check_horizontal_landing(player, platforms[platform], "right")

        if player.colliderect(coin_hitbox): # NOTE Maybe I can invent a coin hitbox later that's circular. Like check if the player is in the circle's area.
            active_screen = change_screen("play", "win", active_screen)

        if player.colliderect(lava):
            active_screen = change_screen("play", "death", active_screen)

        # Different for every level
        pygame.draw.rect(screen, colours["lava_colour"], lava)
        for platform in platforms:
            pygame.draw.rect(screen, colours["wall_colour"], platforms[platform])
        for platform in bouncy_platforms:
            pygame.draw.rect(screen, colours["bouncy_colour"], bouncy_platforms[platform])
        pygame.draw.rect(screen, colours["player_colour"], player)
        pygame.draw.circle(screen, colours["gold_yellow"], coin_graphic, 10) # (1400, 220, 20, 20) #lvl2 1425, 230         #lvl1 1425, 275
        
        pygame.draw.rect(screen, colours["grey"], pause_button)
    clock.tick(60)
    pygame.display.flip()