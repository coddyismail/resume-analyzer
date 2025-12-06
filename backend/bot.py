# bot.py
import os
import requests
from backend.parser import parse_resume
from backend.analyzer import analyze_resume

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def handle_update(update):
    if "message" not in update:
        return

    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")

    # Handle /start command
    if text == "/start":
        send_message(chat_id, "👋 Hello! Send me your resume (PDF, DOCX, TXT) and I'll analyze it.")
        return

    # Check for document (resume) upload
    if "document" in update["message"]:
        file_id = update["message"]["document"]["file_id"]

        # 1️⃣ Get file path
        file_info = requests.get(BASE_URL + "getFile", params={"file_id": file_id}).json()
        file_path = file_info["result"]["file_path"]

        # 2️⃣ Download file
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        response = requests.get(file_url)
        file_bytes = response.content

        # 3️⃣ Use parser.py
        from io import BytesIO
        resume_file = BytesIO(file_bytes)
        resume_file.filename = update["message"]["document"]["file_name"]
        text = parse_resume(resume_file)

        # 4️⃣ Analyze
        result = analyze_resume(text)

        # 5️⃣ Send result back
        send_message(chat_id, f"✅ Resume analysis complete:\n{result}")
        return

    # Default response
    send_message(chat_id, "❌ Please send a resume file (PDF, DOCX, TXT).")
