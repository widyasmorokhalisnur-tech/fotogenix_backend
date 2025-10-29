import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils import (
    beautify_face_picwish,
    remove_background_picwish,
    enhance_image_picwish,
    download_and_save_image
)

# 🌱 Load environment (.env atau Render Environment)
load_dotenv()

# 🚀 Flask setup
app = Flask(__name__, static_folder="output")
CORS(app)

# 🧩 Konfigurasi dari environment Render
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
        app.logger.warning("⚠️ No image uploaded for beautify")
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)
    app.logger.info(f"🖼️ Beautify: received image '{img.filename}' saved to {img_path}")

    try:
        app.logger.info("➡️ Sending to PicWish beautify API...")
        result_url = beautify_face_picwish(PICWISH_API_KEY, img_path)
        app.logger.info(f"✅ PicWish result URL: {result_url}")

        output_path = download_and_save_image(result_url, "beautified.png")
        app.logger.info(f"✅ Saved output to {output_path}")

        image_url = f"{request.host_url.rstrip('/')}/{output_path}"
        app.logger.info(f"✅ Returning image URL: {image_url}")

        return jsonify({"image_url": image_url})
    except Exception as e:
        app.logger.error(f"❌ Beautify failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 🖼️ BACKGROUND REMOVAL
@app.route("/api/background", methods=["POST"])
def api_background():
    if "image" not in request.files:
        app.logger.warning("⚠️ No image uploaded for background removal")
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)
    app.logger.info(f"🖼️ Background removal: received image '{img.filename}' saved to {img_path}")

    try:
        app.logger.info("➡️ Sending to PicWish background removal API...")
        result_url = remove_background_picwish(PICWISH_API_KEY, img_path)
        app.logger.info(f"✅ PicWish result URL: {result_url}")

        output_path = download_and_save_image(result_url, "background_removed.png")
        app.logger.info(f"✅ Saved output to {output_path}")

        image_url = f"{request.host_url.rstrip('/')}/{output_path}"
        app.logger.info(f"✅ Returning image URL: {image_url}")

        return jsonify({"image_url": image_url})
    except Exception as e:
        app.logger.error(f"❌ Background removal failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# ✨ STYLE / ENHANCE
@app.route("/api/style", methods=["POST"])
def api_style():
    if "image" not in request.files:
        app.logger.warning("⚠️ No image uploaded for style enhance")
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "").strip()
    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)
    app.logger.info(f"🎨 Style enhance: received '{img.filename}' with prompt '{prompt}'")

    try:
        app.logger.info("➡️ Sending to PicWish enhance API...")
        result_url = enhance_image_picwish(PICWISH_API_KEY, img_path)
        app.logger.info(f"✅ PicWish result URL: {result_url}")

        output_path = download_and_save_image(result_url, "styled.png")
        app.logger.info(f"✅ Saved output to {output_path}")

        image_url = f"{request.host_url.rstrip('/')}/{output_path}"
        app.logger.info(f"✅ Returning image URL: {image_url}")

        return jsonify({"image_url": image_url})
    except Exception as e:
        app.logger.error(f"❌ Style enhance failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 📁 Serve file hasil output
@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)

# 🚀 Jalankan server
if __name__ == "__main__":
    app.logger.info(f"🌐 Starting server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
