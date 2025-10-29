import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils import (
    beautify_face_picwish,
    remove_background_picwish,
    enhance_image_picwish,
    change_background_picwish,  # ✅ fungsi baru untuk ubah background
    download_and_save_image
)

# 🌱 Load environment (.env atau Render Environment)
load_dotenv()

# 🚀 Flask setup
app = Flask(__name__, static_folder="output")
CORS(app)

# 🧩 Konfigurasi environment
PICWISH_API_KEY = os.getenv("PICWISH_API_KEY")
PORT = int(os.getenv("PORT", 8080))
os.makedirs("output", exist_ok=True)

# 🪵 Logging setup
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

@app.route("/")
def home():
    return jsonify({"message": "✅ AI Photo Editor Backend is running!"})

# 🎨 BEAUTIFY / FACE ENHANCEMENT
@app.route("/api/beautify", methods=["POST"])
def api_beautify():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        result_url = beautify_face_picwish(PICWISH_API_KEY, img_path)
        output_path = download_and_save_image(result_url, "beautified.png")
        image_url = f"{request.host_url.rstrip('/')}/{output_path}"
        return jsonify({"image_url": image_url})
    except Exception as e:
        app.logger.error(f"Beautify failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 🧼 REMOVE BACKGROUND
@app.route("/api/remove_bg", methods=["POST"])
def api_remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        result_url = remove_background_picwish(PICWISH_API_KEY, img_path)
        output_path = download_and_save_image(result_url, "background_removed.png")
        image_url = f"{request.host_url.rstrip('/')}/{output_path}"
        return jsonify({"image_url": image_url})
    except Exception as e:
        app.logger.error(f"Background removal failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 🧠 CHANGE BACKGROUND (pakai prompt dari user)
@app.route("/api/background", methods=["POST"])
def api_background():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt required to change background"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        app.logger.info(f"🎨 Changing background with prompt: '{prompt}'")
        result_url = change_background_picwish(PICWISH_API_KEY, img_path, prompt)
        output_path = download_and_save_image(result_url, "background_changed.png")
        image_url = f"{request.host_url.rstrip('/')}/{output_path}"
        return jsonify({"image_url": image_url})
    except Exception as e:
        app.logger.error(f"Background change failed: {e}", exc_info=True)
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
        image_url = f"{request.host_url.rstrip('/')}/{output_path}"
        return jsonify({"image_url": image_url})
    except Exception as e:
        app.logger.error(f"Style enhance failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 📁 Serve hasil file output
@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)

# 🚀 Jalankan server
if __name__ == "__main__":
    app.logger.info(f"🌐 Starting server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
