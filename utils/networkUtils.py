import definitions
import pickle
import socket
from io import BlockingIOError

import utils.globalVars as glVars
from models.message import Message


def socket_init():
    try:
        soc = socket.socket()
        soc.connect((definitions.SERVER_HOST, definitions.SERVER_PORT))
        soc.setblocking(0)

        return soc
    except ConnectionRefusedError:
        glVars.messages.append(Message(definitions.CONN_REFUSED, definitions.ERROR_MESSAGE))
        glVars.isServerActive = False


def parse_socket_data(soc):
    try:
        raw_data = soc.recv(4096)

        if raw_data is not None:
            return pickle.loads(raw_data)
    except (BlockingIOError, ValueError):
        pass
    except EOFError:
        pass
    except pickle.UnpicklingError:
        return None
    except ConnectionResetError:
        glVars.messages.append(Message(definitions.CONN_REFUSED, definitions.ERROR_MESSAGE))


def send_data(soc, data):
    try:
        soc.send(pickle.dumps(data))
    except BlockingIOError:
        pass
    except AttributeError:
        glVars.messages.append(Message(definitions.SERVER_INACTIVE, definitions.ERROR_MESSAGE))
        glVars.isServerActive = False
    except BrokenPipeError:
        glVars.messages.append(Message(definitions.GAME_CRASHED, definitions.ERROR_MESSAGE))
        glVars.isServerActives = False
