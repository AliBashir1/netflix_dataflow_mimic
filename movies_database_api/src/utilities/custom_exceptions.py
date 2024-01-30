from datetime import date


class DateException(Exception):
    def __init__(self, value: date, message: str = None):
        self.value = value
        if message is None:
            self.message = f"""{value} is a wrong format. Please provide date in yyyy-mm-dd."""
        else:
            self.message = message
        super().__init__(self.message)
