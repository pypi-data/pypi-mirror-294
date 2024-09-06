from PIL import Image
import io
import base64
import requests
from nutrition_ai.advisor import types, constants
import enum


class ToolType(str, enum.Enum):
    VISUALFOODEXTRACTION = "VisualFoodExtraction"


def _pil_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image = image.convert("RGB")
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def food_extraction(
    thread_id: str, image: Image, message: str | None = None, header: dict = {}
) -> types.AdvisorResponse:
    """
    Extracts visual food information from an image and sends it to the AI advisor.

    Args:
        thread_id (str): The ID of the conversation thread.
        image (Image): The image containing the food to be analyzed.
        message (str, optional): An optional message to accompany the image. Defaults to None.
        header (dict, optional): The authorization header. Defaults to an empty dictionary.

    Returns:
        types.AdvisorResponse: The response from the AI advisor containing the extracted food information.
    """

    url = f"{constants.THREAD_URL}/{thread_id}/messages/tools/vision/{ToolType.VISUALFOODEXTRACTION.value}"
    image_str = _pil_to_base64(image)

    resp = requests.post(
        url,
        headers=header,
        json={"image": constants.BASE64_IMAGE + image_str, "message": message},
    )
    r = types.AdvisorResponse.model_validate(resp.json())
    return r


