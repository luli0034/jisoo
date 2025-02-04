from jisoo.models.state import Task, Graph, Pass, Chain

t = Task(
    id="Task_1", resource="arn:aws:states:::lambda:invoke", parameters={"key": "value"}
)
c = Chain(steps=[t, Pass(id="Pass_2"), Pass(id="Pass_3")])
g = Graph(branch=c)
print(g.to_dict())

# Output:
# {
#     "States": {
#         "Task_1": {
#             "Type": "Task",
#             "Parameters": {"key": "value"},
#             "Resource": "arn:aws:states:::lambda:invoke",
#             "Next": "Pass_2",
#         },
#         "Pass_2": {"Type": "Pass", "Next": "Pass_3"},
#         "Pass_3": {"End": True, "Type": "Pass"},
#     },
#     "StartAt": "Task_1",
# }
