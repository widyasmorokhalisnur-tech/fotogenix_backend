from flask import Flask, request, jsonify
from utils import beautify_face_picwish, change_background_techhk, visual_makeover_picwish
from dotenv import load_dotenv
import os
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Ambil API key PicWish/TechHK dari environment
PICWISH_API_KEY = os.getenv("PICWISH_API_KEY")

if not PICWISH_API_KEY:
    raise ValueError("❌ API Key belum diatur! Tambahkan PICWISH_API_KEY di file .env")

# ===========================
# 1️⃣ AI BEAUTY
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
        return jsonify({"error": f"Beautify Error: {str(e)}"}), 500


# ===========================
# 2️⃣ CHANGE BACKGROUND
# ===========================
@app.route("/api/change_background", methods=["POST"])
def change_background():
    try:
        file = request.files["image"]
        prompt = request.form.get("prompt", "modern clean studio background")
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = f"uploads/{filename}"
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)

        result_url = change_background_techhk(PICWISH_API_KEY, file_path, prompt)
        return jsonify({"image": result_url})
    except Exception as e:
        return jsonify({"error": f"Change Background Error: {str(e)}"}), 500


# ===========================
# 3️⃣ VISUAL MAKEOVER (STYLE)
# ===========================
@app.route("/api/makeover", methods=["POST"])
def makeover():
    try:
        file = request.files["image"]
        style = request.form.get("style", "comic")  # comic, vector, realistic, painting, dll
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = f"uploads/{filename}"
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)

        result_url = visual_makeover_picwish(PICWISH_API_KEY, file_path, style)
        return jsonify({"image": result_url})
    except Exception as e:
        return jsonify({"error": f"Makeover Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
