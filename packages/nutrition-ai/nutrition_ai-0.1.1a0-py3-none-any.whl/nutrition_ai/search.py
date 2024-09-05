import nutrition_ai.constants as constants
import nutrition_ai.types as types
import requests


def food_matching(
    query_term: str, metadata=None, limit=10, header: dict = {}
) -> types.SearchResponse:
    """
    Searches for food items matching the given query term.

    Args:
        query_term (str): The term to search for.
        metadata (optional): Additional metadata to filter the search results.
        limit (int, optional): The maximum number of results to return. Defaults to 10.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.SearchResponse: The response containing the search results.
    """

    url = f"{constants.SEARCH_URL}advanced"
    query_params = {"term": query_term}
    if metadata:
        query_params["metadata"] = metadata
    if limit:
        query_params["limit"] = limit
    response = requests.get(url, headers=header, params=query_params)
    if response.status_code != 200:
        print(response.json())
    product = types.SearchResponse.model_validate(response.json())
    return product
