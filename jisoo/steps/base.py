from jisoo.models.state import Task
from jisoo.models.common import ServiceType, INTEGRATION_PATTERN_SUPPORT
from pydantic import model_validator
from typing import Literal, Any, Optional
from enum import Enum


class Service(Task):
    service: ServiceType
    integration_type: Literal["optimized", "aws-sdk"] = "optimized"
    integration_pattern: Literal[None, "runTask", "waitForTaskToken"] = None
    action: Enum

    def set_resource(self) -> str:
        integration_suffix = {
            "runTask": "sync",
            "waitForTaskToken": "waitForTaskToken",
        }
        prefix = "arn:aws:states:::"
        prefix = prefix + "aws-sdk:" if self.integration_type == "aws-sdk" else prefix
        resource = f"{prefix}{self.service.value}:{self.action.value}"
        if self.integration_pattern:
            resource = f"{resource}.{integration_suffix[self.integration_pattern]}"
        return resource

    def set_parameters(self) -> dict:
        params = set(self.model_fields.keys()) - set(Service.model_fields.keys())
        parameters = {}
        for param in params:
            if getattr(self, param):
                parameters[self.to_pascalcase(param)] = getattr(self, param)
        return parameters

    @model_validator(mode="after")
    def valid_supported_pattern(self):
        msg = {
            "runTask": "Run a Job (.sync)",
            "waitForTaskToken": "Wait for Callback (.waitForTaskToken)",
        }
        if self.integration_type == "optimized":
            if (
                self.integration_pattern
                and self.integration_pattern
                not in INTEGRATION_PATTERN_SUPPORT[self.service]
            ):
                raise ValueError(
                    f"{msg[self.integration_pattern]} is not supported for {self.service.name}."
                )
        elif self.integration_type == "aws-sdk":
            if self.integration_pattern == "runTask":
                raise ValueError(
                    f"{msg[self.integration_pattern]} is not supported for AWS SDK integration."
                )

        self.resource = self.set_resource()
        self.parameters = self.set_parameters()
        return self

    def model_dump(
        self,
        *,
        mode: str = "python",
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> dict[str, Any]:
        """Override model_dump to only include fields from parent Task class."""
        # Get all fields from parent class (Task)
        parent_fields = set(Task.model_fields.keys())

        # Call parent's model_dump with include set to parent fields
        return super().model_dump(
            mode=mode,
            include=parent_fields,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )
