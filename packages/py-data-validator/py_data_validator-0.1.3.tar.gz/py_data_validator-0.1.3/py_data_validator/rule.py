import abc

from typing import Any, Dict, Literal

from py_data_validator.libs.helpers import pascal_to_snake


class Rule(abc.ABC):

    def __init__(self, *args, **kwargs) -> None:
        self.__args = args
        self.__kwargs = kwargs

        self.__rule_type = None
        self.__field = None
        self.__value = None
        self.__data = None

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

    @property
    def rule_type(self):
        return self.__rule_type

    @property
    def field(self):
        return self.__field

    @property
    def data(self):
        return self.__data

    @property
    def value(self):
        return self.__value

    @property
    def rule_name(self):
        return pascal_to_snake(self.__class__.__name__)

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

    def set_meta(
        self,
        rule_type: Literal["string", "object"],
        field: str,
        value: Any,
        data: Dict[str, Any],
    ):
        self.__rule_type = rule_type
        self.__field = field
        self.__value = value
        self.__data = data

        return self

    def require_params_count(self, count, parmas, rule):
        if len(parmas) < count:
            raise Exception(
                f"Validation rule {rule} requires at least {count} parameters."
            )
