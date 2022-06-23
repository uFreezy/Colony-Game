import pygame
import definitions


from models.message import Message


def init_screen(size):
    """
    Initializes a pygame game screen with a specific size and fixed name.
    """
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Colony')

    return screen


def draw_obj(screen, obj):
    """
    Draws given object on a given screen.
    """
    screen.blit(obj.image, (obj.x, obj.y))


def text_objects(message, font):
    """
    Creates text surface object from given string and font.
    """
    text_surface = font.render(message.text, True, message.type)
    return text_surface, text_surface.get_rect()


def draw_message(screen, message, text_size, coordinates):
    """
    Draws text on the screen with a specific size and fixed font.
    """
    # Test font
    large_text = pygame.font.Font('freesansbold.ttf', text_size)
    text_surf, _ = text_objects(message, large_text)

    screen.blit(text_surf, coordinates)


def draw_existing_messages(screen, messages):
    """
    Used to drawing the existing list of messages.
    It accepts list of strings and draws them in order.
    """
    if messages:
        y = definitions.SCREEN_HEIGHT - (definitions.MESSAGE_SIZE + 10)
        for msg in messages:
            draw_message(screen, msg, definitions.MESSAGE_SIZE, (10, y))
            y -= definitions.MESSAGE_SIZE + 10


def draw_health_ui(screen, player_health, enemy_health):
    """
    Used to draw both players health on the screen.
    """
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

    screen.blit(pl, (definitions.SCREEN_WIDTH - 95,
                definitions.SCREEN_HEIGHT - 45))
    screen.blit(en, (definitions.SCREEN_WIDTH - 95, 30))
