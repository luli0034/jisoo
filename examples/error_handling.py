from jisoo.models.state import Catch, Retry, Graph, Task, Fail, Pass, Chain, Succeed
from jisoo.models.common import ErrorEqualsEnum


def create_error_handling_workflow():
    """
    Creates a workflow that demonstrates error handling with:
    1. Multiple retry strategies for transient failures
    2. Catch patterns for different error scenarios
    """

    # Define retry strategies
    transient_retry = Retry(
        error_equals=[ErrorEqualsEnum.TaskFailed, ErrorEqualsEnum.Timeout],
        interval_seconds=1,
        max_attempts=3,
        backoff_rate=2.0,
    )

    final_retry = Retry(
        error_equals=[ErrorEqualsEnum.TaskFailed], interval_seconds=5, max_attempts=1
    )

    # Define error handlers
    system_error_handler = Catch(
        error_equals=[ErrorEqualsEnum.TaskFailed],
        next_steps=Chain(
            steps=[
                Pass(
                    id="SystemErrorHandler",
                    parameters={
                        "error": "System failure detected",
                        "action": "alerting",
                    },
                    result_path="$.error_details",
                ),
                Fail(id="SystemFailure"),
            ]
        ),
    )

    timeout_handler = Catch(
        error_equals=[ErrorEqualsEnum.Timeout],
        next_steps=Chain(
            steps=[
                Pass(
                    id="TimeoutHandler",
                    parameters={"error": "Operation timed out", "action": "logging"},
                    result_path="$.error_details",
                ),
                Succeed(id="GracefulTimeout"),
            ]
        ),
    )

    # Create main task with error handling
    main_task = Task(
        id="ProcessingTask",
        input_path="$.data",
        output_path="$.output",
        resource="arn:aws:states:::lambda:invoke",
        parameters={
            "FunctionName": "error-handling-demo",
            "Payload": {"data.$": "$.data", "context.$": "$$"},
        },
        result_path="$.result",
        retry=[transient_retry, final_retry],
        catch=[system_error_handler, timeout_handler],
    )

    # Create the state machine
    graph = Graph(
        branch=main_task, comment="Error Handling Demonstration", timeout_seconds=300
    )

    return graph


# Create and print the state machine definition
graph = create_error_handling_workflow()
with open("./examples/statemachine/error_handling.json", "w+") as f:
    f.write(graph.definition)


"""
Example input:
{
    "data": {
        "operation": "process",
        "payload": "sample-data"
    }
}

The state machine will:
1. Attempt the task with exponential backoff retries for transient failures
2. If retries are exhausted, handle specific errors differently:
   - System errors: Alert and fail
   - Timeouts: Log and succeed gracefully
"""
