import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from utils import beautify_image, change_background, change_style, save_base64_image

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="output")
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8080))

# Pastikan folder output tersedia
os.makedirs("output", exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "AI Photo Editor Backend is running ✅"})

# ============================
# BEAUTIFY
# ============================
@app.route("/api/beautify", methods=["POST"])
def api_beautify():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    b64 = beautify_image(OPENAI_API_KEY, img_path)
    output = save_base64_image(b64, "beautified.png")

    image_url = request.host_url + f"output/{output}"
    return jsonify({"image_url": image_url})


# ============================
# BACKGROUND
# ============================
@app.route("/api/background", methods=["POST"])
def api_background():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    b64 = change_background(OPENAI_API_KEY, img_path)
    output = save_base64_image(b64, "background_changed.png")

    image_url = request.host_url + f"output/{output}"
    return jsonify({"image_url": image_url})


# ============================
# STYLE
# ============================
@app.route("/api/style", methods=["POST"])
def api_style():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join("output", img.filename)
    img.save(img_path)

    b64 = change_style(OPENAI_API_KEY, img_path)
    output = save_base64_image(b64, "style_changed.png")

    image_url = request.host_url + f"output/{output}"
    return jsonify({"image_url": image_url})


# ============================
# Serve output folder
# ============================
@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory("output", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
