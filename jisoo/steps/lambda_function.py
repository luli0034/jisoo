from jisoo.steps.base import Service, Step
from jisoo.models.common import ServiceType
from enum import Enum
from typing import Literal


class LambdaAction(Enum):
    Invoke = "invoke"


class LambdaInvokeStep(Step):

    def __init__(
        self,
        function_name: str, 
        # Parent Step class arguments (based on usage shown)
        id: str,
        integration_pattern: str,
        integration_type: str,
        input_path: str = None,
        output_path: str = None,
        result_path: str = None,
        result_selector: str = None,
        credentials: dict = None,
        timeout_seconds: int = None,
        timeout_seconds_path: str = None,
        heartbeat_seconds: int = None,
        heartbeat_seconds_path: str = None,
        
        # Lambda specific arguments
        payload: dict = None, 
        qualifier: str = None, 
        log_type: Literal["Tail", "None"] = None, 
        client_context: str = None, 
        invocation_type: Literal["RequestResponse", "Event", "DryRun"] = None,
    ):
        super().__init__(
            id=id,
            integration_type=integration_type,
            integration_pattern=integration_pattern,
            input_path=input_path,
            output_path=output_path,
            result_path=result_path,
            result_selector=result_selector,
            credentials=credentials,
            timeout_seconds=timeout_seconds,
            timeout_seconds_path=timeout_seconds_path,
            heartbeat_seconds=heartbeat_seconds,
            heartbeat_seconds_path=heartbeat_seconds_path
        )
        self.action = LambdaAction.Invoke
        self.service = ServiceType.Lambda.value
        self.function_name = function_name
        self.payload = payload
        self.qualifier = qualifier
        self.log_type = log_type
        self.client_context = client_context
        self.invocation_type = invocation_type

    def get_parameters(self) -> dict:
        parameters = {}
        if self.payload:
            parameters["Payload"] = self.payload
        if self.qualifier:
            parameters["Qualifier"] = self.qualifier
        if self.log_type:
            parameters["LogType"] = self.log_type
        if self.client_context:
            parameters["ClientContext"] = self.client_context
        if self.invocation_type:
            parameters["InvocationType"] = self.invocation_type
        return parameters
        