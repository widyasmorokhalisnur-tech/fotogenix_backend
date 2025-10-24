import base64
from openai import OpenAI

def beautify_image(api_key, image_path):
    """Percantik foto wajah secara natural."""
    client = OpenAI(api_key=api_key)
    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt="Enhance the portrait naturally, improve lighting and skin tone while keeping it realistic."
        )
    return result.data[0].b64_json


def change_background(api_key, image_path, prompt):
    """Ganti background berdasarkan prompt."""
    client = OpenAI(api_key=api_key)
    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt=f"Replace background with: {prompt}. Keep the main person clear and realistic."
        )
    return result.data[0].b64_json


def change_style(api_key, image_path, style_prompt):
    """Ubah gaya foto (cartoon, cinematic, oil painting, dll)."""
    client = OpenAI(api_key=api_key)
    with open(image_path, "rb") as img:
        result = client.images.edit(
            model="gpt-image-1",
            image=img,
            prompt=f"Transform this image into {style_prompt} style."
        )
    return result.data[0].b64_json


def save_base64_image(b64_data, filename):
    """Simpan hasil base64 ke file gambar dan kembalikan path-nya."""
    image_bytes = base64.b64decode(b64_data)
    output_path = f"output/{filename}"
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path
