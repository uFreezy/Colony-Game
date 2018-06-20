import sys
import time
import json

import pygame

import definitions
import utils.drawingUtils as drawUtils
import utils.globalVars as glVars
import utils.networkUtils as netUtils

from models.player import Player
from models.message import Message
from utils import eztext

pygame.init()

soc = None
size = width, height = definitions.SCREEN_WIDTH, definitions.SCREEN_HEIGHT
screen = drawUtils.init_screen(size)
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load(
    definitions.BACKGROND_SPRITE), (width, height))
ballrect = background.get_rect()

# Text input for the username
txtInpX = definitions.SCREEN_WIDTH / 2 - 150
txtInpY = definitions.SCREEN_HEIGHT / 2 - 12
txtInpFont = pygame.font.Font('freesansbold.ttf', 20)
textInput = eztext.Input(x=txtInpX, y=txtInpY, maxlength=10, color=(255, 255, 255), font=txtInpFont, prompt='Enter '
                                                                                                            'username: ')

mainPlayer = Player(definitions.PLAYER_SPRITE, False, pygame.display.Info(
).current_w / 2, pygame.display.Info().current_h - definitions.PLAYER_SIZE)
enemyPlayer = Player(definitions.ENEMY_SPRITE, True,
                     pygame.display.Info().current_w / 2, 0)

isGameActive = False
isGameOver = False

# Initiate all visual objects
screen.fill((0, 0, 0))
screen.blit(background, ballrect)
screen.blit(mainPlayer.get_image(), mainPlayer.get_rect())
screen.blit(enemyPlayer.get_image(), enemyPlayer.get_rect())

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

    if glVars.isServerActive and not isGameOver and username:
        mainPlayer.set_username(username)
        # Tick tock motherfucker
        if time.time() - lastTick > tickRate:
            mainPlayer.tick()
            enemyPlayer.tick()
            lastTick = time.time()
        netUtils.send_data(soc, mainPlayer.get_player_info())

        keys = pygame.key.get_pressed()
        # If input is detected we handdle it
        if 1 in keys and isGameActive:
            mainPlayer.handle_input(keys)
            playerData = mainPlayer.get_player_info()
            # Checks if the player data has changes if so => propagate to server
            if lastPlayerState is None or lastPlayerState != json.dumps(playerData, sort_keys=True):
                netUtils.send_data(soc, mainPlayer.get_player_info())

        # Listen for changes from the server
        # TODO: Enemy data parsing as separate method
        commData = netUtils.parse_socket_data(soc)

        if commData is not None and 'isGameOver' not in commData:
            # If we have commData that means
            # there is active match
            isGameActive = True
            mainPlayer.hp = commData['plHp']
            enPl = commData['enemyObj']
            enemyPlayer.posX = enPl['x']
            enemyPlayer.posY = enPl['y']
            enemyPlayer.hp = enPl['hp']
            enemyPlayer.username = enPl['username']
            # TODO: think of a better way to propagate enemy bullets
            # so the screen wont flicker.
            enemyPlayer.clear_bullets()
            if enPl['bullets']:
                for bullet in enPl['bullets']:
                    enemyPlayer.add_bullet(
                        definitions.RED_LASER_SPRITE, bullet['x'], (bullet['y'] - 50))
        elif commData is not None and commData['isGameOver'] is not None:
            glVars.messages.append(Message(commData['message'], definitions.INFO_MESSAGE))
            if commData['isWinner']:
                enemyPlayer.hp = 0
            else:
                mainPlayer.hp = 0

            isGameOver = True

    # Update all visual  objects
    screen.blit(background, ballrect, ballrect)
    # Loops through the messages (if any) and displays them.
    drawUtils.draw_existing_messages(screen, glVars.messages)

    drawUtils.draw_health_ui(screen, mainPlayer.hp, enemyPlayer.hp)
    drawUtils.draw_username_ui(screen, mainPlayer.get_username(), enemyPlayer.get_username())
    drawUtils.draw_obj(screen, enemyPlayer)
    drawUtils.draw_obj(screen, mainPlayer)

    if not username:
        username = textInput.update(events)
        textInput.draw(screen)
        # For testing purposes
        mainPlayer.set_username(username)

    if isGameActive and not isGameOver:
        for bullet in mainPlayer.get_bullets():
            drawUtils.draw_obj(screen, bullet)
        for bullet in enemyPlayer.get_bullets():
            drawUtils.draw_obj(screen, bullet)
    pygame.display.update()
    clock.tick(30)
