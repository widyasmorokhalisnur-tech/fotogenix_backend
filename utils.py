import base64
from openai import OpenAI


def beautify_image(api_key, image_path):
    """Enhance a portrait photo naturally — no prompt from user."""
    client = OpenAI(api_key=api_key)

    base_prompt = (
        "Enhance this portrait photo naturally: improve lighting, smooth skin slightly, "
        "sharpen details, and keep the face and background realistic. "
        "Do not alter facial features or change the person's identity."
    )

    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt=base_prompt
        )
    return result.data[0].b64_json


def change_background(api_key, image_path, prompt):
    """Replace the background of an image using the given prompt."""
    client = OpenAI(api_key=api_key)
    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt=f"Replace the image background with: {prompt}. Keep the main subject clear and realistic."
        )
    return result.data[0].b64_json


def change_style(api_key, image_path, style_prompt):
    """Apply a new visual style (e.g. cartoon, cinematic, oil painting)."""
    client = OpenAI(api_key=api_key)
    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt=f"Transform this image into {style_prompt} style. Maintain composition and subject integrity."
        )
    return result.data[0].b64_json


def save_base64_image(b64_data, filename):
    """Save the base64-encoded image to the output folder and return its path."""
    image_bytes = base64.b64decode(b64_data)
    output_path = f"output/{filename}"
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path
