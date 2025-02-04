from jisoo.models.rule.base import Rule, CompoundRule, NotRule
from typing import List, Union


class Condition:
    """
    Factory class for creating a choice rule.
    """

    @staticmethod
    def _create_rule(
        operator: str, variable: str, value: Union[str, int, float, bool]
    ) -> Rule:
        return Rule(variable=variable, operator=operator, value=value)

    @classmethod
    def StringEquals(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringEquals", variable, value)

    @classmethod
    def StringEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringEqualsPath", variable, value)

    @classmethod
    def StringLessThan(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringLessThan", variable, value)

    @classmethod
    def StringLessThanPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringLessThanPath", variable, value)

    @classmethod
    def StringGreaterThan(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringGreaterThan", variable, value)

    @classmethod
    def StringGreaterThanPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringGreaterThanPath", variable, value)

    @classmethod
    def StringLessThanEquals(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringLessThanEquals", variable, value)

    @classmethod
    def StringLessThanEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringLessThanEqualsPath", variable, value)

    @classmethod
    def StringGreaterThanEquals(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringGreaterThanEquals", variable, value)

    @classmethod
    def StringGreaterThanEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringGreaterThanEqualsPath", variable, value)

    @classmethod
    def NumericEquals(cls, variable: str, value: Union[int, float]) -> Rule:
        return cls._create_rule("NumericEquals", variable, value)

    @classmethod
    def NumericEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("NumericEqualsPath", variable, value)

    @classmethod
    def NumericLessThan(cls, variable: str, value: Union[int, float]) -> Rule:
        return cls._create_rule("NumericLessThan", variable, value)

    @classmethod
    def NumericLessThanPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("NumericLessThanPath", variable, value)

    @classmethod
    def NumericGreaterThan(cls, variable: str, value: Union[int, float]) -> Rule:
        return cls._create_rule("NumericGreaterThan", variable, value)

    @classmethod
    def NumericGreaterThanPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("NumericGreaterThanPath", variable, value)

    @classmethod
    def NumericLessThanEquals(cls, variable: str, value: Union[int, float]) -> Rule:
        return cls._create_rule("NumericLessThanEquals", variable, value)

    @classmethod
    def NumericLessThanEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("NumericLessThanEqualsPath", variable, value)

    @classmethod
    def NumericGreaterThanEquals(cls, variable: str, value: Union[int, float]) -> Rule:
        return cls._create_rule("NumericGreaterThanEquals", variable, value)

    @classmethod
    def NumericGreaterThanEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("NumericGreaterThanEqualsPath", variable, value)

    @classmethod
    def BooleanEquals(cls, variable: str, value: bool) -> Rule:
        return cls._create_rule("BooleanEquals", variable, value)

    @classmethod
    def BooleanEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("BooleanEqualsPath", variable, value)

    @classmethod
    def TimestampEquals(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampEquals", variable, value)

    @classmethod
    def TimestampEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampEqualsPath", variable, value)

    @classmethod
    def TimestampLessThan(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampLessThan", variable, value)

    @classmethod
    def TimestampLessThanPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampLessThanPath", variable, value)

    @classmethod
    def TimestampGreaterThan(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampGreaterThan", variable, value)

    @classmethod
    def TimestampGreaterThanPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampGreaterThanPath", variable, value)

    @classmethod
    def TimestampLessThanEquals(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampLessThanEquals", variable, value)

    @classmethod
    def TimestampLessThanEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampLessThanEqualsPath", variable, value)

    @classmethod
    def TimestampGreaterThanEquals(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampGreaterThanEquals", variable, value)

    @classmethod
    def TimestampGreaterThanEqualsPath(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("TimestampGreaterThanEqualsPath", variable, value)

    @classmethod
    def IsNull(cls, variable: str, value: bool) -> Rule:
        return cls._create_rule("IsNull", variable, value)

    @classmethod
    def IsPresent(cls, variable: str, value: bool) -> Rule:
        return cls._create_rule("IsPresent", variable, value)

    @classmethod
    def IsString(cls, variable: str, value: bool) -> Rule:
        return cls._create_rule("IsString", variable, value)

    @classmethod
    def IsNumeric(cls, variable: str, value: bool) -> Rule:
        return cls._create_rule("IsNumeric", variable, value)

    @classmethod
    def IsTimestamp(cls, variable: str, value: bool) -> Rule:
        return cls._create_rule("IsTimestamp", variable, value)

    @classmethod
    def IsBoolean(cls, variable: str, value: bool) -> Rule:
        return cls._create_rule("IsBoolean", variable, value)

    @classmethod
    def StringMatches(cls, variable: str, value: str) -> Rule:
        return cls._create_rule("StringMatches", variable, value)

    @classmethod
    def And(cls, rules: List[Rule]) -> CompoundRule:
        return CompoundRule(operator="And", rules=rules)

    @classmethod
    def Or(cls, rules: List[Rule]) -> CompoundRule:
        return CompoundRule(operator="Or", rules=rules)

    @classmethod
    def Not(cls, rule: Rule) -> NotRule:
        return NotRule(rule=rule)
