import nutrition_ai.constants as constants
import nutrition_ai.types as types
import requests


def product_by_upc(code: str, header: dict = {}) -> types.ProductCodeResponse:
    """
    Fetches product information by UPC code.

    Args:
        code (str): The UPC code of the product.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.ProductCodeResponse: The response containing product information.
    """
    url = f"{constants.PRODUCTS_URL}productCode/{code}"
    response = requests.get(url, headers=header)
    product = types.ProductCodeResponse.model_validate(response.json())
    return product


def product_by_food_id(food_id: str, header: dict = {}) -> types.ProductCodeResponse:
    """
    Fetches product information by food ID.

    Args:
        food_id (str): The food ID of the product.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.ProductCodeResponse: The response containing product information.
    """
    url = f"{constants.PRODUCTS_URL}{food_id}"
    response = requests.get(url, headers=header)
    product = types.ProductCodeResponse.model_validate(response.json())
    return product


def product_by_refCode(refCode: str, header: dict = {}) -> types.SearchResponse:
    """
    Fetches product information by reference code.

    Args:
        refCode (str): The reference code of the product.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.SearchResponse: The response containing product information.
    """
    url = f"{constants.PRODUCTS_URL}search/result/refCode/{refCode}"
    response = requests.get(url, headers=header)
    product = types.SearchResponse.model_validate(response.json())
    return product
