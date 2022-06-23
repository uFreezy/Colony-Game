import sys
import time
import json

import pygame

import definitions
import utils.drawing_utils as drawUtils
import utils.global_vars as glVars
import utils.network_utils as netUtils

from models.player import Player
from models.message import Message
from utils import eztext

pygame.init()

# Network socket
soc = None
# Screen size
size = width, height = definitions.SCREEN_WIDTH, definitions.SCREEN_HEIGHT
# Screen instance
screen = drawUtils.init_screen(size)
# Game clock
clock = pygame.time.Clock()
# Background image
background = pygame.transform.scale(pygame.image.load(
    definitions.BACKGROND_SPRITE), (width, height))
ballrect = background.get_rect()

# Text input for the username
txtInpX = definitions.SCREEN_WIDTH / 2 - 150
txtInpY = definitions.SCREEN_HEIGHT / 2 - 12
txtInpFont = pygame.font.Font('freesansbold.ttf', 20)
textInput = eztext.Input(x=txtInpX, y=txtInpY, maxlength=10, color=(
    255, 255, 255), font=txtInpFont, prompt='Enter username: ')

main_player = Player(definitions.PLAYER_SPRITE, False, pygame.display.Info(
).current_w / 2, pygame.display.Info().current_h - definitions.PLAYER_SIZE)
enemy_player = Player(definitions.ENEMY_SPRITE, True,
                      pygame.display.Info().current_w / 2, 0)

isGameActive = False
isGameOver = False

# Initiate all visual objects
screen.fill((0, 0, 0))
screen.blit(background, ballrect)
screen.blit(main_player.image, main_player.rect)
screen.blit(enemy_player.image, enemy_player.rect)

tickRate = 0.02
lastTick = time.time()
username = None
lastPlayerState = None

# Main game loop
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

    if username and soc is None:
        soc = netUtils.socket_init()

    if glVars.IS_SERVER_ACTIVE and not isGameOver and username:
        main_player.username = username
        # Tick tock motherfucker
        if time.time() - lastTick > tickRate:
            main_player.tick()
            enemy_player.tick()
            lastTick = time.time()
        netUtils.send_data(soc, main_player.player_info())

        keys = pygame.key.get_pressed()
        # If input is detected we handle it
        if 1 in keys and isGameActive:
            main_player.handle_input(keys)
            playerData = main_player.player_info()
            # Checks if the player data has changes if so => propagate to server
            if lastPlayerState is None or lastPlayerState != json.dumps(playerData, sort_keys=True):
                netUtils.send_data(soc, main_player.player_info())

        # Listen for changes from the server
        comm_data = netUtils.parse_socket_data(soc)
    

        if comm_data and 'isGameOver' not in comm_data:
            # If we have comm_data that means
            # there is active match
            isGameActive = True
            main_player.hp = comm_data['plHp']
            enPl = comm_data['enemyObj']
            enemy_player.x = enPl['x']
            enemy_player.y = enPl['y']
            enemy_player.hp = enPl['hp']
            enemy_player.username = enPl['username']
            enemy_player.clear_bullets()
            if enPl['bullets']:
                for bullet in enPl['bullets']:
                    enemy_player.add_bullet(
                        definitions.RED_LASER_SPRITE, bullet['x'], (bullet['y'] - 50))
        elif comm_data  and comm_data['isGameOver']:
            glVars.MESSAGES.append(
                Message(comm_data['message'], definitions.INFO_MESSAGE))
            if comm_data['isWinner']:
                enemy_player.hp = 0
            else:
                main_player.hp = 0

            isGameOver = True

    # Update all visual  objects
    screen.blit(background, ballrect, ballrect)
    # Loops through the messages (if any) and displays them.
    drawUtils.draw_existing_messages(screen, glVars.MESSAGES)

    # Draw all objects on screen.
    drawUtils.draw_health_ui(screen, main_player.hp, enemy_player.hp)
    drawUtils.draw_username_ui(
        screen, main_player.username, enemy_player.username)
    drawUtils.draw_obj(screen, enemy_player)
    drawUtils.draw_obj(screen, main_player)

    if not username:
        username = textInput.update(events)
        textInput.draw(screen)
        # For testing purposes
        main_player.username = username

    if isGameActive and not isGameOver:
        for bullet in main_player.bullets:
            drawUtils.draw_obj(screen, bullet)
        for bullet in enemy_player.bullets:
            drawUtils.draw_obj(screen, bullet)
            
    pygame.display.update()
    clock.tick(120)
