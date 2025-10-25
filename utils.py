import base64
from openai import OpenAI
from PIL import Image


# -----------------------------------------------------
# BEAUTIFY IMAGE
# -----------------------------------------------------
def beautify_image(api_key, image_path):
    client = OpenAI(api_key=api_key)

    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt="Enhance this portrait photo naturally while keeping identity realistic. "
                   "Improve lighting, color balance, and clarity without over-smoothing."
        )

    return result.data[0].b64_json


# -----------------------------------------------------
# CHANGE BACKGROUND (supports optional mask)
# -----------------------------------------------------
def change_background(api_key, image_path, prompt, mask_path=None):
    client = OpenAI(api_key=api_key)

    if mask_path:
        # With mask — replace only transparent area
        with open(image_path, "rb") as img, open(mask_path, "rb") as mask:
            result = client.images.edit(
                model="gpt-image-1",
                image=img,
                mask=mask,
                prompt=f"Keep the subject identical. Replace ONLY the background with: {prompt}. "
                       "Maintain realism and natural lighting.",
                size="1024x1024"
            )
    else:
        # Without mask — AI auto-detects subject
        with open(image_path, "rb") as img:
            result = client.images.edit(
                model="gpt-image-1",
                image=img,
                prompt=f"Keep the person exactly the same. Replace ONLY the background with: {prompt}. "
                       "Maintain realism and consistent subject details.",
                size="1024x1024"
            )

    return result.data[0].b64_json


# -----------------------------------------------------
# CHANGE STYLE
# -----------------------------------------------------
def change_style(api_key, image_path, style_prompt):
    client = OpenAI(api_key=api_key)

    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt=f"Apply {style_prompt} artistic style while keeping the subject realistic "
                   "and preserving original composition.",
            size="1024x1024"
        )

    return result.data[0].b64_json


# -----------------------------------------------------
# SAVE BASE64 IMAGE TO FILE
# -----------------------------------------------------
def save_base64_image(b64_data, filename):
    image_bytes = base64.b64decode(b64_data)
    output_path = f"output/{filename}"

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    return output_path
