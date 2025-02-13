from jisoo.steps import SQSGetQueueAttributesStep, SQSDeleteMessageStep
from jisoo.models.common import ServiceType
from jisoo.models.input import RootInput

import pytest
from pydantic import ValidationError


def test_get_queue_attr_step():
    get_attributes_step = SQSGetQueueAttributesStep(
        id="example",
        queue_url="example-queue-url",
        attribute_names=["All"],
        result_path="$.result",
        integration_pattern="waitForTaskToken",
        integration_type="optimized",
    )
    step_dict = get_attributes_step.to_dict()
    assert step_dict["Type"] == "Task"
    assert (
        step_dict["Resource"]
        == "arn:aws:states:::sqs:getQueueAttributes.waitForTaskToken"
    )
    assert step_dict["Parameters"]["QueueUrl"] == "example-queue-url"
    assert step_dict["Parameters"]["AttributeNames"] == ["All"]
    assert step_dict["ResultPath"] == "$.result"


def test_delete_messages_step():
    delete_message_step = SQSDeleteMessageStep(
        id="example",
        queue_url="example-queue-url",
        receipt_handle="example-receipt-handle",
        result_path="$.result",
        integration_pattern="waitForTaskToken",
        integration_type="optimized",
    )
    step_dict = delete_message_step.to_dict()
    assert step_dict["Type"] == "Task"
    assert (
        step_dict["Resource"] == "arn:aws:states:::sqs:deleteMessage.waitForTaskToken"
    )
    assert step_dict["Parameters"]["QueueUrl"] == "example-queue-url"
    assert step_dict["Parameters"]["ReceiptHandle"] == "example-receipt-handle"
    assert step_dict["ResultPath"] == "$.result"
