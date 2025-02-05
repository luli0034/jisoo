from jisoo.models.state import Parallel, Pass, Chain, Succeed, Graph

# Define independent data processing tasks
clean_data = Pass(id="Clean_Data")
save_data = Pass(id="Save_Data")
process_invalid = Pass(id="Process_Invalid_Data")
validate_data = Pass(id="Validate_Data")

# Create chains for independent data processing tasks
chain_clean = Chain(steps=[clean_data, save_data])
chain_validate = Chain(steps=[validate_data, process_invalid])

# Combine independent chains into a parallel state for data processing
parallel_independent_processing = Parallel(
    id="ParallelIndependentProcessing",
    branches=[chain_clean, chain_validate],
)

# Define dependent tasks
load_data = Pass(id="Load_Data")
process_data = Succeed(id="Process_Data")  # This task depends on Load_Data

# Combine the parallel independent processing and the dependent chain into a single graph
final_graph = Graph(
    branch=Chain(steps=[parallel_independent_processing, load_data, process_data]),
    comment="Combined Data Processing Pipeline",
    timeout_seconds=60,
)

with open("./examples/statemachine/parallel_processing.json", "w+") as f:
    f.write(final_graph.definition)
