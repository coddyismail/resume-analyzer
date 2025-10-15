from flask import Flask, request, jsonify, send_from_directory
from analyzer import analyze_resume
from parser import parse_resume
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# ✅ Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# ✅ Serve other static files like JS, CSS
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# ✅ Your main API endpoint
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
