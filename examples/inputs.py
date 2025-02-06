from jisoo.models.input.base import StepInput
from jisoo.models.input.terraform import TFVariables
from jisoo.models.common import KeyValuePair

tfvars = TFVariables()
tfvars.add_variable("foo")
schema = {tfvars.get("foo"): ["3", "2"], "bar": int}
i = StepInput(schema=schema)
# print(i.get(tfvars.get("foo")))

a = KeyValuePair(name="foo", value="bar")
b = KeyValuePair(name="foo", value=i.get(tfvars.get("foo")))
print(b.to_dict())
