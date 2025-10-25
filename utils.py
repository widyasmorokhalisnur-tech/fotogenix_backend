import base64
from openai import OpenAI
from rembg import remove
from PIL import Image

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
    """
    Replace the background using OpenAI Image Edit API with proper mask.
    Only background is replaced; main subject is preserved.
    """
    # Step 1: Remove background (transparent PNG)
    with open(image_path, "rb") as f:
        input_bytes = f.read()
    foreground = remove(input_bytes)

    fg_path = "output/foreground.png"
    mask_path = "output/mask.png"
    with open(fg_path, "wb") as f:
        f.write(foreground)

    # Step 2: Create mask from alpha channel
    img = Image.open(fg_path).convert("RGBA")
    alpha = img.split()[3]  # alpha channel
    mask = Image.eval(alpha, lambda a: 255 - a)  # invert: background=white/editable, subject=black/preserved
    mask.save(mask_path)

    # Step 3: OpenAI Image Edit with mask
    client = OpenAI(api_key=api_key)
    with open(fg_path, "rb") as img_file, open(mask_path, "rb") as mask_file:
        result = client.images.edit(
            model="gpt-image-1",
            image=img_file,
            mask=mask_file,
            prompt=f"Replace the background with {prompt}. Keep the main subject realistic and unchanged."
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
