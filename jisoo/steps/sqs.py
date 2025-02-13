from jisoo.steps.base import Service
from jisoo.models.common import ServiceType, ErrorEqualsEnum
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# Follow the SQS API Reference
# https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_Operations.html


class SQSAction(str, Enum):
    SendMessage = "sendMessage"
    ReceiveMessage = "receiveMessage"
    DeleteMessage = "deleteMessage"
    PurgeQueue = "purgeQueue"
    GetQueueAttributes = "getQueueAttributes"
    SetQueueAttributes = "setQueueAttributes"
    ListQueues = "listQueues"
    CreateQueue = "createQueue"
    DeleteQueue = "deleteQueue"


class SQSSendMessageStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.SendMessage, frozen=True)
    queue_url: str
    message_body: str
    delay_seconds: Optional[int] = None
    message_attributes: Optional[Dict[str, Dict[str, str]]] = None


class SQSReceiveMessageStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.ReceiveMessage, frozen=True)
    queue_url: str
    max_number_of_messages: Optional[int] = None
    visibility_timeout: Optional[int] = None
    wait_time_seconds: Optional[int] = None
    message_attribute_names: Optional[List[str]] = None


class SQSDeleteMessageStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.DeleteMessage, frozen=True)
    queue_url: str
    receipt_handle: str


class SQSPurgeQueueStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.PurgeQueue, frozen=True)
    queue_url: str


class SQSGetQueueAttributesStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.GetQueueAttributes, frozen=True)
    queue_url: str
    attribute_names: Optional[List[str]] = None


class SQSSetQueueAttributesStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.SetQueueAttributes, frozen=True)
    queue_url: str
    attributes: Dict[str, str]


class SQSListQueuesStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.ListQueues, frozen=True)
    queue_name_prefix: Optional[str] = None
    next_token: Optional[str] = None
    max_results: Optional[int] = None


class SQSCreateQueueStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.CreateQueue, frozen=True)
    queue_name: str
    attributes: Optional[Dict[str, str]] = None
    tags: Optional[Dict[str, str]] = None


class SQSDeleteQueueStep(Service):
    service: ServiceType = Field(ServiceType.SQS, frozen=True)
    action: SQSAction = Field(SQSAction.DeleteQueue, frozen=True)
    queue_url: str
