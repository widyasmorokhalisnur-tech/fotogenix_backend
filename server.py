import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils import save_base64_image

# 🔧 Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="output")
CORS(app)

PICWISH_API_KEY = os.getenv("PICWISH_API_KEY")
PORT = int(os.getenv("PORT", 8080))

os.makedirs("output", exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "✅ AI Photo Editor Backend (PicWish) is running!"})


# 🎨 BEAUTIFY
@app.route("/api/beautify", methods=["POST"])
def api_beautify():
    """Enhance portrait image using PicWish Beautify API."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    # Kirim ke PicWish beautify endpoint
    url = "https://techhk.aoscdn.com/api/tasks/beautify/portrait"
    headers = {"X-API-KEY": PICWISH_API_KEY}
    files = {"image_file": open(img_path, "rb")}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return jsonify({"error": response.text}), 500

    data = response.json()
    if "data" not in data or "image" not in data["data"]:
        return jsonify({"error": "Invalid response from PicWish"}), 500

    # Hasil berupa URL gambar jadi kita download & simpan lokal
    result_url = data["data"]["image"]
    result = requests.get(result_url)
    output_path = "output/beautified.png"
    with open(output_path, "wb") as f:
        f.write(result.content)

    return jsonify({"image_url": f"{request.host_url}{output_path}"})


# 🖼️ BACKGROUND
@app.route("/api/background", methods=["POST"])
def api_background():
    """Ganti background menggunakan PicWish Remove BG API."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    url = "https://techhk.aoscdn.com/api/tasks/visual/segmentation"
    headers = {"X-API-KEY": PICWISH_API_KEY}
    files = {"image_file": open(img_path, "rb")}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return jsonify({"error": response.text}), 500

    data = response.json()
    if "data" not in data or "image" not in data["data"]:
        return jsonify({"error": "Invalid response from PicWish"}), 500

    # download hasil
    result_url = data["data"]["image"]
    result = requests.get(result_url)
    output_path = "output/background_changed.png"
    with open(output_path, "wb") as f:
        f.write(result.content)

    return jsonify({"image_url": f"{request.host_url}{output_path}"})


# ✨ STYLE TRANSFER
@app.route("/api/style", methods=["POST"])
def api_style():
    """Terapkan gaya tertentu ke foto (simulasi dengan beautify+enhancement)."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "cartoon").strip()
    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    # Sementara gunakan PicWish "enhance" untuk simulasi style (PicWish belum punya style khusus)
    url = "https://techhk.aoscdn.com/api/tasks/ai-enhance"
    headers = {"X-API-KEY": PICWISH_API_KEY}
    files = {"image_file": open(img_path, "rb")}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return jsonify({"error": response.text}), 500

    data = response.json()
    if "data" not in data or "image" not in data["data"]:
        return jsonify({"error": "Invalid response from PicWish"}), 500

    result_url = data["data"]["image"]
    result = requests.get(result_url)
    output_path = "output/styled.png"
    with open(output_path, "wb") as f:
        f.write(result.content)

    return jsonify({"image_url": f"{request.host_url}{output_path}"})


@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
