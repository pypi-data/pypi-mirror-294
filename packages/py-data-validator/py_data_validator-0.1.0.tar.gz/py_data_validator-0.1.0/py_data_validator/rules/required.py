from py_data_validator.rule import Rule


class Required(Rule):
    def __init__(self) -> None:
        super().__init__()

    def validate(self):
        if not self.value:
            return False

        return True

    def get_message(self):
        return "{field} is required"
