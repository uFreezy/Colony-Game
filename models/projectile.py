from random import choice
from string import ascii_uppercase

import pygame
import definitions


class Projectile(pygame.sprite.Sprite):
    """
    Class representation of the projectiles that the players shoot
    """

    def __init__(self, sprite_uri, is_enemy, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self._id = ''.join(choice(ascii_uppercase) for _ in range(12))
        self._image = pygame.image.load(sprite_uri)
        self._image = pygame.transform.scale(self._image, (9, 54))
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._damage = definitions.BULLET_DAMAGE

        if is_enemy:
            self._image = pygame.transform.flip(self._image, False, True)

    @property
    def id(self):
        return self._id

    @property
    def image(self):
        return self._image

    @property
    def x(self):
        return self._pos_x

    @property
    def y(self):
        return self._pos_y

    @y.setter
    def y(self, y):
        self._pos_y = y
