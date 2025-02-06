from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict
from jisoo.models.common.base import (
    CommonObject,
    KeyValuePair,
    EnvironmentFile,
    ResourceRequirement,
)


class ContainerOverride(CommonObject):
    """Represents the overrides that are sent to a container."""

    name: str  # The name of the container that receives the override
    command: Optional[List[str]] = Field(
        None, description="The command to send to the container."
    )
    cpu: Optional[int] = Field(
        None, description="The number of CPU units reserved for the container."
    )
    environment: Optional[List[KeyValuePair]] | List[dict] = Field(
        None, description="The environment variables to send to the container."
    )
    environment_files: Optional[List[EnvironmentFile]] | List[dict] = Field(
        None,
        description="Files containing environment variables to pass to a container.",
    )
    memory: Optional[int] = Field(
        None,
        description="The hard limit (in MiB) of memory to present to the container.",
    )
    memory_reservation: Optional[int] = Field(
        None,
        description="The soft limit (in MiB) of memory to reserve for the container.",
    )
    resource_requirements: Optional[List[ResourceRequirement]] | List[dict] = Field(
        None, description="The type and amount of a resource to assign to a container."
    )

    @model_validator(mode="after")
    def set_to_dict(self):
        if self.environment_files:
            self.environment_files = [
                i.to_dict() if isinstance(i, CommonObject) else i
                for i in self.environment_files
            ]
        if self.environment:
            self.environment = [
                i.to_dict() if isinstance(i, CommonObject) else i
                for i in self.environment
            ]
        if self.resource_requirements:
            self.resource_requirements = [
                i.to_dict() if isinstance(i, CommonObject) else i
                for i in self.resource_requirements
            ]
        return self


class TaskOverride(CommonObject):
    container_overrides: Optional[List[ContainerOverride]] | Optional[List[Dict]] = None
    cpu: Optional[str] = None
    ephemeral_storage: Optional[Dict] = None
    execution_role_arn: Optional[str] = None
    inference_accelerator_overrides: Optional[List[Dict]] = None
    memory: Optional[str] = None
    task_role_arn: Optional[str] = None

    @model_validator(mode="after")
    def set_to_dict(self):
        self.container_overrides = [
            i.to_dict() if isinstance(i, CommonObject) else i
            for i in self.container_overrides
        ]
        return self
