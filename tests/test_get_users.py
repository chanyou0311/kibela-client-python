import pytest
from kibela_client import KibelaClient
from kibela_client.types import Role


@pytest.mark.vcr()
def test_get_users(client: KibelaClient):
    users = client.get_users()
    assert users[0].account == "chanyou"
    assert users[0].role == Role.OWNER
