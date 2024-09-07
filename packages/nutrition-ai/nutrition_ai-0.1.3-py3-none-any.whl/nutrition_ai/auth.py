import requests
import os
from nutrition_ai import constants
import time
import aiohttp


def get_header_and_expiry_time() -> tuple[dict[str, str], float]:
    """
    Retrieves the authorization header and expiry time for the Passio API.

    This function fetches the API key from the environment variables, constructs the
    authentication URL, and makes a POST request to obtain the access token. The token
    is then used to create the authorization header, and the expiry time is calculated
    based on the token's expiration duration.

    Returns:
        tuple: A tuple containing the authorization header (dict) and the expiry time (float).
    """
    api_key = os.getenv("PASSIO_API_KEY")
    auth_url = f"{constants.TOKEN_BASE_URL}oauth/token/{api_key}"
    token = requests.post(auth_url).json()
    header = {
        "Authorization": f"Bearer {token['access_token']}",
        "Passio-ID": token["customer_id"],
    }
    expiry_time = time.time() + token["expires_in"]
    return header, expiry_time


async def get_header_and_expiry_time_async() -> tuple[dict[str, str], float]:
    """
    Asynchronously retrieves the authorization header and expiry time for the Passio API.

    This function fetches the API key from the environment variables, constructs the
    authentication URL, and makes an asynchronous POST request to obtain the access token.
    The token is then used to create the authorization header, and the expiry time is
    calculated based on the token's expiration duration.

    Returns:
        tuple: A tuple containing the authorization header (dict) and the expiry time (float).

    Raises:
        aiohttp.ClientError: If there's an error with the HTTP request.
        ValueError: If the response cannot be parsed as JSON.
    """
    api_key = os.getenv("PASSIO_API_KEY")
    auth_url = f"{constants.TOKEN_BASE_URL}oauth/token/{api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.post(auth_url) as response:
            response.raise_for_status()
            token = await response.json()

    header = {
        "Authorization": f"Bearer {token['access_token']}",
        "Passio-ID": token["customer_id"],
    }
    expiry_time = time.time() + token["expires_in"]
    return header, expiry_time
