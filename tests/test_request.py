import pytest
from kibela_client import KibelaClient
from graphql.error import GraphQLSyntaxError


@pytest.mark.vcr()
def test_get_response(client: KibelaClient):
    query = """
    query {
        currentUser {
            account
            realName
        }
    }
    """
    response = client.request(query)
    assert response["currentUser"]["account"] == "chanyou"


@pytest.mark.vcr()
def test_raise_graphql_syntax_error_invalid_request_string(client: KibelaClient):
    invalid_query = """
    query {
        currentUser {
            account
            realName
    """
    with pytest.raises(GraphQLSyntaxError):
        client.request(invalid_query)
