from gandula.providers.pff.api.api_client import execute_query
from gandula.providers.pff.api.api_client import get_client

from .queries import queries


def account_active(
    pff_api_url: str | None = None, pff_api_key: str | None = None
) -> dict:
    query = queries['account_active']
    client = get_client(pff_api_url, pff_api_key)
    return execute_query(query, client=client)
