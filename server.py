import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils import beautify_image, change_background, change_style, save_base64_image

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="output")
CORS(app)

# Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8080))

# Ensure output folder exists
os.makedirs("output", exist_ok=True)

# -----------------------------------------------------
# ROOT
# -----------------------------------------------------
@app.route("/")
def home():
    return jsonify({"message": "✅ AI Photo Editor Backend is running!"})

# -----------------------------------------------------
# BEAUTIFY ENDPOINT
# -----------------------------------------------------
@app.route("/api/beautify", methods=["POST"])
def api_beautify():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    b64 = beautify_image(OPENAI_API_KEY, img_path)
    output_path = save_base64_image(b64, "beautified.png")

    return jsonify({"image_url": f"{request.host_url}{output_path}"})

# -----------------------------------------------------
# CHANGE BACKGROUND ENDPOINT (now supports mask)
# -----------------------------------------------------
@app.route("/api/background", methods=["POST"])
def api_background():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "simple studio background").strip()

    # Save uploaded image
    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    # Optional mask upload
    mask_path = None
    if "mask" in request.files:
        mask = request.files["mask"]
        mask_path = os.path.join("output", f"mask_{mask.filename}")
        mask.save(mask_path)

    # Process background change
    b64 = change_background(OPENAI_API_KEY, img_path, prompt, mask_path)
    output_path = save_base64_image(b64, "background_changed.png")

    return jsonify({"image_url": f"{request.host_url}{output_path}"})

# -----------------------------------------------------
# STYLE TRANSFORMATION ENDPOINT
# -----------------------------------------------------
@app.route("/api/style", methods=["POST"])
def api_style():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "cartoon").strip()

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    b64 = change_style(OPENAI_API_KEY, img_path, prompt)
    output_path = save_base64_image(b64, "styled.png")

    return jsonify({"image_url": f"{request.host_url}{output_path}"})

# -----------------------------------------------------
# STATIC FILE SERVE
# -----------------------------------------------------
@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)

# -----------------------------------------------------
# ENTRY POINT
# -----------------------------------------------------
if __name__ == "__main__":
    print("✅ Run using Gunicorn, not Flask dev server.")
