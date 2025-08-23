import pytest

from src.flow import DagaFlow
from test.flow.values_for_test import get_valid_dag, get_cyclic_dag, get_valid_dag_with_rollbacks, get_cyclic_dag_with_rollbacks


class TestFlow:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("initial_value, expected_results", [
        (0, [7, 12]),
        (1, [8, 14]),
        (2, [9, 16]),
    ])
    async def test_valid_dag(self, initial_value: int, expected_results: list[int]):
        flow = DagaFlow(get_valid_dag())
        results = await flow.run(initial_value)
        assert results == expected_results

    @pytest.mark.asyncio
    async def test_cyclic_dag(self):
        with pytest.raises(AssertionError):
            DagaFlow(get_cyclic_dag())

    @pytest.mark.asyncio
    @pytest.mark.parametrize("initial_value, expected_results, should_fail", [
        (set(["input"]), [
            {'layer2_f1', 'input', 'layer1_f1', 'root'}, 
            {'layer2_f2', 'root', 'layer1_f2', 'input', 'layer1_f1'}
        ], False),
        (set(["input"]), [
            {'layer2_f1', 'input', 'layer1_f1', 'root'}, 
            {'layer2_f2', 'root', 'layer1_f2', 'input', 'layer1_f1'}
        ], True),
    ])
    async def test_valid_dag_with_rollbacks(self, initial_value: set[str], expected_results: list[set[str]], should_fail: bool):
        flow = DagaFlow(get_valid_dag_with_rollbacks(fail=should_fail))
        try:
            results = await flow.run(initial_value)
            assert results == expected_results
        except Exception as e:
            assert should_fail
            assert isinstance(e, ExceptionGroup)
            assert len(e.exceptions) == 1
            assert str(e.exceptions[0]) == "Failing purposefully"
        else:
            assert not should_fail

    @pytest.mark.asyncio
    async def test_cyclic_dag_with_rollbacks(self):
        with pytest.raises(AssertionError):
            DagaFlow(get_cyclic_dag_with_rollbacks())
