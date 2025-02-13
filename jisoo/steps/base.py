from jisoo.models.state import Task
from jisoo.models.common import (
    ServiceType,
    INTEGRATION_PATTERN_SUPPORT,
    CommonObject,
    INTEGRATION_SDK_RESOURCES,
)
from pydantic import model_validator
from typing import Literal, Any, Optional, Dict, TypeVar, ClassVar
from enum import Enum

T = TypeVar("T", bound="CommonObject")


class Service(Task):
    """
    A service class that handles AWS service integration configurations for state machines.

    Attributes:
        service (ServiceType): The type of AWS service to integrate with
        integration_type (Literal["optimized", "aws-sdk"]): Integration method with AWS services
        integration_pattern (Literal[None, "runTask", "waitForTaskToken"]): Task execution pattern
        action (Enum): The service action to perform
    """

    # Class level constants
    INTEGRATION_PATTERNS: ClassVar[Dict] = {
        "runTask": "sync",
        "waitForTaskToken": "waitForTaskToken",
    }

    PATTERN_MESSAGES: ClassVar[Dict] = {
        "runTask": "Run a Job (.sync)",
        "waitForTaskToken": "Wait for Callback (.waitForTaskToken)",
    }

    # Pydantic model fields
    service: ServiceType
    integration_type: Literal["optimized", "aws-sdk"] = "optimized"
    integration_pattern: Literal[None, "runTask", "waitForTaskToken"] = None
    action: Enum

    def __init__(self, **data):
        super().__init__(**data)
        self.resource = self.set_resource()
        self.parameters = self.set_parameters()

    def set_resource(self) -> str:
        """
        Constructs the AWS resource ARN based on service configuration.

        Returns:
            str: The complete AWS resource ARN
        """
        base_prefix = "arn:aws:states:::"
        prefix = (
            f"{base_prefix}aws-sdk:"
            if self.integration_type == "aws-sdk"
            else base_prefix
        )
        if self.integration_type == "aws-sdk":
            service = INTEGRATION_SDK_RESOURCES[self.service.value]
        else:
            service = self.service.value
        resource = f"{prefix}{service}:{self.action.value}"

        if self.integration_pattern:
            suffix = self.INTEGRATION_PATTERNS[self.integration_pattern]
            resource = f"{resource}.{suffix}"

        return resource

    def set_parameters(self) -> dict:
        """
        Builds the parameters dictionary for the service configuration.

        Returns:
            dict: Parameters formatted in PascalCase with properly transformed values
        """

        def transform_value(value: Any) -> Any:
            if isinstance(value, CommonObject):
                return value.to_dict()
            if isinstance(value, list) and value and isinstance(value[0], CommonObject):
                return [item.to_dict() for item in value]

            return value

        service_fields = set(Service.model_fields.keys())
        return {
            self.to_pascalcase(param): transform_value(getattr(self, param))
            for param in (set(self.model_fields.keys()) - service_fields)
            if getattr(self, param) is not None
        }

    @model_validator(mode="after")
    def validate_integration_pattern(self) -> "Service":
        """
        Validates the integration pattern compatibility with the service and integration type.

        Raises:
            ValueError: If the integration pattern is not supported

        Returns:
            Service: The validated service instance
        """
        if not self.integration_pattern:
            return self

        if self.integration_type == "optimized":
            self._validate_optimized_integration()
        elif self.integration_type == "aws-sdk":
            self._validate_aws_sdk_integration()

        return self

    def _validate_optimized_integration(self) -> None:
        """Validates integration pattern for optimized integration type."""
        if self.integration_pattern not in INTEGRATION_PATTERN_SUPPORT[self.service]:
            raise ValueError(
                f"{self.PATTERN_MESSAGES[self.integration_pattern]} is not "
                f"supported for {self.service.name}."
            )

    def _validate_aws_sdk_integration(self) -> None:
        """Validates integration pattern for AWS SDK integration type."""
        if self.integration_pattern == "runTask":
            raise ValueError(
                f"{self.PATTERN_MESSAGES[self.integration_pattern]} is not "
                "supported for AWS SDK integration."
            )

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
        """
        Override model_dump to only include fields from parent Task class.

        Returns:
            dict[str, Any]: Dictionary containing only the parent Task fields
        """
        parent_fields = set(Task.model_fields.keys()) | {"next", "end"}

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
