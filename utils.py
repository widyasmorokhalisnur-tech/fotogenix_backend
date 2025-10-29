# utils.py
import os
import base64
import requests

def save_base64_image(b64_data, filename):
    os.makedirs("output", exist_ok=True)
    image_bytes = base64.b64decode(b64_data)
    output_path = f"output/{filename}"
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path

def download_and_save_image(url, filename):
    os.makedirs("output", exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        output_path = f"output/{filename}"
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        raise Exception(f"Failed to download image: {response.status_code} - {response.text}")

def beautify_face_picwish(api_key, image_path, scale_factor=1):
    """
    Gunakan API /visual/scale dengan type="face" untuk beautify / face enhancement
    """
    url = "https://techhk.aoscdn.com/api/tasks/visual/scale"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {
        "sync": 1,          # langsung return hasil
        "type": "face",     # portrait enhancement
        "scale_factor": scale_factor,
        "return_type": 1    # return URL
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    data_json = response.json()

    if response.status_code != 200 or "data" not in data_json:
        raise Exception(f"PicWish Beautify Error: {data_json}")

    return data_json["data"]["image"]

def remove_background_picwish(api_key, image_path):
    url = "https://techhk.aoscdn.com/api/tasks/visual/segmentation"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {"sync": 1}  # sync=1 supaya hasil langsung dapat
    response = requests.post(url, headers=headers, files=files, data=data)
    data_json = response.json()

    if response.status_code != 200 or "data" not in data_json:
        raise Exception(f"PicWish Background Error: {data_json}")

    return data_json["data"]["image"]

def enhance_image_picwish(api_key, image_path):
    url = "https://techhk.aoscdn.com/api/tasks/ai-enhance"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    response = requests.post(url, headers=headers, files=files)
    data = response.json()

    if response.status_code != 200 or "data" not in data:
        raise Exception(f"PicWish Enhance Error: {data}")

    return data["data"]["image"]
