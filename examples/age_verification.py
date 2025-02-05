from jisoo.models.state import Choice, Succeed, Fail, Graph, ChoiceRule, Chain, Pass
from jisoo.models.rule import Condition
import json

# Define success and failure states
success_state = Succeed(id="Success")
failure_state = Fail(id="Fail")

# Define conditions for age verification
is_adult = Condition.NumericGreaterThanEquals(variable="$.age", value=18)
has_guardian = Condition.BooleanEquals(variable="$.has_guardian", value=True)

# Create two paths through the state machine:
# 1. Adult path: age >= 18 -> process adult -> success
# 2. Minor with guardian path: has guardian -> process minor -> success

# Path for adults
adult_path = ChoiceRule(
    rule=is_adult,
    next=Chain(
        steps=[Pass(id="ProcessAdult", comment="Processing as adult"), success_state]
    ),
)

# Path for minors with guardian
minor_path = ChoiceRule(
    rule=has_guardian,
    next=Chain(
        steps=[
            Pass(id="ProcessMinor", comment="Processing as minor with guardian"),
            success_state,
        ]
    ),
)

# Create the choice state that will direct the flow
age_check = Choice(id="AgeVerification", choices=[adult_path, minor_path])

# Define the main flow: start -> age verification -> (success or failure)
main_flow = Chain(
    steps=[
        Pass(id="Start", comment="Starting age verification"),
        age_check,
        failure_state,  # Default path if no choices match
    ]
)

# Create and print the state machine
graph = Graph(branch=main_flow)

with open("./examples/statemachine/age_verification.json", "w+") as f:
    f.write(graph.definition)
