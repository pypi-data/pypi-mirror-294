from gql.transport.exceptions import TransportServerError

from gandula.providers.pff.api import auth


def validate_api_key(api_key: str | None = None) -> bool:
    """
    Validates the provided PFF API key.

    :param api_key: The API key to validate.
    :return: True if the API key is valid, False otherwise.
    """
    try:
        response = auth.account_active(pff_api_key=api_key)
        return response['accountActive']
    except TransportServerError:
        return False
