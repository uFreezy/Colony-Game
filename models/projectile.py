import pygame

import definitions

from random import choice
from string import ascii_uppercase


class Projectile(pygame.sprite.Sprite):
    def __init__(self, sprite_uri, is_enemy, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.id = ''.join(choice(ascii_uppercase) for i in range(12))

        self.image = pygame.image.load(sprite_uri)
        self.image = pygame.transform.scale(self.image, (9, 54))

        self.posX = pos_x
        self.posY = pos_y
        self.damage = definitions.BULLET_DAMAGE

        if is_enemy:
            self.image = pygame.transform.flip(self.image, False, True)

    def get_id(self):
        return self.id

    def get_image(self):
        return self.image

    def get_x(self):
        return self.posX

    def get_y(self):
        return self.posY

    def set_y(self, y):
        self.posY = y
