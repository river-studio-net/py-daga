# Daga - Saga DAGs Made Easy
A simple, standard library-based tool to create and run Saga pattern mission DAGs. 
Need an atomic way to create real world objects? This is the way. 
No more try-excepts and nested logic - focus on your bussiness.
## Usage
### Basic Usage Without Rollbacks
```python
import networkx as nx
from py_daga import DagaFlow


async def root(predecessors_results: list[int]):
    return sum(predecessors_results) + 1
async def layer1_f1(predecessors_results: list[int]): 
    return sum(predecessors_results) + 2
async def layer1_f2(predecessors_results: list[int]): 
    return sum(predecessors_results) + 3
async def layer2_f1(predecessors_results: list[int]): 
    return sum(predecessors_results) + 4
async def layer2_f2(predecessors_results: list[int]): 
    return sum(predecessors_results) + 5

dag = nx.DiGraph()
dag.add_edges_from([
    (root, layer1_f1),
    (root, layer1_f2),
    (layer1_f1, layer2_f1),
    (layer1_f1, layer2_f2),
    (layer1_f2, layer2_f2),
])
flow = DagaFlow(dag)
results = flow.run(input=0)  # = [7, 12]
```
### Basic Usage With Rollbacks
To use rollback functionality, we need to wrap our functions as `DagaAction`s:
```python
import networkx as nx

from py_daga import DagaAction, DagaFlow


@DagaAction[set[str], set[str]]
async def root(predecessors_results: list[set[str]]):
    ...

@root.register_function_as_rollback
@DagaAction[set[str], set[str]]
async def root_rollback(predecessors_results: list[set[str]]):
    ...

@DagaAction[set[str], set[str]]
async def layer1_f1(predecessors_results: list[set[str]]): 
    ...

@layer1_f1.register_function_as_rollback
@DagaAction[set[str], set[str]]
async def layer1_f1_rollback(predecessors_results: list[set[str]]): 
    ...

flow = DagaFlow(
    nx.DiGraph().add_edges_from([(root, layer1_f1)])
)
results = flow.run()
```

## Contributing

### Documentation

The project includes comprehensive auto-generated documentation that is updated automatically on every push to the main branch.

#### Auto-Generation

The documentation in the `docs/` folder is automatically generated using [pdoc](https://pdoc.dev/) whenever changes are pushed to the main branch. The GitHub Action workflow (`.github/workflows/docs.yml`) handles this process.

#### Viewing Documentation

Open `docs/index.html` in your web browser to view the generated documentation.

#### Documentation Structure

- `index.html` - Main documentation page with module overview
- `action.html` - Documentation for the DagaAction classes
- `flow.html` - Documentation for the DagaFlow orchestrator
- `meta.html` - Documentation for the DagaMeta metaclass
- `utils.html` - Documentation for utility functions and classes

### Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `uv run pytest`
6. Submit a pull request

## Rejected Ideas
### Implmenting DagaAction as a context manager
Trying to use said context manager proved to be confusing beyond any standard, and so it has been decided to drop the implementation.
Another concern against the idea was that it added significant complexity to the codebase, adding a lot of functionality that was not used otherwise. 
### Implementing rollbacks with Python `results` module
I didn't want to add extra dependency and added complexity on top of everything.