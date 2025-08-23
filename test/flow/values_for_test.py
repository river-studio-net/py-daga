import networkx as nx

from src.action import DagaAction


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


def get_valid_dag():
    valid_dag = nx.DiGraph()
    valid_dag.add_edges_from([
        (root, layer1_f1),
        (root, layer1_f2),
        (layer1_f1, layer2_f1),
        (layer1_f1, layer2_f2),
        (layer1_f2, layer2_f2),
    ])
    return valid_dag


def get_cyclic_dag():
    cyclic_dag = nx.DiGraph()
    cyclic_dag.add_edges_from([
        (root, layer1_f1),
        (layer1_f1, layer2_f1),
        (layer2_f1, layer1_f1),
    ])
    return cyclic_dag


def get_root(fail: bool = False, should_print: bool = False):
    @DagaAction[set[str], set[str]]
    async def root(predecessors_results: list[set[str]]):
        if should_print:
            print(predecessors_results)
        # Create a union of all predecessor results
        valid_predecessors = [p for p in predecessors_results if p is not None] if predecessors_results else []
        union_set = set().union(*valid_predecessors) if valid_predecessors else set()
        union_set.add("root")
        if fail:
            raise RuntimeError("Failing purposefully")
        return union_set 
    
    @root.register_function_as_rollback
    @DagaAction[set[str], set[str]]
    async def root_rollback(predecessors_results: list[set[str]]):
        # Filter out None values before unpacking
        valid_predecessors = [p for p in predecessors_results if p is not None] if predecessors_results else []
        union_set = set().union(*valid_predecessors) if valid_predecessors else set()
        if "root" in union_set:
            union_set.remove("root")
        union_set.add("root_rollback")
        return union_set

    return root


def get_layer1_f1(fail: bool = False, should_print: bool = False):
    @DagaAction[set[str], set[str]]
    async def layer1_f1(predecessors_results: list[set[str]]): 
        if should_print:
            print(predecessors_results)
        # Create a union of all predecessor results
        valid_predecessors = [p for p in predecessors_results if p is not None] if predecessors_results else []
        union_set = set().union(*valid_predecessors) if valid_predecessors else set()
        union_set.add("layer1_f1")
        if fail:
            raise RuntimeError("Failing purposefully")
        return union_set
    
    @layer1_f1.register_function_as_rollback
    @DagaAction[set[str], set[str]]
    async def layer1_f1_rollback(action_result: set[str]):
        # For rollback, we work with the action_result directly
        if action_result and "layer1_f1" in action_result:
            action_result.remove("layer1_f1")
            action_result.add("layer1_f1_rollback")
            return action_result
        return set(["layer1_f1_rollback"])
    
    return layer1_f1


def get_layer1_f2(fail: bool = False, should_print: bool = False):
    @DagaAction[set[str], set[str]]
    async def layer1_f2(predecessors_results: list[set[str]]): 
        if should_print:
            print(predecessors_results)
        # Create a union of all predecessor results
        valid_predecessors = [p for p in predecessors_results if p is not None] if predecessors_results else []
        union_set = set().union(*valid_predecessors) if valid_predecessors else set()
        union_set.add("layer1_f2")
        if fail:
            raise RuntimeError("Failing purposefully")
        return union_set
    
    @layer1_f2.register_function_as_rollback
    @DagaAction[set[str], set[str]]
    async def layer1_f2_rollback(action_result: set[str]):
        # For rollback, we work with the action_result directly
        if action_result and "layer1_f2" in action_result:
            action_result.remove("layer1_f2")
            action_result.add("layer1_f2_rollback")
            return action_result
        return set(["layer1_f2_rollback"])
    
    return layer1_f2


def get_layer2_f1(fail: bool = False, should_print: bool = False):
    @DagaAction[set[str], set[str]]
    async def layer2_f1(predecessors_results: list[set[str]]): 
        if should_print:
            print(predecessors_results)
        # Create a union of all predecessor results
        valid_predecessors = [p for p in predecessors_results if p is not None] if predecessors_results else []
        union_set = set().union(*valid_predecessors) if valid_predecessors else set()
        union_set.add("layer2_f1")
        if fail:
            raise RuntimeError("Failing purposefully")
        return union_set
    
    @layer2_f1.register_function_as_rollback
    @DagaAction[set[str], set[str]]
    async def layer2_f1_rollback(action_result: set[str]):
        # For rollback, we work with the action_result directly
        if action_result and "layer2_f1" in action_result:
            action_result.remove("layer2_f1")
            action_result.add("layer2_f1_rollback")
            return action_result
        return set(["layer2_f1_rollback"])
    
    return layer2_f1


def get_layer2_f2(fail: bool = False, should_print: bool = False):
    @DagaAction[set[str], set[str]]
    async def layer2_f2(predecessors_results: list[set[str]]): 
        if should_print:
            print(predecessors_results)
        # Create a union of all predecessor results
        valid_predecessors = [p for p in predecessors_results if p is not None] if predecessors_results else []
        union_set = set().union(*valid_predecessors) if valid_predecessors else set()
        union_set.add("layer2_f2")
        if fail:
            raise RuntimeError("Failing purposefully")
        return union_set 
    
    @layer2_f2.register_function_as_rollback
    @DagaAction[set[str], set[str]]
    async def layer2_f2_rollback(action_result: set[str]):
        # For rollback, we work with the action_result directly
        if action_result and "layer2_f2" in action_result:
            action_result.remove("layer2_f2")
            action_result.add("layer2_f2_rollback")
            return action_result
        return set(["layer2_f2_rollback"])
    
    return layer2_f2


def get_valid_dag_with_rollbacks(fail: bool = False, should_print: bool = False):
    valid_dag = nx.DiGraph()
    root = get_root(should_print=should_print)
    layer1_f1 = get_layer1_f1(should_print=should_print)
    layer1_f2 = get_layer1_f2(should_print=should_print)
    layer2_f1 = get_layer2_f1(should_print=should_print, fail=fail)
    layer2_f2 = get_layer2_f2(should_print=should_print)
    valid_dag.add_edges_from([
        (root, layer1_f1),
        (root, layer1_f2),
        (layer1_f1, layer2_f1),
        (layer1_f1, layer2_f2),
        (layer1_f2, layer2_f2),
    ])
    return valid_dag


def get_cyclic_dag_with_rollbacks(fail: bool = False, should_print: bool = False):
    cyclic_dag = nx.DiGraph()
    root = get_root(should_print=should_print)
    layer1_f1 = get_layer1_f1(should_print=should_print)
    layer2_f1 = get_layer2_f1(should_print=should_print, fail=fail)
    cyclic_dag.add_edges_from([
        (root, layer1_f1),
        (layer1_f1, layer2_f1),
        (layer2_f1, layer1_f1),
    ])
    return cyclic_dag
