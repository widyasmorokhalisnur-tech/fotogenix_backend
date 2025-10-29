import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils import (
    beautify_face_picwish,
    remove_background_picwish,
    enhance_image_picwish,
    download_and_save_image
)

# 🔹 Load .env (for local dev, Render akan auto load dari dashboard)
load_dotenv()

app = Flask(__name__, static_folder="output")
CORS(app)

# 🔑 Environment variables
PICWISH_API_KEY = os.getenv("PICWISH_API_KEY")
PORT = int(os.getenv("PORT", 8080))

# 🧩 Debug info — untuk memastikan API key terbaca
print("===========================================")
print("🚀 Server starting up...")
print(f"🔑 PICWISH_API_KEY Loaded: {bool(PICWISH_API_KEY)}")
print(f"🌐 Running on port: {PORT}")
print("===========================================")

# Pastikan folder output tersedia
os.makedirs("output", exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "✅ AI Photo Editor Backend is running!"})

# 🎨 BEAUTIFY / FACE ENHANCEMENT
@app.route("/api/beautify", methods=["POST"])
def api_beautify():
    if not PICWISH_API_KEY:
        return jsonify({"error": "API key not found. Please set PICWISH_API_KEY in environment."}), 500

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        result_url = beautify_face_picwish(PICWISH_API_KEY, img_path)
        output_path = download_and_save_image(result_url, "beautified.png")

        # Buat URL penuh Render (misal https://yourapp.onrender.com/output/...)
        full_url = request.host_url.rstrip("/") + "/" + output_path
        return jsonify({"image_url": full_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🖼️ BACKGROUND REMOVAL
@app.route("/api/background", methods=["POST"])
def api_background():
    if not PICWISH_API_KEY:
        return jsonify({"error": "API key not found. Please set PICWISH_API_KEY in environment."}), 500

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        result_url = remove_background_picwish(PICWISH_API_KEY, img_path)
        output_path = download_and_save_image(result_url, "background_removed.png")
        full_url = request.host_url.rstrip("/") + "/" + output_path
        return jsonify({"image_url": full_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✨ STYLE / ENHANCE
@app.route("/api/style", methods=["POST"])
def api_style():
    if not PICWISH_API_KEY:
        return jsonify({"error": "API key not found. Please set PICWISH_API_KEY in environment."}), 500

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "").strip()
    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    try:
        result_url = enhance_image_picwish(PICWISH_API_KEY, img_path)
        output_path = download_and_save_image(result_url, "styled.png")
        full_url = request.host_url.rstrip("/") + "/" + output_path
        return jsonify({"image_url": full_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔗 Serve image files
@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
