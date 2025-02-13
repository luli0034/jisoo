from jisoo.models.state import Pass, Chain, Succeed, Graph, Map, Fail, Catch
from jisoo.models.common import ErrorEqualsEnum
from jisoo.steps import DynamoDBGetItemStep


def create_order_processing_workflow():
    """
    Creates a state machine for processing a list of orders in an e-commerce application.
    Each order is processed in parallel, and the results are aggregated.
    """

    # Define the success and failure states
    success_state = Succeed(id="AllOrdersProcessed")

    # Define a Pass state to simulate order processing
    def create_order_processing_task():
        return DynamoDBGetItemStep(
            id="ProcessOrder", table_name="Orders", key={"foo": {"S": "bar"}}
        )

    def create_error_handler():
        return Catch(
            error_equals=[
                ErrorEqualsEnum.Events.TaskFailed,
                ErrorEqualsEnum.Events.Runtime,
            ],
            next_steps=Chain(
                steps=[
                    Pass(
                        id="ErrorHandler",
                        parameters={"error": "Order processing failed"},
                        result_path="$.error_details",
                    ),
                    Fail(id="ProcessOrderFailed"),
                ]
            ),
        )

    # Create a Map state to process each order in parallel
    order_processing_map = Map(
        id="ProcessOrders",
        item_processor=Chain(steps=[create_order_processing_task()]),
        input_path="$.orders",
        result_path="$.processed_orders",
        catch=create_error_handler(),
    )

    # Define the main workflow
    main_flow = Chain(
        steps=[
            order_processing_map,
            success_state,
        ]
    )

    # Create the state machine
    graph = Graph(branch=main_flow, comment="Order Processing Workflow")

    return graph


# Create and print the state machine definition
graph = create_order_processing_workflow()
with open("./examples/statemachine/order_processing.json", "w+") as f:
    f.write(graph.definition)

"""
Example Input:
{
    "orders": [
        {"order_id": 1, "item": "Laptop", "quantity": 1},
        {"order_id": 2, "item": "Smartphone", "quantity": 2},
        {"order_id": 3, "item": "Tablet", "quantity": 1},
        {"order_id": 4, "item": "Headphones", "quantity": 3},
        {"order_id": 5, "item": "Smartwatch", "quantity": 1}
    ]
}
"""
