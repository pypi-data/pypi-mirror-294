from typing import Any, Dict, List
from py_data_validator.base_validator import BaseValidator
from py_data_validator.rule import Rule
from py_data_validator.rules_mapper import RulesMapper
from py_data_validator.validation_response import ValidationResponse


class Validator(BaseValidator):
    def __init__(
        self,
        data: Dict[str, Any],
        rules: Dict[str, List[str | Rule]],
        messages: Dict[str, Any] | None = None,
    ):
        self.data = data

        self.rules = rules

        self.messages = messages or {}

        self.validate_payload()

        self.__validation_response = ValidationResponse(self.data)

        self.__rules_mapper = RulesMapper()

    def validate(self) -> ValidationResponse:
        try:
            for field, rule_items in self.rules.items():
                value = self.data.get(field, None)

                validatable = self.is_validatable(field, value, rule_items)

                if validatable:
                    self.__process_validation(field, value, rule_items, self.data)

            return self.__validation_response.execute()
        except Exception as e:
            raise Exception(str(e))

    def __process_validation(self, field, value, rule_items, data):
        for rule_item in rule_items:
            rule_executor = self.__get_rule_executor(field, rule_item, value, data)

            validated = rule_executor.validate()

            if not validated:
                formatted_message = rule_executor.get_formatted_message(
                    self.messages, field, rule_item
                )

                self.__validation_response.set_error(field, formatted_message)

                if rule_item in self.__rules_mapper.implicit_rules:
                    break

    def is_validatable(self, field, value, rule_items) -> bool:
        if "nullable" not in rule_items:
            return True

        return value is not None

    def __get_rule_executor(
        self, field: str, rule_item: str | Rule, value: Any, data: Dict[str, Any]
    ):
        if isinstance(rule_item, Rule):
            return rule_item.set_meta("object", field, value, data)
        else:
            rule_with_args = rule_item.split(":")

            rule = rule_with_args[0]

            rule_args = None if len(rule_with_args) == 1 else rule_with_args[1]

            rule_args = rule_args.split(",") if rule_args else []

            rule_executor = self.__rules_mapper.get_rule_executor(rule)

            return rule_executor(*rule_args).set_meta("string", field, value, data)
