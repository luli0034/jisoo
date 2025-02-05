from jisoo.steps import Service
from jisoo.models.common import ServiceType
import pytest
from pydantic import ValidationError


def test_service():
    with pytest.raises(ValidationError):
        dynamodb = Service(
            service=ServiceType.DynamoDB,
            integration_type="aws-sdk",
            integration_pattern="runTask",
        )

    dynamodb = Service(
        service=ServiceType.DynamoDB,
        integration_type="aws-sdk",
    )

    _lambda = Service(
        service=ServiceType.Lambda,
        integration_type="aws-sdk",
        integration_pattern="waitForTaskToken",
    )

    with pytest.raises(ValidationError):
        _lambda = Service(
            service=ServiceType.Lambda,
            integration_type="aws-sdk",
            integration_pattern="runTask",
        )
