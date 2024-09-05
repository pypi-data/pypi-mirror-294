from PIL import Image
import requests
import io
import base64
from nutrition_ai import constants, types


def _pil_to_base64(image: Image) -> str:
    buffered = io.BytesIO()
    image = image.convert("RGB")
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def packaged_food(
    image: Image, content: str = "", header: dict = {}
) -> types.ProductResponse:
    """
    Analyze a packaged food product from an image.

    This function sends a POST request to the PACKAGED_PRODUCT_URL endpoint
    with an image of a packaged food product and optional text content.

    Args:
        image (Image): A PIL Image object of the packaged food product.
        content (str, optional): Additional text content related to the image. Defaults to an empty string.
        header (dict, optional): Additional headers for the HTTP request. Defaults to an empty dictionary.

    Returns:
        types.ProductResponse: A ProductResponse object containing information about the analyzed food product.

    Raises:
        requests.RequestException: If there's an error with the HTTP request.
        pydantic.ValidationError: If the response data doesn't match the ProductResponse model.

    Note:
        This function relies on an external API endpoint defined in constants.PACKAGED_PRODUCT_URL.
        Ensure that the API is accessible and the correct URL is set before using this function.
    """
    url = f"{constants.PACKAGED_PRODUCT_URL}"
    image_str = _pil_to_base64(image)
    resp = requests.post(
        url,
        headers=header,
        json={"image": constants.BASE64_IMAGE + image_str, "content": content},
    )
    r = types.ProductResponse.model_validate(resp.json())
    return r
