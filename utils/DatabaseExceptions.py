class DatabaseTypeError(Exception):
    def __init__(self, value):
        self.value = value + " is not a valid DatabaseType"
    def __str__(self):
        return repr(self.value)

class DatabaseCursorError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
