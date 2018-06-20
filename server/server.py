import copy
import pickle
import socket

import time
from io import BlockingIOError
import utils.gameUtils as gameUtils
from servModels.match import Match

import definitions


socket_obj = socket.socket()
host = definitions.SERVER_HOST
port = definitions.SERVER_PORT
socket_obj.bind((host, port))
socket_obj.setblocking(0)

clients = []
matches = []
lastCheck = None

print('Welcome to colony game server!')


def game_over():
    go_obj = {'isGameOver': True, 'isWinner': True, 'message': "You won! Game Over!"}

    try:
        if match.get_player_one_data()['hp'] > 0:
            match.get_player_one_conn().send(pickle.dumps(go_obj))
            go_obj['message'] = 'You lost! Game Over!'
            go_obj['isWinner'] = False
            match.get_player_two_conn().send(pickle.dumps(go_obj))
        elif match.get_player_two_data()['hp'] > 0:
            match.get_player_two_conn().send(pickle.dumps(go_obj))
            go_obj['message'] = 'You lost! Game Over!'
            go_obj['isWinner'] = False
            match.get_player_one_conn().send(pickle.dumps(go_obj))
    except (BlockingIOError, BrokenPipeError):
        pass


# Listens for client connection
socket_obj.listen(5)
while True:
    isNewConnAdded = False

    conn = None
    addr = None
    try:
        # Establish connection with client.
        conn, addr = socket_obj.accept()
        clients.append(conn)
        isNewConnAdded = True
        print('Got connection from ', addr)
    except BlockingIOError:
        pass

    # Check the user conn status
    for client in clients:
        if gameUtils.is_user_connected(client) is not True:
            clients.remove(client)

    # If new connection is added => look for a match
    if isNewConnAdded and conn is not None:
        while len(clients) >= 2:
            matches.append(Match(clients.pop(0), clients.pop(0)))
            print('Matched!')

    for match in matches:
        if match.get_is_active():
            plOneByte = None
            plTwoByte = None

            if gameUtils.is_user_connected(match.get_player_one_conn()) is not True:
                gameUtils.end_game_disconnect(matches, match)
            elif gameUtils.is_user_connected(match.get_player_one_conn()) is not True:
                gameUtils.end_game_disconnect(matches, match)

            try:
                # TODO: Socket receiving to be done in a separate  method
                try:
                    plOneByte = match.get_player_one_conn().recv(4096)
                except BlockingIOError:
                    pass
                try:
                    plTwoByte = match.get_player_two_conn().recv(4096)
                except BlockingIOError:
                    pass

                plOne = None
                plTwo = None
                if plOneByte is not None:
                    plOne = pickle.loads(plOneByte)

                    # TODO: Do it in the match object
                    plOne['y'] = definitions.SCREEN_HEIGHT - (plOne['y'] + definitions.PLAYER_SIZE)

                    # If this is the first time setting data
                    # => put the player's hp = maxHp
                    if match.get_player_one_data() is None:
                        plOne['hp'] = 100
                    else:
                        plOne['hp'] = match.get_player_one_data()['hp']

                    match.set_player_one_data(copy.deepcopy(plOne))

                    if plOne['bullets']:
                        for bul in plOne['bullets']:
                            bul['y'] = definitions.SCREEN_HEIGHT - bul['y']

                    # We create comm obj containing player's own hp
                    # and enemy data.
                    commData = {}
                    if match.get_player_two_data() is None:
                        commData['plHp'] = 100
                    else:
                        commData['plHp'] = match.get_player_two_data()['hp']

                    plOne['hp'] = match.get_player_one_data()['hp']
                    commData['enemyObj'] = plOne

                    match.get_player_two_conn().send(pickle.dumps(commData))

                if plTwoByte is not None:
                    plTwo = pickle.loads(plTwoByte)
                    plTwo['y'] = definitions.SCREEN_HEIGHT - (plTwo['y'] + definitions.PLAYER_SIZE)

                    # TODO: Temporay solution! Improve!

                    if match.get_player_two_data() is None:
                        plTwo['hp'] = 100
                    else:
                        plTwo['hp'] = match.get_player_two_data()['hp']
                    match.set_player_two_data(copy.deepcopy(plTwo))

                    if plTwo['bullets']:
                        for bul in plTwo['bullets']:
                            bul['y'] = definitions.SCREEN_HEIGHT - bul['y']

                    commData = {}

                    if match.get_player_one_data() is None:
                        commData['plHp'] = 100
                    else:
                        commData['plHp'] = match.get_player_one_data()['hp']

                    plTwo['hp'] = match.get_player_two_data()['hp']
                    commData['enemyObj'] = plTwo

                    match.get_player_one_conn().send(pickle.dumps(commData))

                # Bullet flow
                isData = match.get_player_one_data() is not None and match.get_player_two_data() is not None
                if isData and (match.get_last_tick() is None or time.time() - match.get_last_tick() > 0.035):
                    match.bullet_flow()
                    match.set_last_tick(time.time())

                # Collision Check
                if isData:
                    afterCollPlData = gameUtils.collision_detec(match)
                    match.set_player_one_data(afterCollPlData[0])
                    match.set_player_two_data(afterCollPlData[1])

                # When one of the players looses the game we make the match inactive
                # and stop processing the match's data but we still propagate the
                # last known data to the players for a while
                if isData and (match.get_player_one_data()['hp'] == 0 or match.get_player_two_data()['hp'] == 0):
                    match.set_is_active(False)
                    game_over()
            except (EOFError, OSError):
                gameUtils.end_game_disconnect(matches, match)
        else:
            game_over()
