from jisoo.models.state import Task
from jisoo.models.common import ServiceType, INTEGRATION_PATTERN_SUPPORT
from pydantic import computed_field, model_validator, field_validator, ValidationInfo
from typing import Literal, Any, Optional
from enum import Enum


class Service(Task):
    service: ServiceType
    integration_type: Literal["optimized", "aws-sdk"] = "optimized"
    integration_pattern: Literal[None, "runTask", "waitForTaskToken"] = None
    action: Enum

    def set_resource(self) -> str:
        prefix = "arn:aws:states:::"
        prefix = prefix + "aws-sdk:" if self.integration_type == "aws-sdk" else prefix
        resource = f"{prefix}{self.service.value}:{self.action.value}"
        if self.integration_pattern:
            resource = f"{resource}.{self.integration_pattern}"
        return resource

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

        self.resource = self.set_resource()
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


class Step:

    def __init__(
        self,
        id: str,
        integration_type: Literal["optimized", "aws-sdk"],
        integration_pattern: Literal[None, "runTask", "waitForTaskToken"],
        input_path: Optional[str] = None,
        output_path: Optional[str] = None,
        result_path: Optional[str] = None,
        result_selector: Optional[str] = None,
        credentials: Optional[dict] = None,
        timeout_seconds: Optional[int] = None,
        timeout_seconds_path: Optional[str] = None,
        heartbeat_seconds: Optional[int] = None,
        heartbeat_seconds_path: Optional[str] = None

    ):
        self.id = id
        self.integration_type = integration_type
        self.integration_pattern = integration_pattern
        self.input_path = input_path
        self.output_path = output_path
        self.result_path = result_path
        self.result_selector = result_selector
        self.credentials = credentials
        self.timeout_seconds = timeout_seconds
        self.timeout_seconds_path = timeout_seconds_path
        self.heartbeat_seconds = heartbeat_seconds
        self.heartbeat_seconds_path = heartbeat_seconds_path
        self.action = None
        self.service: Service = None
    
    def get_parameters(self) -> dict:
        raise NotImplementedError

    def __call__(self):
        return Service(
            id=self.id,
            service=self.service,
            action=self.action,
            integration_type=self.integration_type,
            integration_pattern=self.integration_pattern,
            parameters=self.get_parameters(),
            input_path=self.input_path,
            output_path=self.output_path,
            result_path=self.result_path,
            result_selector=self.result_selector,
            credentials=self.credentials,
            timeout_seconds=self.timeout_seconds,
            timeout_seconds_path=self.timeout_seconds_path,
            heartbeat_seconds=self.heartbeat_seconds,
            heartbeat_seconds_path=self.heartbeat_seconds_path
        )
