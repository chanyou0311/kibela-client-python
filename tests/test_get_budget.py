import pytest
from kibela_client import KibelaClient


@pytest.mark.vcr()
def test_get_budget(client: KibelaClient):
    budget = client.get_budget()
    assert budget.consumed == 100
    assert budget.cost == 100
    assert budget.remaining == 299900
