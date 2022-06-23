"""
Module that provides common server game functions
"""
from io import BlockingIOError


def is_user_connected(conn):
    """
    Checks if provided connection is active.
    """
    try:
        if conn.recv(1024) == '':
            return False
    except BlockingIOError:
        return True
    except ConnectionError:
        print("The user " + str(conn) + "has exited the game.")
        return False

    return True


def end_game_disconnect(matches, match):
    """
    Close the network connection to both players in the game.
    """
    match.player_one_conn.close()
    match.player_two_conn.close()
    try:
        matches.remove(match)
    except ValueError:
        pass


def collision_detect(match):
    """
    Detects destructive collisions between objects
    """
    pl_one = match.player_one_data
    pl_two = match.player_two_data

    for bullet in pl_two['bullets']:
        if (pl_one['x'] + 30 > bullet['x'] >= pl_one['x']) and (pl_one['y'] + 50 > bullet['y']):
            print('Collision: player 1 is hit.' + 'BULLET: X: ')
            pl_one['hp'] -= 10
            match.remove_bullet(bullet['id'])

            continue
        if (pl_one['x'] < bullet['x'] and pl_one['y'] < bullet['y']) and (pl_one['x'] + 30 > bullet['x'] and pl_one['y'] + 30 > bullet['y']):
            print('Collision: player 1 is hit.')
            pl_one['hp'] -= 10

            match.remove_bullet(bullet['id'])

    for bullet in pl_one['bullets']:
        if (pl_two['x'] + 30 > bullet['x'] >= pl_two['x']) and (pl_two['y'] + 50 > bullet['y']):
            print('Collision: player 2 was hit.')
            pl_two['hp'] -= 10

            match.remove_bullet(bullet['id'])
            continue
        if (pl_two['x'] < bullet['x'] and pl_two['y'] < bullet['y']) and (pl_two['x'] + 30 > bullet['x'] and pl_two['y'] + 30 > bullet['y']):
            print('Collision: player 2 is hit.')
            pl_two['hp'] -= 10

            match.remove_bullet(bullet['id'])

    return [pl_one, pl_two]
