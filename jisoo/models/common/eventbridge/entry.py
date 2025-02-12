from pydantic import BaseModel, Field, Json
from typing import List, Optional
from jisoo.models.common.base import CommonObject


class PutEventsRequestEntry(CommonObject):
    """
    Represents an event to be submitted to Amazon EventBridge.
    """

    detail: Optional[Json] = Field(
        None,
        description="A valid JSON object. There is no other schema imposed. The JSON object may contain fields and nested sub-objects.",
    )
    detail_type: Optional[str] = Field(
        None,
        max_length=128,
        description="Free-form string, used to decide what fields to expect in the event detail.",
    )
    event_bus_name: Optional[str] = Field(
        None, description="The name or ARN of the event bus to receive the event."
    )
    resources: Optional[List[str]] = Field(
        None,
        description="AWS resources, identified by Amazon Resource Name (ARN), which the event primarily concerns.",
    )
    source: Optional[str] = Field(None, description="The source of the event.")
    time: Optional[str] = Field(
        None, description="The time stamp of the event, per RFC3339."
    )
    trace_header: Optional[str] = Field(
        None,
        max_length=500,
        description="An AWS X-Ray trace header, which is an http header (X-Amzn-Trace-Id) that contains the trace-id associated with the event.",
    )
