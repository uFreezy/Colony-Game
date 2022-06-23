from abc import ABC


class Entity(ABC):
    """
    Class representation of abstract entity.
    """

    def __init__(self, sprite_uri):
        self._sprite_uri = sprite_uri

    @property
    def sprite_uri(self):
        return self._sprite_uri
