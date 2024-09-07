import nutrition_ai.constants as constants
import nutrition_ai.types as types
import requests
import aiohttp


# Synchronous versions

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


# Asynchronous versions

async def product_by_upc_async(code: str, header: dict = {}) -> types.ProductCodeResponse:
    """
    Asynchronously fetches product information by UPC code.

    Args:
        code (str): The UPC code of the product.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.ProductCodeResponse: The response containing product information.

    Raises:
        aiohttp.ClientError: If there's an error with the HTTP request.
        ValueError: If the response cannot be parsed as JSON.
        pydantic.ValidationError: If the response data doesn't match the ProductCodeResponse model.
    """
    url = f"{constants.PRODUCTS_URL}productCode/{code}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as response:
            response.raise_for_status()
            json_data = await response.json()
    product = types.ProductCodeResponse.model_validate(json_data)
    return product


async def product_by_food_id_async(food_id: str, header: dict = {}) -> types.ProductCodeResponse:
    """
    Asynchronously fetches product information by food ID.

    Args:
        food_id (str): The food ID of the product.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.ProductCodeResponse: The response containing product information.

    Raises:
        aiohttp.ClientError: If there's an error with the HTTP request.
        ValueError: If the response cannot be parsed as JSON.
        pydantic.ValidationError: If the response data doesn't match the ProductCodeResponse model.
    """
    url = f"{constants.PRODUCTS_URL}{food_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as response:
            response.raise_for_status()
            json_data = await response.json()
    product = types.ProductCodeResponse.model_validate(json_data)
    return product


async def product_by_refCode_async(refCode: str, header: dict = {}) -> types.SearchResponse:
    """
    Asynchronously fetches product information by reference code.

    Args:
        refCode (str): The reference code of the product.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.SearchResponse: The response containing product information.

    Raises:
        aiohttp.ClientError: If there's an error with the HTTP request.
        ValueError: If the response cannot be parsed as JSON.
        pydantic.ValidationError: If the response data doesn't match the SearchResponse model.
    """
    url = f"{constants.PRODUCTS_URL}search/result/refCode/{refCode}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as response:
            response.raise_for_status()
            json_data = await response.json()
    product = types.SearchResponse.model_validate(json_data)
    return product

