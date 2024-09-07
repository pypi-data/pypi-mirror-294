from py_data_validator.rule import Rule


class Accepted(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.accepts = ["yes", "on", 1, "1", True, "true"]

    def validate(self):
        return self.value in self.accepts

    def get_message(self):
        return "{field} must be a valid email address"
