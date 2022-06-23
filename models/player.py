import time
import pygame
import definitions

from models.projectile import Projectile


class Player(pygame.sprite.Sprite):
    """
    Class representation of the player in the game.
    """

    def __init__(self, sprite_uri, is_enemy, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self._username = ""
        self._is_enemy = is_enemy
        self._image = pygame.image.load(sprite_uri)
        self._image = pygame.transform.scale(
            self._image, (definitions.PLAYER_SIZE, definitions.PLAYER_SIZE))
        self._x = pos_x
        self._y = pos_y
        self._hp = 100
        self._shoot_stamp = time.time()

        self._bullets = []

        if self._is_enemy:
            self._image = pygame.transform.flip(self._image, False, True)

        self._rect = self._image.get_rect()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self.image = image

    @property
    def rect(self):
        return self._rect

    @property
    def username(self):
        if self._username:
            return self._username
        return None

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        self._hp = hp

    @property
    def bullets(self):
        return self._bullets

    @bullets.setter
    def bullets(self, bullets):
        self._bullets = bullets

    def add_bullet(self, sprite_uri, x, y):
        self._bullets.append(Projectile(sprite_uri, self._is_enemy, x, y))

    def clear_bullets(self):
        self._bullets = []

    def shoot(self):
        self.add_bullet(definitions.BLUE_LASER_SPRITE,
                        self.x, self.y - 50)

    def handle_input(self, input_keys):
        if input_keys[pygame.K_UP] == 1 and self._y > 0:
            self._y -= definitions.MOVEMENT_SPEED
        if input_keys[pygame.K_DOWN] == 1 and self._y < definitions.SCREEN_HEIGHT - definitions.PLAYER_SIZE:
            self._y += definitions.MOVEMENT_SPEED
        if input_keys[pygame.K_LEFT] == 1 and self._x > 0:
            self._x -= definitions.MOVEMENT_SPEED
        if input_keys[pygame.K_RIGHT] == 1 and self._x < definitions.SCREEN_WIDTH - definitions.PLAYER_SIZE:
            self._x += definitions.MOVEMENT_SPEED
        if input_keys[pygame.K_SPACE] == 1 and time.time() - self._shoot_stamp >= definitions.FIRE_RATE:
            self._shoot_stamp = time.time()
            self.shoot()

        return self.rect.move(self._x, self._y)

    def tick(self):
        """
        Used for updating the UI of player's child components
        """
        _bullets = self.bullets
        for bul in _bullets:
            if self._is_enemy:
                bul.y = bul.y + definitions.BULLET_SPEED
            else:
                bul.y = bul.y - definitions.BULLET_SPEED
            if bul.y <= -30 or bul.y > definitions.SCREEN_HEIGHT + 54:
                self._bullets.remove(bul)

    def player_info(self):
        plr = {'username': self.username, 'x': self._x,
               'y': self._y, 'bullets': []}
        for bull in self._bullets:
            plr['bullets'].append(
                {'id': bull.id, 'x': bull.x, 'y': bull.y})

        return plr
