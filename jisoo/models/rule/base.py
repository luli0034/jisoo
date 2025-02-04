from pydantic import BaseModel, field_validator, model_validator
from typing import List, Union
from jisoo.exception import InvalidRule


class BaseRule(BaseModel):
    def to_dict(self) -> dict:
        raise NotImplementedError


class Rule(BaseRule):
    """
    Class for creating a rule.
    """

    variable: str
    operator: str
    value: Union[str, int, float, bool]

    @field_validator("variable", mode="after")
    @classmethod
    def validate_variable(cls, v):
        if not v.startswith("$"):
            raise ValueError(f"Variable must start with '$', but got '{v}'")
        return v

    @model_validator(mode="after")
    def validate_value(self):

        VALIDATORS = {
            "String": (str,),
            "Numeric": (int, float),
            "Boolean": (bool,),
            "Timestamp": (str,),
            "Is": (bool,),
        }

        if self.operator.endswith("Path"):
            if not isinstance(self.value, str) or not self.value.startswith("$"):
                raise InvalidRule(
                    f"Value must be a path starting with '$', but got '{self.value}'"
                )
        else:
            for prefix, valid_types in VALIDATORS.items():
                if self.operator.startswith(prefix) and not isinstance(
                    self.value, valid_types
                ):
                    raise InvalidRule(
                        f"Expected value to be a {prefix}, but got {self.value}"
                    )

        return self

    def to_dict(self) -> dict:
        return {
            "Variable": self.variable,
            self.operator: self.value,
        }


class CompoundRule(BaseRule):
    """
    Class for creating a compound rule.
    """

    operator: str
    rules: List[Rule]

    @field_validator("rules", mode="after")
    @classmethod
    def validate_rules(cls, rules: List[Rule]):
        for rule in rules:
            if not isinstance(rule, Rule):
                raise InvalidRule(f"Rule '{rule}' is invalid")

        return rules

    def to_dict(self) -> dict:
        return {self.operator: [rule.to_dict() for rule in self.rules]}


class NotRule(BaseRule):
    """
    Class for creating a negation rule.
    """

    rule: Rule

    @field_validator("rule", mode="after")
    @classmethod
    def validate_rule(cls, rule: Rule):

        if not isinstance(rule, Rule):
            raise InvalidRule(f"Rule '{rule}' is invalid")

        return rule

    def to_dict(self) -> dict:
        return {"Not": self.rule.to_dict()}
