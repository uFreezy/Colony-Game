import definitions


class Match:
    """
    Class representation of a single match between two players.
    """

    def __init__(self, player_one, player_two):
        self._player_one_connection = player_one
        self._player_two_connection = player_two
        self._player_one_data = None
        self._player_two_data = None
        self._last_tick = None
        self._bullet_log = []
        self._is_active = True

    @property
    def player_one_conn(self):
        return self._player_one_connection

    @property
    def player_two_conn(self):
        return self._player_two_connection

    @property
    def player_one_data(self):
        return self._player_one_data

    @player_one_data.setter
    def player_one_data(self, pl_data):
        if not self._player_one_data:
            self._player_one_data = pl_data
            self._player_one_data['hp'] = 100
            return
        self._player_one_data['x'] = pl_data['x']
        self._player_one_data['y'] = pl_data['y']
        self._player_one_data['hp'] = pl_data['hp']

        self.__bullet_append(pl_data['bullets'], self._player_one_data)

    @property
    def player_two_data(self):
        return self._player_two_data

    @player_two_data.setter
    def player_two_data(self, pl_data):
        if not self._player_two_data:
            self._player_two_data = pl_data
            self._player_two_data['hp'] = 100
            return

        self._player_two_data['x'] = pl_data['x']
        self._player_two_data['y'] = pl_data['y']

        self._player_two_data['hp'] = pl_data['hp']

        self.__bullet_append(pl_data['bullets'], self._player_two_data)

    @property
    def last_tick(self):
        return self._last_tick

    @last_tick.setter
    def last_tick(self, tick_date):
        self._last_tick = tick_date

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        self._is_active = is_active

    def are_active_bullets(self):
        is_pl_one_bull = self._player_one_data['bullets'] and any(
            self._player_one_data['bullets'])
        is_pl_two_bull = self._player_two_data['bullets'] and any(
            self._player_two_data['bullets'])

        return is_pl_one_bull and is_pl_two_bull

    # Removes out of screen bullets.
    @staticmethod
    def __bullet_trim(bullets):
        for bull in bullets:
            if bull['y'] <= -30 or bull['y'] > definitions.SCREEN_HEIGHT + 54:
                bullets.remove(bull)

    def __bullet_append(self, bullets, player):
        if bullets:
            for bul in bullets:
                does_exist = False
                for exBull in player['bullets']:
                    if exBull['id'] == bul['id']:
                        does_exist = True
                if not does_exist and bul['id'] not in self._bullet_log:
                    player['bullets'].append(bul)
                    self._bullet_log.append(bul['id'])

    def bullet_flow(self):
        """
        Moves bullets serverside
        """
        if self._player_one_data['bullets']:
            for bul in self._player_one_data['bullets']:
                bul['y'] = bul['y'] - definitions.BULLET_SPEED

        if self._player_two_data['bullets']:
            for bul in self._player_two_data['bullets']:
                bul['y'] = bul['y'] - definitions.BULLET_SPEED

        self.__bullet_trim(self._player_one_data['bullets'])
        self.__bullet_trim(self._player_two_data['bullets'])

    def remove_bullet(self, bullet_id):
        """
        Removes bullet from player per given id
        """
        for bul in self._player_one_data['bullets']:
            if bullet_id == bul['id']:
                self._player_one_data['bullets'].remove(bul)
                return
        for bul in self._player_two_data['bullets']:
            if bullet_id == bul['id']:
                self._player_two_data['bullets'].remove(bul)
