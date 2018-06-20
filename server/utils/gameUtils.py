from io import BlockingIOError


def is_user_connected(conn):
    try:
        if conn.recv(1024) is '':
            return False
        else:
            return True
    except BlockingIOError:
        return True
    except ConnectionError:
        print("The user " + str(conn) + "has exited the game.")
        return False


def end_game_disconnect(matches, match):
    match.get_player_one_conn().close()
    match.get_player_two_conn().close()
    try:
        matches.remove(match)
    except ValueError:
        pass


# TODO: Simplify it to use only one loop
# Detects destructive collisions between objects
def collision_detec(match):
    pl_one = match.get_player_one_data()
    pl_two = match.get_player_two_data()

    for bullet in pl_two['bullets']:
        if pl_one['x'] + 30 > bullet['x'] >= pl_one['x']:
            if pl_one['y'] + 50 > bullet['y']:
                print('Collision: player 1 is hit.' + 'BULLET: X: ')
                pl_one['hp'] -= 10
                match.remove_bullet(bullet['id'])

                continue
        if pl_one['x'] < bullet['x'] and pl_one['y'] < bullet['y']:
            if pl_one['x'] + 30 > bullet['x'] and pl_one['y'] + 30 > bullet['y']:
                print('Collision: player 1 is hit.')
                pl_one['hp'] -= 10

                match.remove_bullet(bullet['id'])

    for bullet in pl_one['bullets']:
        if pl_two['x'] + 30 > bullet['x'] >= pl_two['x']:
            if pl_two['y'] + 50 > bullet['y']:
                print('Collision: player 2 was hit.')
                pl_two['hp'] -= 10

                match.remove_bullet(bullet['id'])
                continue
        if pl_two['x'] < bullet['x'] and pl_two['y'] < bullet['y']:
            if pl_two['x'] + 30 > bullet['x'] and pl_two['y'] + 30 > bullet['y']:
                print('Collision: player 2 is hit.')
                pl_two['hp'] -= 10

                match.remove_bullet(bullet['id'])

    return [pl_one, pl_two]
