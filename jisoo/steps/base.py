from jisoo.models.state import Task
from jisoo.models.common import ServiceType, INTEGRATION_PATTERN_SUPPORT
from pydantic import computed_field, model_validator, field_validator, ValidationInfo
from typing import Literal
from enum import Enum


class Service(Task):
    service: ServiceType
    integration_type: Literal["optimized", "aws-sdk"] = "optimized"
    integration_pattern: Literal[None, "runTask", "waitForTaskToken"] = None
    action: Enum

    @computed_field
    def resouce(self) -> str:
        prefix = "arn:aws:states:::"
        prefix = prefix + "aws-sdk:" if self.integration_type == "aws-sdk" else prefix
        resouce = f"{prefix}{self.service.value}:{self.action.value}"
        if self.integration_pattern:
            resouce = f"{resouce}.{self.integration_pattern}"
        return resouce

    @model_validator(mode="after")
    def valid_supported_pattern(self):

        if (
            self.integration_pattern
            and self.integration_pattern
            not in INTEGRATION_PATTERN_SUPPORT[self.service]
        ):
            raise ValueError(
                f"{self.integration_pattern} is not supported for {self.service.name}"
            )
