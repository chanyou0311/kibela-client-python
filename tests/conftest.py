import json
import re
from typing import Dict

from gql.transport.requests import RequestsHTTPTransport
from vcr.request import Request
import pytest

from kibela_client import KibelaClient
from kibela_client.settings import Settings


kibela_team_pattern = re.compile(r"(https?://)\w+(\.kibe.la/api/v1)")


def filter_url(url: str) -> str:
    return kibela_team_pattern.sub(r"\1my\2", url)


def filter_request(request: Request):
    request.uri = filter_url(request.uri)
    return request


def filter_response(response: Dict):
    if "body" in response and "string" in response["body"]:
        try:
            content = json.loads(response["body"]["string"])
        except json.JSONDecodeError:
            pass
        else:
            response["body"]["string"] = json.dumps(content, separators=(",", ":")).encode()
    return response


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [('authorization', 'Bearer XXXXXX')],
        "decode_compressed_response": True,
        "before_record_request": filter_request,
        "before_record_response": filter_response,
    }


@pytest.fixture(scope="module")
def settings():
    return Settings()


@pytest.fixture(scope="module")
def client(settings: Settings):
    client = KibelaClient(team=settings.kibela_team, access_token=settings.kibela_access_token)

    # vcrpy has a bug using AIOHTTPTransport. so replace RequestsHTTPTransport for testing.
    # ref: https://github.com/kevin1024/vcrpy/issues/507
    client.client.transport = RequestsHTTPTransport(
        url=client.url, headers=client.headers, verify=True, retries=3,
    )
    return client
