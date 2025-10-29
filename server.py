from flask import Flask, request, jsonify
from utils import (
    beautify_face_picwish,
    enhance_image_picwish,
    save_base64_image,
)
import os
import uuid
import requests

app = Flask(__name__)

# 🔑 API key PicWish
PICWISH_API_KEY = os.getenv("PICWISH_API_KEY", "ISI_API_KEY_KAMU_DI_SINI")

# Buat folder penyimpanan
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

# ===========================
# Endpoint: AI BEAUTIFY
# ===========================
@app.route("/api/beautify", methods=["POST"])
def beautify():
    try:
        file = request.files["image"]
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = os.path.join("uploads", filename)
        file.save(file_path)

        result_url = beautify_face_picwish(PICWISH_API_KEY, file_path)
        return jsonify({"image": result_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===========================
# Endpoint: CHANGE BACKGROUND (pakai prompt)
# ===========================
@app.route("/api/change_background", methods=["POST"])
def change_background():
    try:
        file = request.files["image"]
        prompt = request.form.get("prompt", "").strip()
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = os.path.join("uploads", filename)
        file.save(file_path)

        # 🔹 Kirim request ke API AI Background Change (contoh pakai Replicate/endpoint sendiri)
        response = requests.post(
            "https://api.openai.com/v1/images/edits",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', 'ISI_OPENAI_KEY_DI_SINI')}"
            },
            files={"image": open(file_path, "rb")},
            data={
                "model": "gpt-image-1",
                "prompt": f"Replace background with: {prompt or 'a clean studio background'}"
            },
        )

        data_json = response.json()
        if response.status_code != 200 or "data" not in data_json:
            raise Exception(f"Change Background Error: {data_json}")

        # Ambil hasil base64 image dari response
        image_b64 = data_json["data"][0]["b64_json"]
        output_file = f"{uuid.uuid4().hex}_changed.png"
        output_path = save_base64_image(image_b64, output_file)

        return jsonify({"image": f"https://fotogenix-backend.onrender.com/{output_path}"})
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
        file_path = os.path.join("uploads", filename)
        file.save(file_path)

        result_url = enhance_image_picwish(PICWISH_API_KEY, file_path)
        return jsonify({"image": result_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===========================
# Root Info
# ===========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Fotogenix AI Backend aktif ✅",
        "available_endpoints": [
            "/api/beautify",
            "/api/change_background",
            "/api/style"
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
