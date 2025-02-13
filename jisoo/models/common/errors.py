from enum import Enum
from jisoo.models.common.lambda_function.errors import LambdaErrorEqualsEnum
from jisoo.models.common.eventbridge.errors import EventsErrorEqualsEnum


class ErrorEqualsEnum:
    Events = EventsErrorEqualsEnum
    Lambda = LambdaErrorEqualsEnum
