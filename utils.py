import os
import time
import base64
import requests


# ===================================
# SAVE BASE64 IMAGE
# ===================================
def save_base64_image(b64_data, filename):
    os.makedirs("output", exist_ok=True)
    image_bytes = base64.b64decode(b64_data)
    output_path = f"output/{filename}"
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path


# ===================================
# 1️⃣ BEAUTIFY FACE (PicWish)
# ===================================
def beautify_face_picwish(api_key, image_path):
    """AI Beautify / Face Enhancement"""
    url = "https://techhk.aoscdn.com/api/tasks/visual/face_beautify"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {"whitening": 0.3, "smoothing": 0.5}

    response = requests.post(url, headers=headers, files=files, data=data)
    data_json = response.json()

    if response.status_code != 200 or "data" not in data_json:
        raise Exception(f"Beautify Error: {data_json}")

    return data_json["data"]["image"]


# ===================================
# 2️⃣ CHANGE BACKGROUND (TechHK)
# ===================================
def change_background_techhk(api_key, image_path, prompt=None, scene_type="105"):
    """
    Ubah background foto.
    Bisa pakai 'prompt' deskripsi (contoh: 'beach sunset', 'modern studio background')
    atau scene_type default (105 = studio).
    """
    try:
        # 1️⃣ Buat task
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

        # 2️⃣ Cek hasil (polling)
        url_result = f"https://techhk.aoscdn.com/api/tasks/visual/background/{task_id}"
        for _ in range(20):  # ±40 detik
            res = requests.get(url_result, headers=headers)
            if res.status_code == 200:
                data = res.json().get("data", {})
                if data.get("state_detail") == "Complete":
                    return data.get("image_1")
            time.sleep(2)

        raise Exception("Timeout: Background generation not completed.")
    except Exception as e:
        raise Exception(f"ChangeBackground Error: {e}")


# ===================================
# 3️⃣ VISUAL MAKEOVER (STYLE)
# ===================================
def visual_makeover_picwish(api_key, image_path, style="comic"):
    """
    Ubah gaya foto menjadi comic / vector / realistic / painting / cartoon / anime dll.
    """
    url = "https://techhk.aoscdn.com/api/tasks/visual/transfer"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {
        "sync": 1,
        "style": style,  # contoh: "comic", "vector", "painting", "anime"
        "return_type": 1
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    data_json = response.json()

    if response.status_code != 200 or "data" not in data_json:
        raise Exception(f"Makeover Error: {data_json}")

    return data_json["data"]["image"]
