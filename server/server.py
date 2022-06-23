"""
Game server run file.
"""
import copy
import pickle
import socket

import time
from io import BlockingIOError
from servModels.match import Match
from utils import game_utils


import definitions


socket_obj = socket.socket()
host = definitions.SERVER_HOST
port = definitions.SERVER_PORT
socket_obj.bind((host, port))
socket_obj.setblocking(0)

clients = []
matches = []
last_check = None

print('Welcome to colony game server!')


def game_over():
    go_obj = {'isGameOver': True, 'isWinner': True,
              'message': "You won! Game Over!"}

    try:
        if match.player_one_data['hp'] > 0:
            match.player_one_conn.send(pickle.dumps(go_obj))
            go_obj['message'] = 'You lost! Game Over!'
            go_obj['isWinner'] = False
            match.player_two_conn.send(pickle.dumps(go_obj))
        elif match.player_two_data['hp'] > 0:
            match.player_two_conn.send(pickle.dumps(go_obj))
            go_obj['message'] = 'You lost! Game Over!'
            go_obj['isWinner'] = False
            match.player_one_conn.send(pickle.dumps(go_obj))
    except (BlockingIOError, BrokenPipeError):
        pass


# Listens for client connection
socket_obj.listen(5)
while True:
    is_new_connection_added = False

    connection = None
    address = None
    try:
        # Establish connection with client.
        connection, address = socket_obj.accept()
        clients.append(connection)
        is_new_connection_added = True
        print('Got connection from ', address)
    except BlockingIOError:
        pass

    # Check the user connection status
    for client in clients:
        if game_utils.is_user_connected(client) is not True:
            clients.remove(client)

    # If new connection is added => look for a match
    if is_new_connection_added and connection:
        while len(clients) >= 2:
            matches.append(Match(clients.pop(0), clients.pop(0)))
            print('Matched!')

    for match in matches:
        if match.is_active:
            player_one_bytes = None
            player_two_bytes = None

            if not game_utils.is_user_connected(match.player_one_conn) or not game_utils.is_user_connected(match.player_two_conn):
                game_utils.end_game_disconnect(matches, match)

            try:
                try:
                    player_one_bytes = match.player_one_conn.recv(4096)
                except BlockingIOError:
                    pass
                try:
                    player_two_bytes = match.player_two_conn.recv(4096)
                except BlockingIOError:
                    pass

                player_one = None
                player_two = None
                if player_one_bytes:
                    player_one = pickle.loads(player_one_bytes)

                    player_one['y'] = definitions.SCREEN_HEIGHT - \
                        (player_one['y'] + definitions.PLAYER_SIZE)

                    # If this is the first time setting data
                    # => put the player's hp = maxHp
                    if match.player_one_data is None:
                        player_one['hp'] = 100
                    else:
                        player_one['hp'] = match.player_one_data['hp']

                    match.player_one_data = copy.deepcopy(player_one)

                    if player_one['bullets']:
                        for bul in player_one['bullets']:
                            bul['y'] = definitions.SCREEN_HEIGHT - bul['y']

                    # We create comm obj containing player's own hp
                    # and enemy data.
                    commData = {}
                    if match.player_one_data is None:
                        commData['plHp'] = 100
                    else:
                        commData['plHp'] = match.player_one_data['hp']

                    player_one['hp'] = match.player_one_data['hp']
                    commData['enemyObj'] = player_one

                    match.player_two_conn.send(pickle.dumps(commData))

                if player_two_bytes:
                    player_two = pickle.loads(player_two_bytes)
                    player_two['y'] = definitions.SCREEN_HEIGHT - \
                        (player_two['y'] + definitions.PLAYER_SIZE)

                    if not match.player_two_data:
                        player_two['hp'] = 100
                    else:
                        player_two['hp'] = match.player_two_data['hp']
                    match.player_two_data = copy.deepcopy(player_two)

                    if player_two['bullets']:
                        for bul in player_two['bullets']:
                            bul['y'] = definitions.SCREEN_HEIGHT - bul['y']

                    commData = {}

                    if not match.player_one_data:
                        commData['plHp'] = 100
                    else:
                        commData['plHp'] = match.player_one_data['hp']

                    player_two['hp'] = match.player_two_data['hp']
                    commData['enemyObj'] = player_two

                    match.player_one_conn.send(pickle.dumps(commData))

                # Bullet flow
                isData = match.player_one_data and match.player_two_data

                if isData and (match.last_tick is None or time.time() - match.last_tick > 0.035):
                    match.bullet_flow()
                    match.last_tick = time.time()

                # Collision Check
                if isData:
                    afterCollPlData = game_utils.collision_detect(match)
                    match.player_one_data = afterCollPlData[0]
                    match.player_two_data = afterCollPlData[1]

                # When one of the players looses the game we make the match inactive
                # and stop processing the match's data but we still propagate the
                # last known data to the players for a while

                if isData and (match.player_one_data['hp'] <= 0 or match.player_one_data['hp'] <= 0):
                    match.is_active = False
                    game_over()
            except (EOFError, OSError):
                game_utils.end_game_disconnect(matches, match)
        else:
            game_over()
