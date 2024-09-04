from gandula.providers.pff.api import competitions


def get_competitions(*, api_url: str | None = None, api_key: str | None = None) -> dict:
    """
    Retrieves all competitions, in full (long).

    :param api_url: The API URL to connect to.
    :param api_key: The API key for authentication.
    :return: A dictionary containing all competitions.
    """
    return competitions.get_competitions(pff_api_url=api_url, pff_api_key=api_key)


def get_available_competitions(
    *, api_url: str | None = None, api_key: str | None = None
) -> dict:
    """
    Retrieves only the available competitions for these credentials.

    :param api_url: The API URL to connect to.
    :param api_key: The API key for authentication.
    :return: A dictionary containing available competitions.
    """
    return competitions.get_available_competitions(
        pff_api_url=api_url, pff_api_key=api_key
    )


def get_competition(
    competition_id: int, *, api_url: str | None = None, api_key: str | None = None
) -> dict:
    """
    Retrieves a specific competition by its ID.

    :param competition_id: The ID of the competition to retrieve.
    :param api_url: The API URL to connect to.
    :param api_key: The API key for authentication.
    :return: A dictionary containing the competition data.
    """
    return competitions.get_competition(
        competition_id, pff_api_url=api_url, pff_api_key=api_key
    )
