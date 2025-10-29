import os
import base64
import requests
import time

# ===================================
# SAVE BASE64 / DOWNLOAD IMAGE
# ===================================
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


# ===================================
# BEAUTIFY FACE (PicWish)
# ===================================
def beautify_face_picwish(api_key, image_path, scale_factor=1):
    """AI Beautify / Face Enhancement"""
    url = "https://techhk.aoscdn.com/api/tasks/visual/scale"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {
        "sync": 1,
        "type": "face",
        "scale_factor": scale_factor,
        "return_type": 1
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    data_json = response.json()

    if response.status_code != 200 or "data" not in data_json:
        raise Exception(f"PicWish Beautify Error: {data_json}")

    return data_json["data"]["image"]


# ===================================
# REMOVE BACKGROUND (PicWish)
# ===================================
def remove_background_picwish(api_key, image_path):
    """Remove Background"""
    url = "https://techhk.aoscdn.com/api/tasks/visual/segmentation"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {"sync": 1}
    response = requests.post(url, headers=headers, files=files, data=data)
    data_json = response.json()

    if response.status_code != 200 or "data" not in data_json:
        raise Exception(f"PicWish Background Error: {data_json}")

    return data_json["data"]["image"]


# ===================================
# ENHANCE IMAGE (PicWish)
# ===================================
def enhance_image_picwish(api_key, image_path):
    """AI Style Enhancement"""
    url = "https://techhk.aoscdn.com/api/tasks/visual/scale"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {
        "sync": 1,
        "type": "image",
        "scale_factor": 2,
        "return_type": 1
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    data_json = response.json()

    if response.status_code != 200 or "data" not in data_json:
        raise Exception(f"PicWish Enhance Error: {data_json}")

    return data_json["data"]["image"]


# ===================================
# CHANGE BACKGROUND (TechHK Visual API)
# ===================================
def change_background_techhk(api_key, image_path, prompt=None, scene_type="105"):
    """
    Generate new background using TechHK Visual Background API.
    - image_path: local path
    - prompt: optional text-based background description
    - scene_type: integer (default 105)
    """
    try:
        # 1️⃣ Create task
        url_create = "https://techhk.aoscdn.com/api/tasks/visual/background"
        headers = {"X-API-KEY": api_key}
        files = {"image_file": open(image_path, "rb")}
        data = {}
        if prompt:
            data["prompt"] = prompt
        else:
            data["scene_type"] = scene_type

        response = requests.post(url_create, headers=headers, files=files, data=data)
        if response.status_code != 200:
            raise Exception(f"Create Task Error: {response.text}")

        resp_json = response.json()
        task_id = resp_json["data"]["task_id"]

        # 2️⃣ Poll until complete
        url_result = f"https://techhk.aoscdn.com/api/tasks/visual/background/{task_id}"
        for _ in range(20):  # max ±40 detik
            res = requests.get(url_result, headers=headers)
            if res.status_code == 200:
                data = res.json().get("data", {})
                if data.get("state_detail") == "Complete":
                    return data.get("image_1")
            time.sleep(2)

        raise Exception("Timeout: Background generation not completed.")

    except Exception as e:
        raise Exception(f"ChangeBackground Error: {e}")
