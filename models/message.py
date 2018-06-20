import definitions


class Message:
    def __init__(self, msg_text, msg_type):
        is_string = isinstance(msg_text, str)
        is_type_allowed = msg_type is definitions.INFO_MESSAGE or definitions.ERROR_MESSAGE
        if is_string and is_type_allowed:
            self.msgText = msg_text
            self.msgType = msg_type
        else:
            raise TypeError('Invalid message arguments')

    def get_text(self):
        return self.msgText

    def get_type(self):
        return self.msgType
