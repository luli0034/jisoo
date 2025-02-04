from jisoo.models.input.base import ExecutionInput, StepInput

schema = {"foo": ["3", "2"], "bar": int}
exi = ExecutionInput(schema=schema)
print(exi.foo[0], exi.bar)

si = StepInput(schema=schema)
print(si.foo[0], si.bar)
