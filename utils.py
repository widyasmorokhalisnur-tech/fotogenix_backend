import os
import base64
import requests

# ================================
# 🔧 Helper Functions
# ================================
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


# ================================
# ✨ PicWish API Wrappers
# ================================

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
    """
    Hapus background gambar → return URL hasil transparan (PNG)
    """
    url = "https://techhk.aoscdn.com/api/tasks/visual/segmentation"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {"sync": 1}  # sync=1 supaya hasil langsung dapat
    response = requests.post(url, headers=headers, files=files, data=data)
    data_json = response.json()

    if response.status_code != 200 or "data" not in data_json:
        raise Exception(f"PicWish Background Remove Error: {data_json}")

    return data_json["data"]["image"]


def enhance_image_picwish(api_key, image_path):
    """
    Tingkatkan kualitas gambar secara umum
    """
    url = "https://techhk.aoscdn.com/api/tasks/ai-enhance"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    response = requests.post(url, headers=headers, files=files)
    data = response.json()

    if response.status_code != 200 or "data" not in data:
        raise Exception(f"PicWish Enhance Error: {data}")

    return data["data"]["image"]


def change_background_picwish(api_key, image_path, prompt):
    """
    🧠 Ganti background menggunakan prompt (AI)
    API ini akan menggunakan endpoint replace-background.
    Prompt bisa berupa deskripsi background baru, contoh:
      'sunset beach', 'city skyline', 'fantasy forest', dll.
    """
    url = "https://techhk.aoscdn.com/api/tasks/visual/replace-background"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}
    data = {
        "sync": 1,
        "prompt": prompt,
        "return_type": 1
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    result = response.json()

    if response.status_code != 200 or "data" not in result:
        raise Exception(f"PicWish Change Background Error: {result}")

    return result["data"]["image"]
