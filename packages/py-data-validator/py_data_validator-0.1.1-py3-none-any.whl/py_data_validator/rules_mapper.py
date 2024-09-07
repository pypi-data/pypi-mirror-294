import importlib
import os

from py_data_validator.rule import Rule


class RulesMapper:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(RulesMapper, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized"):
            return
        else:
            self.__package_name = "py_data_validator"

            self.__rules_executors = self.get_rules_mappings()

            self._initialized = True

    def get_rules_mappings(self):
        rules_directory = os.path.join(os.path.dirname(__file__), "rules")

        rules_mappings = {}

        for filename in os.listdir(rules_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                rule_name = filename[:-3]

                class_name = self.snake_to_pascal(rule_name)

                try:
                    module = importlib.import_module(
                        f"{self.__package_name}.rules.{rule_name}"
                    )

                    rule_class = getattr(module, class_name)

                    rules_mappings[rule_name] = rule_class
                except (ImportError, AttributeError) as e:
                    print(f"Failed to load rule '{rule_name}': {e}")

        return rules_mappings

    def snake_to_pascal(self, rule_name):
        return "".join(word.capitalize() for word in rule_name.split("_"))

    def get_rule_executor(self, rule: str | Rule):
        try:
            return self.__rules_executors[rule]
        except KeyError:
            raise Exception(f"Rule `{rule}` does not exists.")
