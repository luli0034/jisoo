from enum import Enum
from typing import Any, ClassVar, Dict, Literal, Optional, TypeVar, Union
from pydantic import model_validator

from jisoo.models.state import Task
from jisoo.models.common import (
    ServiceType,
    INTEGRATION_PATTERN_SUPPORT,
    CommonObject,
    INTEGRATION_SDK_RESOURCES,
    JSONPath,
)
from jisoo.utils import to_pascalcase, process_context

T = TypeVar("T", bound="CommonObject")


class Service(Task):
    """
    A service class that handles AWS service integration configurations for state machines.

    This class manages the configuration and validation of AWS service integrations,
    including resource ARN construction and parameter formatting.

    Attributes:
        service (ServiceType): The type of AWS service to integrate with
        integration_type (Literal["optimized", "aws-sdk"]): Integration method with AWS services
        integration_pattern (Literal[None, "runTask", "waitForTaskToken"]): Task execution pattern
        action (Enum): The service action to perform
        resource (str): The constructed AWS resource ARN
        parameters (dict): Formatted parameters for the service configuration
    """

    # Class level constants with better type hints
    INTEGRATION_PATTERNS: ClassVar[Dict[str, str]] = {
        "runTask": "sync",
        "waitForTaskToken": "waitForTaskToken",
    }

    PATTERN_MESSAGES: ClassVar[Dict[str, str]] = {
        "runTask": "Run a Job (.sync)",
        "waitForTaskToken": "Wait for Callback (.waitForTaskToken)",
    }

    TASK_FIELD_KEYS: ClassVar[set[str]] = set(Task.model_fields.keys())

    # Pydantic model fields
    service: ServiceType
    integration_type: Literal["optimized", "aws-sdk"] = "optimized"
    integration_pattern: Optional[Literal["runTask", "waitForTaskToken"]] = None
    action: Enum

    def __init__(self, **data: Any) -> None:
        """Initialize the Service with the given configuration."""
        super().__init__(**data)
        self.resource = self._build_resource()
        self.parameters = self._build_parameters()

    def _build_resource(self) -> str:
        """
        Construct the AWS resource ARN based on service configuration.

        Returns:
            str: The complete AWS resource ARN
        """
        base_prefix = "arn:aws:states:::"
        is_sdk = self.integration_type == "aws-sdk"

        service_name = (
            INTEGRATION_SDK_RESOURCES[self.service.value]
            if is_sdk
            else self.service.value
        )

        resource = f"{base_prefix}{'aws-sdk:' if is_sdk else ''}{service_name}:{self.action.value}"

        if self.integration_pattern:
            resource = (
                f"{resource}.{self.INTEGRATION_PATTERNS[self.integration_pattern]}"
            )

        return resource

    def _build_parameters(self) -> dict:
        """
        Build the parameters dictionary for the service configuration.

        Returns:
            dict: Parameters formatted in PascalCase with properly transformed values
        """

        service_fields = set(self.model_fields.keys()) - set(
            Service.model_fields.keys()
        )
 

        return {
            to_pascalcase(key): value
            for field in service_fields
            if (field_value := getattr(self, field)) is not None
            for key, value in [process_context(field, field_value)]
        }

    @model_validator(mode="after")
    def validate_integration_pattern(self) -> "Service":
        """
        Validate the integration pattern compatibility with the service and integration type.

        Raises:
            ValueError: If the integration pattern is not supported

        Returns:
            Service: The validated service instance
        """
        if not self.integration_pattern:
            return self

        if self.integration_type == "optimized":
            if (
                self.integration_pattern
                not in INTEGRATION_PATTERN_SUPPORT[self.service]
            ):
                raise ValueError(
                    f"{self.PATTERN_MESSAGES[self.integration_pattern]} is not "
                    f"supported for {self.service.name}."
                )
        elif self.integration_pattern == "runTask":
            raise ValueError(
                f"{self.PATTERN_MESSAGES[self.integration_pattern]} is not "
                "supported for AWS SDK integration."
            )

        return self

    def model_dump(
        self,
        *,
        mode: str = "python",
        include: Optional[Any] = None,
        exclude: Optional[Any] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool = True,
    ) -> Dict[str, Any]:
        """
        Override model_dump to only include fields from parent Task class.

        Returns:
            Dict[str, Any]: Dictionary containing only the parent Task fields
        """
        parent_fields = self.TASK_FIELD_KEYS | {"next", "end"}

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
