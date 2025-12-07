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
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    text = parse_resume(file)

    if not text or text.strip() == "":
        return jsonify({"error": "Could not extract text from resume"}), 400

    result = analyze_resume(text)
    return jsonify(result)


# ⭐ THIS IS THE MOST IMPORTANT PART ⭐
@app.route("/api/bot", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if data:
        handle_update(data)

    return jsonify({"status": "ok"}), 200   # MUST return 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
