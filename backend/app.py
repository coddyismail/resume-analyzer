# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze_resume
from parser import parse_resume
from bot import send_message

app = Flask(__name__)
CORS(app)

# ----------------------------
#  RESUME ANALYZER ENDPOINT
# ----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    parsed_text = parse_resume(file)
    analysis = analyze_resume(parsed_text)

    return jsonify({
        "parsed_text": parsed_text,
        "analysis": analysis
    })


# ----------------------------
#  TELEGRAM BOT WEBHOOK
# ----------------------------
@app.route("/api/bot", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Welcome! Send your resume PDF.")
        else:
            send_message(chat_id, "Upload your resume PDF as a document.")

    return jsonify({"ok": True})


@app.route("/", methods=["GET"])
def home():
    return "Resume Analyzer Backend Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
