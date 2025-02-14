from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from jisoo.models.common.base import CommonObject


class AwsVpcConfiguration(CommonObject):
    """Represents the networking details for a task or service in Amazon ECS."""

    subnets: List[str] = Field(
        ...,
        description="The IDs of the subnets associated with the task or service. Maximum of 16 subnets.",
    )
    assign_public_ip: Optional[str] = Field(
        "ENABLED",
        description="Whether the task's elastic network interface receives a public IP address. Valid values: 'ENABLED' or 'DISABLED'.",
    )
    security_groups: Optional[List[str]] = Field(
        None,
        description="The IDs of the security groups associated with the task or service. Maximum of 5 security groups.",
    )


class NetworkConfiguration(CommonObject):
    awsvpc_configuration: AwsVpcConfiguration | dict
