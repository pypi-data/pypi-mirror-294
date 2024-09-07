import re

from py_data_validator.rule import Rule


class Email(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def validate(self):
        if not self.value or not re.match(self.email_regex, str(self.value)):
            return False

        return True

    def get_message(self):
        return "{field} must be a valid email address"
