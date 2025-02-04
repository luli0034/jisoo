from jisoo.models.state import Catch, Retry, Graph, Task, Fail, Pass, Chain, Succeed
from jisoo.models.common import ErrorEqualsEnum

retry = Retry(error_equals=[ErrorEqualsEnum.TaskFailed])
catch = Catch(
    error_equals=[ErrorEqualsEnum.TaskFailed], next_steps=Fail(id="FailState")
)

task_state = Task(
    id="TaskState",
    input_path="$.input",
    output_path="$.output",
    resource="arn:aws:states:::lambda:invoke",
    parameters={"FunctionName": "my-function"},
    result_path="$.result",
    retry=retry,
    catch=catch,
)

graph = Graph(branch=task_state, comment="Task State Graph", timeout_seconds=60)
# print(graph.definition)

retry2 = Retry(error_equals=[ErrorEqualsEnum.TaskFailed])
catch2 = Catch(
    error_equals=[ErrorEqualsEnum.TaskFailed],
    next_steps=Chain(steps=[Pass(id="Pass"), Succeed(id="Success")]),
)
task_state = Task(
    id="TaskState",
    input_path="$.input",
    output_path="$.output",
    resource="arn:aws:states:::lambda:invoke",
    parameters={"FunctionName": "my-function"},
    result_path="$.result",
    retry=[retry, retry2],
    catch=[catch, catch2],
)

graph = Graph(branch=task_state, comment="Task State Graph", timeout_seconds=60)
print(graph.definition)

# {
#     "States": {
#         "FailState": {
#             "Type": "Fail"
#         },
#         "Pass": {
#             "Type": "Pass",
#             "Next": "Success"
#         },
#         "Success": {
#             "Type": "Succeed"
#         },
#         "TaskState": {
#             "Retry": [
#                 {
#                     "ErrorEquals": [
#                         "States.TaskFailed"
#                     ]
#                 },
#                 {
#                     "ErrorEquals": [
#                         "States.TaskFailed"
#                     ]
#                 }
#             ],
#             "Catch": [
#                 {
#                     "ErrorEquals": [
#                         "States.TaskFailed"
#                     ],
#                     "Next": "FailState"
#                 },
#                 {
#                     "ErrorEquals": [
#                         "States.TaskFailed"
#                     ],
#                     "Next": "Pass"
#                 }
#             ],
#             "Type": "Task",
#             "InputPath": "$.input",
#             "OutputPath": "$.output",
#             "ResultPath": "$.result",
#             "Parameters": {
#                 "FunctionName": "my-function"
#             },
#             "Resource": "arn:aws:states:::lambda:invoke",
#             "End": true
#         }
#     },
#     "StartAt": "TaskState",
#     "Comment": "Task State Graph",
#     "TimeoutSeconds": 60
# }
