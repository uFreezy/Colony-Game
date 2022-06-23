"""
Module hosting utility functions used for network communication.
"""
import pickle
import socket
from io import BlockingIOError
import definitions

import utils.global_vars as glVars
from models.message import Message
from utils.global_vars import MESSAGES


def socket_init():
    """
    Initializes a network socket to be used by the server.
    """
    try:
        soc = socket.socket()
        soc.connect((definitions.SERVER_HOST, definitions.SERVER_PORT))
        soc.setblocking(0)

        return soc
    except ConnectionRefusedError:
        glVars.messages.append(
            Message(definitions.CONN_REFUSED, definitions.ERROR_MESSAGE))
        glVars.isServerActive = False

    return None


def parse_socket_data(soc):
    """
    Receives and parses data from the network.
    Parses the received data from bytes to python objects.
    """
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
        MESSAGES.append(Message(definitions.CONN_REFUSED,
                        definitions.ERROR_MESSAGE))

    return None


def send_data(soc, data):
    """
    Sends data over the network
    """
    try:
        soc.send(pickle.dumps(data))
    except BlockingIOError:
        pass
    except AttributeError:
        MESSAGES.append(Message(definitions.SERVER_INACTIVE,
                        definitions.ERROR_MESSAGE))
        glVars.isServerActive = False
    except BrokenPipeError:
        MESSAGES.append(Message(definitions.GAME_CRASHED,
                        definitions.ERROR_MESSAGE))
        glVars.isServerActives = False
