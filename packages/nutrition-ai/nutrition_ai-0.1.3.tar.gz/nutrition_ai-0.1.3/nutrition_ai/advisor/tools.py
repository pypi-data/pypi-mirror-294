import enum
from PIL import Image
import io
import base64
import requests
import aiohttp
from nutrition_ai.advisor import types
from nutrition_ai.advisor import constants


class ToolType(str, enum.Enum):
    SEARCHINGREDIENTMATCHES = "SearchIngredientMatches"
    DETECTMEALLOGSREQUIRED = "DetectMealLogsRequired"


def search_ingredient_matches(
    thread_id: str, message_id: str, header: dict = {}
) -> types.AdvisorResponse:
    """
    Searches for ingredient matches using the AI advisor.

    Args:
        thread_id (str): The ID of the conversation thread.
        message_id (str): The ID of the message to search for ingredient matches.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the ingredient matches.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages/tools/target/{ToolType.SEARCHINGREDIENTMATCHES.value}"
    resp = requests.post(url, headers=header, json={"messageId": message_id})
    r = types.AdvisorResponse.model_validate(resp.json())
    return r


async def search_ingredient_matches_async(
    thread_id: str, message_id: str, header: dict = {}
) -> types.AdvisorResponse:
    """
    Asynchronously searches for ingredient matches using the AI advisor.

    Args:
        thread_id (str): The ID of the conversation thread.
        message_id (str): The ID of the message to search for ingredient matches.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the ingredient matches.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages/tools/target/{ToolType.SEARCHINGREDIENTMATCHES.value}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=header, json={"messageId": message_id}) as resp:
            resp.raise_for_status()
            json_data = await resp.json()
    r = types.AdvisorResponse.model_validate(json_data)
    return r


def detect_meal_logs_required(
    thread_id: str,
    message_id: str,
    tool_call_id: str,
    run_id: str,
    data: str,
    header: dict = {},
) -> types.AdvisorResponse:
    """
    Detects the required meal logs for a given conversation thread.

    Args:
        thread_id (str): The ID of the conversation thread.
        message_id (str): The ID of the message to detect meal logs for.
        tool_call_id (str): The ID of the tool call.
        run_id (str): The ID of the run.
        data (str): The data to be sent in the request.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the detected meal logs.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages/{message_id}/respond"
    resp = requests.post(
        url,
        headers=header,
        json={"data": data, "toolCallId": tool_call_id, "runId": run_id},
    )
    r = types.AdvisorResponse.model_validate(resp.json())
    return r


async def detect_meal_logs_required_async(
    thread_id: str,
    message_id: str,
    tool_call_id: str,
    run_id: str,
    data: str,
    header: dict = {},
) -> types.AdvisorResponse:
    """
    Asynchronously detects the required meal logs for a given conversation thread.

    Args:
        thread_id (str): The ID of the conversation thread.
        message_id (str): The ID of the message to detect meal logs for.
        tool_call_id (str): The ID of the tool call.
        run_id (str): The ID of the run.
        data (str): The data to be sent in the request.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the detected meal logs.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages/{message_id}/respond"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            headers=header,
            json={"data": data, "toolCallId": tool_call_id, "runId": run_id},
        ) as resp:
            resp.raise_for_status()
            json_data = await resp.json()
    r = types.AdvisorResponse.model_validate(json_data)
    return r


def list_tools(header: dict = {}) -> types.ToolInfoList:
    """
    Retrieves a list of available tools from the AI advisor.

    Args:
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.ToolInfoList: The response containing the list of available tools.
    """
    url = f"{constants.TOOLS_URL}"
    resp = requests.get(url, headers=header)
    r = types.ToolInfoList(tools=[types.ToolInfo(**item) for item in resp])
    return r


async def list_tools_async(header: dict = {}) -> types.ToolInfoList:
    """
    Asynchronously retrieves a list of available tools from the AI advisor.

    Args:
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.ToolInfoList: The response containing the list of available tools.
    """
    url = f"{constants.TOOLS_URL}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as resp:
            resp.raise_for_status()
            json_data = await resp.json()
    r = types.ToolInfoList(tools=[types.ToolInfo(**item) for item in json_data])
    return r

