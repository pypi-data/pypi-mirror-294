from py_data_validator.rule import Rule


class Required(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        return self.value is None

    def get_message(self):
        return "{field} is required"
