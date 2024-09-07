from typing import Any, Dict, List
from py_data_validator.base_validator import BaseValidator
from py_data_validator.rule import Rule
from py_data_validator.rules_mapper import RulesMapper


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

        self.__validation_errors = {}

        self.__validated_data = {}

        self.__status = "pending"

        self.validate_payload()

        self.__rules_mapper = RulesMapper()

        self.__implicit_rules = [
            "accepted",
            "accepted_if",
            "declined",
            "declined_if",
            "filled",
            "missing",
            "missing_if",
            "missing_unless",
            "missing_with",
            "missing_with_all",
            "present",
            "present_if",
            "present_unless",
            "present_with",
            "present_with_all",
            "required",
            "required_if",
            "required_if_accepted",
            "required_if_declined",
            "required_unless",
            "required_with",
            "required_with_all",
            "required_without",
            "required_without_all",
        ]

    def validate(self) -> bool:
        try:
            if self.__status != "pending":
                return

            self.__validation_errors = {}

            self.__validated_data = {}

            for field, rule_items in self.rules.items():
                value = self.data.get(field, None)

                validatable = self.is_validatable(field, value, rule_items)

                if validatable:
                    self.process_validation(field, value, rule_items)
                else:
                    self.__validated_data[field] = value

            self.__status = len(self.__validation_errors.keys()) == 0
        except Exception as e:
            raise Exception(str(e))

    def process_validation(self, field, value, rule_items):
        for rule_item in rule_items:
            rule_executor = self.__get_rule_executor(field, rule_item, value)

            validated = rule_executor.validate()

            if validated:
                self.__validated_data[field] = value
            else:
                field_error = self.__validation_errors.setdefault(field, [])

                formatted_message = rule_executor.get_formatted_message(
                    self.messages, field, rule_item
                )

                field_error.append(formatted_message)

                if rule_item in self.__implicit_rules:
                    break

    def is_validatable(self, field, value, rule_items) -> bool:
        if "nullable" not in rule_items:
            return True

        return value is not None

    def passes(self):
        return self.validate()

    def fails(self):
        return not self.passes()

    def failed(self):
        if self.fails():
            return self.__validation_errors

        return None

    def validated(self):
        if self.passes():
            return self.__validated_data

        return None

    def __get_rule_executor(self, field: str, rule_item: str | Rule, value: Any):
        if isinstance(rule_item, Rule):
            return rule_item.set_meta(field, value)
        else:
            rule_with_args = rule_item.split(":")

            rule = rule_with_args[0]

            rule_args = None if len(rule_with_args) == 1 else rule_with_args[1]

            rule_args = rule_args.split(",") if rule_args else []

            rule_executor = self.__rules_mapper.get_rule_executor(rule)

            rule_args_mappings = (
                Rule.get_args_keys(rule_executor, rule_args) if rule_args else {}
            )

            return rule_executor(**rule_args_mappings).set_meta(field, value)
