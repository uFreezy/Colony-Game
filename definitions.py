import os

# Project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BACKGROND_SPRITE = ROOT_DIR + "/assets/Backgrounds/blue.png"
PLAYER_SPRITE = ROOT_DIR + "/assets/PNG/playerShip1_blue.png"
ENEMY_SPRITE = ROOT_DIR + "/assets/PNG/playerShip1_red.png"
BLUE_LASER_SPRITE = ROOT_DIR + "/assets/PNG/Lasers/laserBlue01.png"
RED_LASER_SPRITE = ROOT_DIR + "/assets/PNG/Lasers/laserRed01.png"
PLAYER_SIZE = 30
SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640
MOVEMENT_SPEED = 3
BULLET_SPEED = 5
FIRE_RATE = 0.7
BULLET_DAMAGE = 5
BULLET_SIZE = 50
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12347
MESSAGE_SIZE = 11
INFO_MESSAGE = (255, 255, 255)
ERROR_MESSAGE = (255, 0, 0)
PLAYER_HEALTH = (50, 205, 50)
ENEMY_HEALTH = (220, 20, 60)
SERVER_INACTIVE = "Server is inactive! Try again later!"
CONN_REFUSED = "The server refused to connect! Try again later!"
GAME_CRASHED = "The game has crashed. Try again later!"
