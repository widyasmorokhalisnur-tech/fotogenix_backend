import base64
from openai import OpenAI
from rembg import remove
from PIL import Image

def beautify_image(api_key, image_path):
    client = OpenAI(api_key=api_key)

    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt="Enhance this portrait photo naturally while keeping identity realistic."
        )
    return result.data[0].b64_json


def change_background(api_key, image_path, prompt):
    with open(image_path, "rb") as f:
        input_bytes = f.read()
    foreground = remove(input_bytes)

    fg_path = "output/foreground.png"
    mask_path = "output/mask.png"
    with open(fg_path, "wb") as f:
        f.write(foreground)

    img = Image.open(fg_path).convert("RGBA")
    alpha = img.split()[3]
    mask = Image.eval(alpha, lambda a: 255 - a)
    mask.save(mask_path)

    client = OpenAI(api_key=api_key)
    with open(fg_path, "rb") as img_file, open(mask_path, "rb") as mask_file:
        result = client.images.edit(
            model="gpt-image-1",
            image=img_file,
            mask=mask_file,
            prompt=f"Replace the background with {prompt}."
        )
    return result.data[0].b64_json


def change_style(api_key, image_path, style_prompt):
    client = OpenAI(api_key=api_key)
    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt=f"Apply {style_prompt} style while keeping subject realistic."
        )
    return result.data[0].b64_json


def save_base64_image(b64_data, filename):
    image_bytes = base64.b64decode(b64_data)
    output_path = f"output/{filename}"
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path
