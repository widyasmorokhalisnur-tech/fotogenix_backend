# server.py
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils import beautify_with_picwish, remove_background_picwish, enhance_image_picwish, download_and_save_image

load_dotenv()

app = Flask(__name__, static_folder="output")
CORS(app)

PICWISH_API_KEY = os.getenv("PICWISH_API_KEY")
PORT = int(os.getenv("PORT", 8080))
os.makedirs("output", exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "✅ AI Photo Editor Backend is running!"})

# 🎨 BEAUTIFY
@app.route("/api/beautify", methods=["POST"])
def api_beautify():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        result_url = beautify_with_picwish(PICWISH_API_KEY, img_path)
        output_path = download_and_save_image(result_url, "beautified.png")
        return jsonify({"image_url": f"{request.host_url}{output_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🖼️ BACKGROUND
@app.route("/api/background", methods=["POST"])
def api_background():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        result_url = remove_background_picwish(PICWISH_API_KEY, img_path)
        output_path = download_and_save_image(result_url, "background_removed.png")
        return jsonify({"image_url": f"{request.host_url}{output_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✨ STYLE / ENHANCE
@app.route("/api/style", methods=["POST"])
def api_style():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "").strip()
    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        result_url = enhance_image_picwish(PICWISH_API_KEY, img_path)
        output_path = download_and_save_image(result_url, "styled.png")
        return jsonify({"image_url": f"{request.host_url}{output_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
