from jisoo.steps import Service, EventBridgePutEventsStep
from jisoo.models.common import ServiceType
from jisoo.models.input import RootInput
from jisoo.models.common.eventbridge import PutEventsRequestEntry
import pytest
from pydantic import ValidationError
import json


def test_putevents_step():
    put_event_stpe = EventBridgePutEventsStep(
        id="example",
        entries=[
            PutEventsRequestEntry(
                source="example",
                detail_type="example",
                detail=json.dumps({"key": "value"}),
                event_bus_name="example-bus",
            )
        ],
        result_path="$.result",
        integration_pattern="waitForTaskToken",
        integration_type="aws-sdk",
    )
    step_dict = put_event_stpe.to_dict()
    assert step_dict["Type"] == "Task"
    assert (
        step_dict["Resource"]
        == "arn:aws:states:::aws-sdk:events:putEvents.waitForTaskToken"
    )
    assert step_dict["Parameters"]["Entries"] == [
        {
            "Source": "example",
            "DetailType": "example",
            "Detail": {"key": "value"},
            "EventBusName": "example-bus",
        }
    ]
    assert step_dict["ResultPath"] == "$.result"


test_putevents_step()
