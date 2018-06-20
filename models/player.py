import pygame
import definitions
import time
from models.projectile import Projectile


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_uri, is_enemy, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.username = ""
        self.isEnemy = is_enemy
        self.image = pygame.image.load(sprite_uri)
        self.image = pygame.transform.scale(self.image, (definitions.PLAYER_SIZE, definitions.PLAYER_SIZE))
        self.posX = pos_x
        self.posY = pos_y
        self.hp = 100  # TODO: put the starter HP in a const
        self.shootStamp = time.time()

        self.bullets = []

        if self.isEnemy:
            self.image = pygame.transform.flip(self.image, False, True)

        # TODO: firerate  *serverside too*

        self.rect = self.image.get_rect()

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_rect(self):
        return self.rect

    def get_username(self):
        if self.username:
            return self.username
        else:
            return ""

    def set_username(self, username):
        self.username = username

    def get_x(self):
        return self.posX

    def get_y(self):
        return self.posY

    def get_bullets(self):
        return self.bullets

    # ???
    def add_bullet(self, sprite_uri, x, y):
        self.bullets.append(Projectile(sprite_uri, self.isEnemy, x, y))
        # TODO: Propagate the bullet addition to the server

    def clear_bullets(self):
        self.bullets = []

    def shoot(self):
        self.add_bullet(definitions.BLUE_LASER_SPRITE,
                        self.get_x(), self.get_y() - 50)

    def handle_input(self, input_keys):
        if input_keys[pygame.K_UP] == 1 and self.posY > 0:
            self.posY -= definitions.MOVEMENT_SPEED
        if input_keys[pygame.K_DOWN] == 1 and self.posY < definitions.SCREEN_HEIGHT - definitions.PLAYER_SIZE:
            self.posY += definitions.MOVEMENT_SPEED
        if input_keys[pygame.K_LEFT] == 1 and self.posX > 0:
            self.posX -= definitions.MOVEMENT_SPEED
        if input_keys[pygame.K_RIGHT] == 1 and self.posX < definitions.SCREEN_WIDTH - definitions.PLAYER_SIZE:
            self.posX += definitions.MOVEMENT_SPEED
        if input_keys[pygame.K_SPACE] == 1 and time.time() - self.shootStamp >= definitions.FIRE_RATE:
            self.shootStamp = time.time()
            self.shoot()

        # TODO: Send socket event that input is present to the server

        return self.get_rect().move(self.posX, self.posY)

    # Used for updating the UI of player's child components
    def tick(self):
        bullets = self.get_bullets()
        for bul in bullets:
            if self.isEnemy:
                bul.set_y(bul.get_y() + definitions.BULLET_SPEED)
            else:
                bul.set_y(bul.get_y() - definitions.BULLET_SPEED)
            if bul.get_y() <= -30 or bul.get_y() > definitions.SCREEN_HEIGHT + 54:
                self.bullets.remove(bul)

    def get_player_info(self):
        plr = {'username': self.username, 'x': self.posX, 'y': self.posY, 'bullets': []}
        for bull in self.bullets:
            plr['bullets'].append({'id': bull.get_id(), 'x': bull.get_x(), 'y': bull.get_y()})

        return plr
