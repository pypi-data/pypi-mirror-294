from nutrition_ai import constants, types
import requests


def extract_ingredients(text: str, header: dict = {}) -> list[types.IngredientInfo]:
    """
    Extract ingredients from a given text.

    This function sends a POST request to the EXTRACT_INGREDIENTS_URL endpoint
    to parse and extract ingredient information from the provided text.

    Args:
        text (str): The text containing ingredient information to be extracted.
        header (dict, optional): Additional headers for the HTTP request. Defaults to an empty dictionary.

    Returns:
        list[types.IngredientInfo]: A list of IngredientInfo objects, each representing
        an extracted ingredient with its associated information.

    Raises:
        requests.RequestException: If there's an error with the HTTP request.
        ValueError: If the response cannot be parsed as JSON.
        pydantic.ValidationError: If the response data doesn't match the IngredientInfo model.

    Note:
        This function relies on an external API endpoint defined in constants.EXTRACT_INGREDIENTS_URL.
        Ensure that the API is accessible and the correct URL is set before using this function.
    """
    url = constants.EXTRACT_INGREDIENTS_URL
    payload = {
        "content": text,
    }
    response = requests.post(url, json=payload, headers=header)
    r = [types.IngredientInfo.model_validate(j) for j in response.json()]
    return r
