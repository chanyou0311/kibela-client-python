from typing import Dict
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from .types import Budget

class KibelaClient:
    def __init__(self, team: str, access_token: str) -> None:
        self.url = f"https://{team}.kibe.la/api/v1"
        self.headers = {"Authorization": f"Bearer {access_token}"}
        transport = AIOHTTPTransport(url=self.url, headers=self.headers)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def request(self, request_string: str) -> Dict:
        document = gql(request_string)
        return self.client.execute(document)

    def get_budget(self) -> Budget:
        query = """
        {
            budget {
                consumed
                cost
                remaining
            }
        }
        """
        response = self.request(query)
        return Budget.parse_obj(response["budget"])
