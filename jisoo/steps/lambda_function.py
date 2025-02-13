from jisoo.steps.base import Service
from jisoo.models.state import Retry
from jisoo.models.common import ServiceType, ErrorEqualsEnum
from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field


class LambdaAction(Enum):
    Invoke = "invoke"


class LambdaInvokeStep(Service):
    service: ServiceType = Field(ServiceType.Lambda, frozen=True)
    action: LambdaAction = Field(LambdaAction.Invoke, frozen=True)
    function_name: str
    payload: Optional[dict] = None
    qualifier: Optional[str] = None
    log_type: Optional[Literal["Tail", "None"]] = None
    client_context: Optional[str] = None
    invocation_type: Optional[Literal["RequestResponse", "Event", "DryRun"]] = None


# Default Retry for Lambda
LambdaDefaultRetry = Retry(
    error_equals=[
        ErrorEqualsEnum.Lambda.ServiceException,
        ErrorEqualsEnum.Lambda.ClientExecutionTimeoutException,
        ErrorEqualsEnum.Lambda.AWSLambdaException,
        ErrorEqualsEnum.Lambda.TooManyRequestsException,
    ],
    interval_seconds=1,
    max_attempts=1,
    backoff_rate=2,
)
