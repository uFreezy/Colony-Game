import collections

global messages
messages = collections.deque(maxlen=5)

global isServerActive
# noinspection PyRedeclaration
isServerActive = True
