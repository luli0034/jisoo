from __future__ import annotations
from __future__ import absolute_import
from enum import Enum


class ErrorEqualsEnum(str, Enum):
    # reference: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html
    ALL = "States.ALL"
    DataLimitExceeded = "States.DataLimitExceeded"
    ExceedToleratedFailureThreshold = "States.ExceedToleratedFailureThreshold"
    HeartbeatTimeout = "States.HeartbeatTimeout"
    Http_Socket = "States.Http.Socket"
    IntrinsicFailure = "States.IntrinsicFailure"
    ItemReaderFailed = "States.ItemReaderFailed"
    NoChoiceMatched = "States.NoChoiceMatched"
    ParameterPathFailure = "States.ParameterPathFailure"
    Permissions = "States.Permissions"
    ResultPathMatchFailure = "States.ResultPathMatchFailure"
    ResultWriterFailed = "States.ResultWriterFailed"
    Runtime = "States.Runtime"
    TaskFailed = "States.TaskFailed"
    Timeout = "States.Timeout"
