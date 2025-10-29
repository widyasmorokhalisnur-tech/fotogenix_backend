import base64
import requests
import os

def save_base64_image(b64_data, filename):
    """
    Simpan gambar dari base64 string ke folder output dan kembalikan path-nya.
    """
    os.makedirs("output", exist_ok=True)
    image_bytes = base64.b64decode(b64_data)
    output_path = f"output/{filename}"
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path


def download_and_save_image(url, filename):
    """
    Download gambar dari URL (biasanya dari PicWish) dan simpan ke folder output.
    """
    os.makedirs("output", exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        output_path = f"output/{filename}"
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        raise Exception(f"Failed to download image: {response.status_code} - {response.text}")


def beautify_with_picwish(api_key, image_path):
    """
    Gunakan API PicWish untuk mempercantik foto wajah (beautify).
    """
    url = "https://techhk.aoscdn.com/api/tasks/beautify/portrait"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}

    response = requests.post(url, headers=headers, files=files)
    data = response.json()

    if response.status_code != 200 or "data" not in data:
        raise Exception(f"PicWish Beautify Error: {data}")

    return data["data"]["image"]  # URL hasil beautify


def remove_background_picwish(api_key, image_path):
    """
    Gunakan API PicWish untuk menghapus/mengganti background.
    """
    url = "https://techhk.aoscdn.com/api/tasks/visual/segmentation"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}

    response = requests.post(url, headers=headers, files=files)
    data = response.json()

    if response.status_code != 200 or "data" not in data:
        raise Exception(f"PicWish Background Error: {data}")

    return data["data"]["image"]  # URL hasil remove background


def enhance_image_picwish(api_key, image_path):
    """
    Gunakan API PicWish untuk meningkatkan kualitas (enhance/style simulasi).
    """
    url = "https://techhk.aoscdn.com/api/tasks/ai-enhance"
    headers = {"X-API-KEY": api_key}
    files = {"image_file": open(image_path, "rb")}

    response = requests.post(url, headers=headers, files=files)
    data = response.json()

    if response.status_code != 200 or "data" not in data:
        raise Exception(f"PicWish Enhance Error: {data}")

    return data["data"]["image"]  # URL hasil enhance
