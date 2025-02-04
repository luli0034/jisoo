from jisoo.models.state import Pass, Chain, Succeed, Graph, Map

a = Pass(
    id="id",
)

b = Pass(
    id="id_2",
)

map = Map(id="TestMap", item_processor=Chain(steps=[a, b]), input_path="$")
graph = Graph(branch=Chain(steps=[map, Pass(id="id_3"), Succeed(id="id_4")]))
print(graph.definition)
# Output:
# {
#     "States": {
#         "TestMap": {
#             "Type": "Map",
#             "InputPath": "$",
#             "ItemProcessor": {
#                 "States": {
#                     "id": {
#                         "Type": "Pass",
#                         "Next": "id_2"
#                     },
#                     "id_2": {
#                         "End": true,
#                         "Type": "Pass"
#                     }
#                 },
#                 "StartAt": "id",
#                 "ProcessorConfig": {
#                     "Mode": "INLINE"
#                 }
#             },
#             "Next": "id_3"
#         },
#         "id_3": {
#             "Type": "Pass",
#             "Next": "id_4"
#         },
#         "id_4": {
#             "Type": "Succeed"
#         }
#     },
#     "StartAt": "TestMap"
# }
