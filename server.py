import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils import beautify_image, change_background, change_style, save_base64_image

# 🔧 Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="output")
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8080))

# Ensure the output folder exists
os.makedirs("output", exist_ok=True)


@app.route("/")
def home():
    return jsonify({"message": "✅ AI Photo Editor Backend is running!"})


# ✅ Beautify: always natural, no user prompt
@app.route("/api/beautify", methods=["POST"])
def api_beautify():
    """Enhance a portrait image naturally (no prompt allowed)."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    # Always use the default base beautify prompt from utils.py
    b64 = beautify_image(OPENAI_API_KEY, img_path)
    output_path = save_base64_image(b64, "beautified.png")

    return jsonify({"image_url": f"{request.host_url}{output_path}"})


@app.route("/api/background", methods=["POST"])
def api_background():
    """Change the photo background based on a prompt."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "simple studio background").strip()
    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    b64 = change_background(OPENAI_API_KEY, img_path, prompt)
    output_path = save_base64_image(b64, "background_changed.png")

    return jsonify({"image_url": f"{request.host_url}{output_path}"})


@app.route("/api/style", methods=["POST"])
def api_style():
    """Apply a visual style to the photo."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    prompt = request.form.get("prompt", "cartoon").strip()
    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    b64 = change_style(OPENAI_API_KEY, img_path, prompt)
    output_path = save_base64_image(b64, "styled.png")

    return jsonify({"image_url": f"{request.host_url}{output_path}"})


@app.route("/output/<path:filename>")
def serve_output(filename):
    """Serve generated image files."""
    return send_from_directory("output", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
