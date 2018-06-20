import definitions


class Match:
    def __init__(self, player_one, player_two):
        self.playerOneConn = player_one
        self.playerTwoConn = player_two
        self.playerOneData = None
        self.playerTwoData = None
        self.lastTick = None
        self.bulletLog = []
        self.isActive = True

    def get_player_one_conn(self):
        return self.playerOneConn

    def get_player_two_conn(self):
        return self.playerTwoConn

    def get_player_one_data(self):
        return self.playerOneData

    def get_player_two_data(self):
        return self.playerTwoData

    def set_player_one_data(self, pl_data):
        if self.playerOneData is None:
            self.playerOneData = pl_data
            self.playerOneData['hp'] = 100
            return
        self.playerOneData['x'] = pl_data['x']
        self.playerOneData['y'] = pl_data['y']
        self.playerOneData['hp'] = pl_data['hp']

        self.__bullet_append(pl_data['bullets'], self.playerOneData)

    def set_player_two_data(self, pl_data):
        if self.playerTwoData is None:
            self.playerTwoData = pl_data
            self.playerTwoData['hp'] = 100
            return

        self.playerTwoData['x'] = pl_data['x']
        self.playerTwoData['y'] = pl_data['y']

        self.playerTwoData['hp'] = pl_data['hp']

        self.__bullet_append(pl_data['bullets'], self.playerTwoData)

    def get_last_tick(self):
        return self.lastTick

    def set_last_tick(self, tick_date):
        self.lastTick = tick_date

    def get_is_active(self):
        return self.isActive

    def set_is_active(self, is_active):
        self.isActive = is_active

    # TODO: Fix
    def are_active_bullets(self):
        is_pl_one_bull = self.playerOneData['bullets'] is not None and len(self.playerOneData['bullets']) > 0
        is_pl_two_bull = self.playerTwoData['bullets'] is not None and len(self.playerTwoData['bullets']) > 0

        return is_pl_one_bull and is_pl_two_bull

    # Removes out of screen bullets.
    @staticmethod
    def __bullet_trim(bullets):
        for bull in bullets:
            if bull['y'] <= -30 or bull['y'] > definitions.SCREEN_HEIGHT + 54:
                bullets.remove(bull)

    # TODO: Simplify
    def __bullet_append(self, bullets, player):
        if bullets is not None:
            for bul in bullets:
                does_exist = False
                for exBull in player['bullets']:
                    if exBull['id'] == bul['id']:
                        does_exist = True
                if not does_exist and bul['id'] not in self.bulletLog:
                    player['bullets'].append(bul)
                    self.bulletLog.append(bul['id'])

    # Moves bullets serverside
    def bullet_flow(self):
        if self.playerOneData['bullets'] is not None:
            for bul in self.playerOneData['bullets']:
                bul['y'] = bul['y'] - definitions.BULLET_SPEED

        if self.playerTwoData['bullets'] is not None:
            for bul in self.playerTwoData['bullets']:
                bul['y'] = bul['y'] - definitions.BULLET_SPEED

        self.__bullet_trim(self.playerOneData['bullets'])
        self.__bullet_trim(self.playerTwoData['bullets'])

    # Removes bullet from player per given id
    def remove_bullet(self, bullet_id):
        for bul in self.playerOneData['bullets']:
            if bullet_id == bul['id']:
                self.playerOneData['bullets'].remove(bul)
                return
        for bul in self.playerTwoData['bullets']:
            if bullet_id == bul['id']:
                self.playerTwoData['bullets'].remove(bul)
