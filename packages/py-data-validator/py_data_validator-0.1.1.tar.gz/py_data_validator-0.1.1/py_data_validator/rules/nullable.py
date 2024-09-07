from py_data_validator.rule import Rule


class Nullable(Rule):
    def __init__(self) -> None:
        super().__init__()

    def validate(self):
        return True
