from ray import serve
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode
from starlette.requests import Request

# Unpack request
@serve.deployment
async def unpack_request(http_request: Request) -> float:
    return await http_request.json()

# Nodes in the graph
@serve.deployment
async def func1(number: float) -> float:
    return number + 5

@serve.deployment
async def func2(number: float) -> float:
    return number * 3

@serve.deployment
async def func3(number: float) -> float:
    return number - 4

func1_node = func1.bind()
func2_node = func2.bind()
func3_node = func3.bind()

with InputNode() as http_request:
    unpack_output = unpack_request.bind(http_request)
    func1_output = func1.bind(unpack_output)
    func2_output = func2.bind(func1_output)
    func3_output = func3.bind(func2_output)

graph = DAGDriver.options(route_prefix="/inference").bind(func3_output)
