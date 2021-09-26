import re
from typing import Dict

from vcr.request import Request
import pytest


kibela_team_pattern = re.compile(r"(https?://)\w+(\.kibe.la/api/v1)")

def filter_url(url: str) -> str:
    return kibela_team_pattern.sub(r"\1my\2", url)

def filter_request(request: Request):
    request.uri = filter_url(request.uri)
    return request

def filter_response(response: Dict):
    response["url"] = filter_url(response["url"])
    return response

@pytest.fixture(scope='module')
def vcr_config():
    return {
        "filter_headers": [('authorization', 'Bearer XXXXXX')],
        "before_record_request": filter_request,
        "before_record_response": filter_response,
    }
