from typing import Callable
from py_data_validator.rule import Rule


class RequiredIf(Rule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self):
        args_count = 1 if self.rule_type == "object" else 3

        self.require_params_count(args_count, self.args, self.rule_name)

        object_argument_1 = self.args[0]

        if isinstance(object_argument_1, bool):
            return object_argument_1 and self.value is not None

        if isinstance(object_argument_1, Callable):
            return object_argument_1() and self.value is not None

        if self.rule_type == "string":
            field_left, operator, value_right = self.args

            value_left = self.data.get(field_left)

            self.expression = f"{value_left} {operator} {value_right}"

            status = eval(self.expression)

            if status and self.value is None:
                return False

            return True

        return False

    def get_message(self):
        if self.rule_type == "string":
            return f"{self.field} is required when {self.args}"

        return "{field} is required"
