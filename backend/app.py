from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .analyzer import analyze_resume
from .parser import parse_resume
import os

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/frontend")

CORS(app)

# -------- API Route --------
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

# -------- Serve React frontend --------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# -------- Run Flask --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
