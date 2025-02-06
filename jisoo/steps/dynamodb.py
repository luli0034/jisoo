from jisoo.steps.base import Service
from jisoo.models.common import ServiceType
from jisoo.models.state import Task
from enum import Enum
from pydantic import model_validator


class DynamoDBActions(Enum):
    GetItem = "getItem"
    PutItem = "putItem"


test = Service(
    id="DynamoDBGetItem",
    service=ServiceType.DynamoDB,
    integration_type="aws-sdk",
    action=DynamoDBActions.GetItem,
)
print(test.to_dict())
