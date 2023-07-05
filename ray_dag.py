from ray import serve
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode
from starlette.requests import Request

# Unpack http request
@serve.deployment
async def unpack_request(http_request: Request) -> float:
    return await http_request.json()

# Node 1 of the DAG
@serve.deployment
async def func1(number: float) -> float:
    return number * 10

# Node 2 of the DAG
@serve.deployment
async def func2(number: float) -> float:
    return number + 2

# Bind functions
func1_node = func1.bind()
func2_node = func2.bind()

with InputNode() as http_request:
    request_number = unpack_request.bind(http_request)
    func1_output = func1.bind(request_number)
    func2_output = func2.bind(func1_output)

graph = DAGDriver.options(route_prefix="/inference").bind(func2_output)
