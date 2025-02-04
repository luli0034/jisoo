from jisoo.models.state import Choice, Succeed, Fail, Graph, ChoiceRule, Chain, Pass
from jisoo.models.rule import Condition


r1 = Condition.IsBoolean(variable="$.a", value=False)
r2 = Condition.StringEquals(variable="$.a", value="hi")
r = Condition.And(rules=[r1, r2])


success = Succeed(id="Success")
fail = Fail(id="Fail")
cr1 = ChoiceRule(rule=r, next=Chain(steps=[Pass(id="Pass_1"), success]))
cr2 = ChoiceRule(rule=r, next=Chain(steps=[Pass(id="Pass_1"), success]))
choice = Choice(id="IsSuccess", choices=[cr1, cr2])
ch = Chain(steps=[choice, Pass(id="Pass_2")])

graph = Graph(branch=Chain(steps=[Pass(id="Pass_2"), choice, fail]))
print(graph.to_json())

# {
#     "States": {
#         "Pass_2": {"Type": "Pass", "Next": "IsSuccess"},
#         "Pass_1": {"Type": "Pass", "Next": "Success"},
#         "Success": {"Type": "Succeed"},
#         "IsSuccess": {
#             "Type": "Choice",
#             "Choices": [
#                 {
#                     "And": [
#                         {"Variable": "$.a", "IsBoolean": false},
#                         {"Variable": "$.a", "StringEquals": "hi"},
#                     ],
#                     "Next": "Pass_1",
#                 },
#                 {
#                     "And": [
#                         {"Variable": "$.a", "IsBoolean": false},
#                         {"Variable": "$.a", "StringEquals": "hi"},
#                     ],
#                     "Next": "Pass_1",
#                 },
#             ],
#             "Default": "Fail",
#         },
#         "Fail": {"Type": "Fail"},
#     },
#     "StartAt": "Pass_2",
# }
