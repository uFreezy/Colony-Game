import definitions


class Message:
    def __init__(self, msg_text, msg_type):
        is_string = isinstance(msg_text, str)
        is_type_allowed = msg_type is definitions.INFO_MESSAGE or definitions.ERROR_MESSAGE

        if is_string and is_type_allowed:
            self._msg_text = msg_text
            self._msg_type = msg_type
        else:
            raise TypeError('Invalid message arguments')

    @property
    def text(self):
        return self._msg_text

    @property
    def type(self):
        return self._msg_type
