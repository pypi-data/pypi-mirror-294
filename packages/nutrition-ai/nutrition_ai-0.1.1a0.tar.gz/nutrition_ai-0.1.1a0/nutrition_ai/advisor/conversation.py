import requests
import nutrition_ai.advisor.types as types
import nutrition_ai.advisor.constants as constants
import nutrition_ai.advisor.tools as tools


def start_thread(header: dict = {}) -> types.AdvisorResponse:
    """
    Starts a new conversation thread with the AI advisor.

    Args:
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the thread information.
    """
    url = constants.THREAD_URL
    response = requests.post(url, headers=header)
    advisor_response = types.AdvisorResponse.model_validate(response.json())
    return advisor_response


def send_message(
    thread_id: str,
    message: str,
    header: dict = {},
    input_sensors=[tools.ToolType.DETECTMEALLOGSREQUIRED.value],
) -> types.AdvisorResponse:
    """
    Sends a message to the AI advisor within a specific conversation thread.

    Args:
        thread_id (str): The ID of the conversation thread.
        message (str): The message to be sent to the AI advisor.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.
        input_sensors (list, optional): A list of input sensors to be used. Defaults to [tools.ToolType.DETECTMEALLOGSREQUIRED.value].

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the message information.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages"
    response = requests.post(
        url, headers=header, json={"message": message, "inputSensors": input_sensors}
    )
    advisor_response = types.AdvisorResponse.model_validate(response.json())
    return advisor_response
