import re

from py_data_validator.rule import Rule


class Email(Rule):
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def __init__(self) -> None:
        super().__init__()

    def validate(self):
        if not self.value or not re.match(self.EMAIL_REGEX, str(self.value)):
            return False

        return True

    def get_message(self):
        return "{field} must be a valid email address"
