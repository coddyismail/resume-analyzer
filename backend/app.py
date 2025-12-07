# app.py
from flask import Flask, request, jsonify
from backend.analyzer import analyze_resume
from backend.parser import parse_resume
from backend.bot import handle_update
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    print("🔥 /analyze endpoint hit")

    if "file" not in request.files:
        print("❌ No file found in request")
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    print(f"📄 Received file: {file.filename}")

    text = parse_resume(file)
    print("📄 Extracted text length:", len(text) if text else 0)

    if not text or text.strip() == "":
        print("❌ No text extracted")
        return jsonify({"error": "Could not extract text from resume"}), 400

    result = analyze_resume(text)
    print("✅ Analysis Complete")
    return jsonify(result)


# ⭐ REQUIRED FOR TELEGRAM BOT ⭐
@app.route("/api/bot", methods=["POST"])
def telegram_webhook():
    print("🔥 Telegram webhook hit")

    data = request.get_json()
    print("📨 Update received:", data)

    if data:
        handle_update(data)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
