import abc
import inspect

from typing import Any, Dict


class Rule(abc.ABC):
    @staticmethod
    def get_args_keys(child_class, rule_args):
        init_signature = inspect.signature(child_class.__init__)

        rule_args_keys = [
            item for item in init_signature.parameters.keys() if item != "self"
        ]

        if not rule_args_keys:
            return {}

        if len(rule_args_keys) != len(rule_args):
            raise Exception("Invalid rule arguments")

        return dict(zip(rule_args_keys, rule_args))

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.field = None
        self.value = None

    @abc.abstractmethod
    def validate(self):
        raise NotImplementedError

    def get_message(self):
        return None

    def get_formatted_message(
        self,
        messages: Dict[str, str],
        field: str,
        rule_item: str,
    ):
        if f"{field}.{rule_item}" in messages:
            message = messages[f"{field}.{rule_item}"]
        elif field in messages:
            message = messages[field]
        else:
            message = self.get_message()

        return message.format(field=self.field, value=self.value)

    def set_meta(self, field: str, value: Any):
        self.field = field
        self.value = value

        return self
