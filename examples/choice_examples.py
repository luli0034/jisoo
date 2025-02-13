from jisoo.steps import SFNListExecutionsStep
from jisoo.models.rule import Condition
from jisoo.models.state import Choice, ChoiceRule, Succeed, State, Graph, Chain
from typing import List


def check_execution_steps() -> List[State]:

    list_executions = SFNListExecutionsStep(
        id="ListExecutions",
        integration_type="aws-sdk",
        state_machine_arn="example-arn",
        status_filter="RUNNING",
        result_selector={"RunningExecutions.$": "States.ArrayLength($.Executions)"},
        result_path="$.result",
    )
    has_running_execution_cond = Condition.And(
        [
            Condition.BooleanEquals("$.StartFromStepFunction", False),
            Condition.NumericGreaterThan("$.result.RunningExecutions", 1),
        ]
    )
    has_running_execution = Choice(
        id="HasRunningExecution",
        choices=[
            ChoiceRule(
                rule=has_running_execution_cond, next=Succeed(id="SkipExecution")
            )
        ],
    )

    return [list_executions, has_running_execution]


# Combine the parallel independent processing and the dependent chain into a single graph
final_graph = Graph(
    branch=Chain(steps=check_execution_steps()),
    comment="Combined Data Processing Pipeline",
    timeout_seconds=60,
)

with open("./examples/statemachine/choice_examples.json", "w+") as f:
    f.write(final_graph.definition)
