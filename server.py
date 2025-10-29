# server.py
import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

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
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    url = "https://api.picwish.com/v1/beautify"
    headers = {"X-API-KEY": PICWISH_API_KEY}
    files = {"image_file": open(img_path, "rb")}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return jsonify({"error": response.text}), 500

    data = response.json()
    if "result_url" not in data:
        return jsonify({"error": "Invalid response from PicWish"}), 500

    result_url = data["result_url"]
    result = requests.get(result_url)
    output_path = "output/beautified.png"
    with open(output_path, "wb") as f:
        f.write(result.content)

    return jsonify({"image_url": f"{request.host_url}{output_path}"})

# 🖼️ BACKGROUND
@app.route("/api/background", methods=["POST"])
def api_background():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    url = "https://api.picwish.com/v1/remove-background"
    headers = {"X-API-KEY": PICWISH_API_KEY}
    files = {"image_file": open(img_path, "rb")}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return jsonify({"error": response.text}), 500

    data = response.json()
    if "result_url" not in data:
        return jsonify({"error": "Invalid response from PicWish"}), 500

    result_url = data["result_url"]
    result = requests.get(result_url)
    output_path = "output/background_changed.png"
    with open(output_path, "wb") as f:
        f.write(result.content)

    return jsonify({"image_url": f"{request.host_url}{output_path}"})

# ✨ STYLE / ENHANCE
@app.route("/api/style", methods=["POST"])
def api_style():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "").strip()
    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    url = "https://api.picwish.com/v1/enhance"
    headers = {"X-API-KEY": PICWISH_API_KEY}
    files = {"image_file": open(img_path, "rb")}
    data = {"prompt": prompt} if prompt else {}
    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code != 200:
        return jsonify({"error": response.text}), 500

    resp_json = response.json()
    if "result_url" not in resp_json:
        return jsonify({"error": "Invalid response from PicWish"}), 500

    result_url = resp_json["result_url"]
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
