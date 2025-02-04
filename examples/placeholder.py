from jisoo.models.input import JSONPath, ExecutionInput

exi = ExecutionInput(schema={"key_1": str, "key_2": str})
print(exi.key_2)
step_input = JSONPath(schema={"key_1": str, "key_2": str})
print(step_input.key_2)
