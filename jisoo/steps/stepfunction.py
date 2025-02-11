from jisoo.steps.base import Service
from jisoo.models.common import ServiceType
from enum import Enum
from pydantic import Field, Json
from typing import Optional, Dict, List, Literal

# Follow the Amazon DynamoDB API Reference
# https://docs.aws.amazon.com/step-functions/latest/apireference/API_Operations.html


class SFNAction(Enum):
    CreateStateMachine = "createStateMachine"
    DeleteStateMachine = "deleteStateMachine"
    DescribeStateMachine = "describeStateMachine"
    ListStateMachines = "listStateMachines"
    StartExecution = "startExecution"
    StopExecution = "stopExecution"
    DescribeExecution = "describeExecution"
    ListExecutions = "listExecutions"


class SFNCreateStateMachineStep(Service):
    service: ServiceType = Field(ServiceType.StepFunctions, frozen=True)
    action: SFNAction = Field(SFNAction.CreateStateMachine, frozen=True)
    name: str
    role_arn: str
    definition: str
    type: Optional[str] = None
    logging_configuration: Optional[Dict] = None
    tags: Optional[List[Dict[str, str]]] = None


class SFNDeleteStateMachineStep(Service):
    service: ServiceType = Field(ServiceType.StepFunctions, frozen=True)
    action: SFNAction = Field(SFNAction.DeleteStateMachine, frozen=True)
    state_machine_arn: str


class SFNDescribeStateMachineStep(Service):
    service: ServiceType = Field(ServiceType.StepFunctions, frozen=True)
    action: SFNAction = Field(SFNAction.DescribeStateMachine, frozen=True)
    state_machine_arn: str


class SFNListStateMachinesStep(Service):
    service: ServiceType = Field(ServiceType.StepFunctions, frozen=True)
    action: SFNAction = Field(SFNAction.ListStateMachines, frozen=True)
    max_results: Optional[int] = None
    next_token: Optional[str] = None


class SFNStartExecutionStep(Service):
    service: ServiceType = Field(ServiceType.StepFunctions, frozen=True)
    action: SFNAction = Field(SFNAction.StartExecution, frozen=True)
    state_machine_arn: str
    name: Optional[str] = None
    input: Optional[Dict] = None
    trace_header: Optional[str] = None


class SFNStopExecutionStep(Service):
    service: ServiceType = Field(ServiceType.StepFunctions, frozen=True)
    action: SFNAction = Field(SFNAction.StopExecution, frozen=True)
    execution_arn: str
    error: Optional[str] = None
    cause: Optional[str] = None


class SFNDescribeExecutionStep(Service):
    service: ServiceType = Field(ServiceType.StepFunctions, frozen=True)
    action: SFNAction = Field(SFNAction.DescribeExecution, frozen=True)
    execution_arn: str


class SFNListExecutionsStep(Service):
    service: ServiceType = Field(ServiceType.StepFunctions, frozen=True)
    action: SFNAction = Field(SFNAction.ListExecutions, frozen=True)
    state_machine_arn: str
    status_filter: Optional[
        Literal[
            "RUNNING", "SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED", "PENDING_REDRIVE"
        ]
    ] = None
    redrive_filter: Optional[Literal["REDRIVEN", "NOT_REDRIVEN"]] = None
    max_results: Optional[int] = None
    next_token: Optional[str] = None
