from flask import Flask, request, jsonify
from utils import (
    beautify_face_picwish,
    remove_background_picwish,
    enhance_image_picwish,
    save_base64_image,
)
import os
import uuid

app = Flask(__name__)

PICWISH_API_KEY = os.getenv("PICWISH_API_KEY", "ISI_API_KEY_KAMU_DI_SINI")

# ===========================
# Endpoint: AI BEAUTIFY
# ===========================
@app.route("/api/beautify", methods=["POST"])
def beautify():
    try:
        file = request.files["image"]
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = f"uploads/{filename}"
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)

        result_url = beautify_face_picwish(PICWISH_API_KEY, file_path)
        return jsonify({"image": result_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===========================
# Endpoint: CHANGE BACKGROUND
# ===========================
@app.route("/api/change_background", methods=["POST"])
def change_background():
    try:
        file = request.files["image"]
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = f"uploads/{filename}"
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)

        result_url = remove_background_picwish(PICWISH_API_KEY, file_path)
        return jsonify({"image": result_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===========================
# Endpoint: STYLE ENHANCEMENT
# ===========================
@app.route("/api/style", methods=["POST"])
def style():
    try:
        file = request.files["image"]
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = f"uploads/{filename}"
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)

        result_url = enhance_image_picwish(PICWISH_API_KEY, file_path)
        return jsonify({"image": result_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
