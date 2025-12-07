# app.py
from flask import Flask, request, jsonify
from backend.analyzer import analyze_resume
from backend.parser import parse_resume
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    print("🔥 /analyze endpoint hit")   # Log entry

    if "file" not in request.files:
        print("❌ No file found in request")  # Log
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    print(f"📄 Received file: {file.filename}")  # Log

    text = parse_resume(file)
    print("📄 Extracted text length:", len(text) if text else 0)

    if not text or text.strip() == "":
        print("❌ No text extracted")  # Log
        return jsonify({"error": "Could not extract text from resume"}), 400

    result = analyze_resume(text)
    print("✅ Analysis Complete")  # Log
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
