from flask import Flask, request, jsonify
from analyzer import analyze_resume
from parser import parse_resume
from flask_cors import CORS  # <-- import

app = Flask(__name__)
CORS(app)  # <-- enable CORS for all routes

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
    app.run(debug=True)
