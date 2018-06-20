import definitions
import pygame

from models.message import Message


def init_screen(size):
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Colony')

    return screen


def draw_obj(screen, obj):
    screen.blit(obj.get_image(), (obj.get_x(), obj.get_y()))


def text_objects(message, font):
    text_surface = font.render(message.get_text(), True, message.get_type())
    return text_surface, text_surface.get_rect()


def draw_message(screen, message, text_size, coordinates):
    # Test font
    large_text = pygame.font.Font('freesansbold.ttf', text_size)
    text_surf, text_rect = text_objects(message, large_text)

    screen.blit(text_surf, coordinates)


def draw_existing_messages(screen, messages):
    if messages:
        y = definitions.SCREEN_HEIGHT - (definitions.MESSAGE_SIZE + 10)
        for msg in messages:
            draw_message(screen, msg, definitions.MESSAGE_SIZE, (10, y))
            y -= definitions.MESSAGE_SIZE + 10
            # if msg.getType() is definitions.ERROR_MESSAGE:
            # break


def draw_health_ui(screen, player_health, enemy_health):
    draw_message(screen, Message("Health : " + str(player_health), definitions.PLAYER_HEALTH), 15,
                 (definitions.SCREEN_WIDTH - 95, definitions.SCREEN_HEIGHT - 25))
    draw_message(screen, Message("Health : " + str(enemy_health), definitions.ENEMY_HEALTH), 15,
                 (definitions.SCREEN_WIDTH - 95, 10))


def draw_username_ui(screen, pl_usr, en_usr):
    font = pygame.font.Font('freesansbold.ttf', definitions.MESSAGE_SIZE)
    pl = font.render(pl_usr, True, (255, 255, 255))
    if en_usr == '':
        en_usr = '-'
    en = font.render(en_usr, True, (255, 255, 255))

    screen.blit(pl, (definitions.SCREEN_WIDTH - 95, definitions.SCREEN_HEIGHT - 45))
    screen.blit(en, (definitions.SCREEN_WIDTH - 95, 30))
