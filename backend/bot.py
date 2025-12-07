import os
import requests
from backend.parser import parse_resume
from backend.analyzer import analyze_resume
from io import BytesIO

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"


def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)


def handle_update(update):
    if "message" not in update:
        return

    message = update["message"]
    chat_id = message["chat"]["id"]

    # ---- Handle /start ----
    if "text" in message and message["text"] == "/start":
        send_message(chat_id, "👋 Send your resume (PDF, DOCX, TXT). I'll analyze it.")
        return

    # ---- Handle File Upload ----
    if "document" in message:
        file_id = message["document"]["file_id"]

        # 1️⃣ Get file info
        file_info = requests.get(BASE_URL + "getFile", params={"file_id": file_id}).json()
        file_path = file_info["result"]["file_path"]

        # 2️⃣ Download file
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        file_bytes = requests.get(file_url).content

        resume_file = BytesIO(file_bytes)
        resume_file.filename = message["document"]["file_name"]

        # 3️⃣ Extract text
        text = parse_resume(resume_file)

        # 4️⃣ Analyze
        result = analyze_resume(text)

        # 5️⃣ Send result
        send_message(chat_id, "✅ Resume Analysis Complete:\n\n" + str(result))
        return

    # Default fallback
    send_message(chat_id, "❌ Send a resume file (PDF / DOCX / TXT).")
