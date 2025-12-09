import os
import requests
from backend.parser import parse_resume
from backend.analyzer import analyze_resume
from io import BytesIO

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"


def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)


def handle_update(update):
    if "message" not in update:
        return

    message = update["message"]
    chat_id = message["chat"]["id"]
    

    # ---- Handle /start ----
    if "text" in message and message["text"] == "/start":
        user_first = message["from"]["first_name"]
        user_username = message["from"].get("username")
        # prefer @username, else fallback 
        name = f"@{user_username}" if user_username else user_first
        
        send_message(chat_id,  f"👋 Hi {name}!\n\nSend your resume (PDF, DOCX, TXT).\nI'll analyze it instantly.")
        return

    # ---- File Upload ----
    if "document" in message:

        # ❗ Reject forwarded protected files
        if message.get("forward_origin") or message.get("forward_from"):
            send_message(chat_id,
                         "❌ I cannot analyze forwarded files.\nPlease upload the resume directly.")
            return

        file_id = message["document"]["file_id"]

        # 1️⃣ Get file info safely
        file_info = requests.get(
            BASE_URL + "getFile",
            params={"file_id": file_id}
        ).json()

        if not file_info.get("ok"):
            send_message(chat_id,
                         "❌ Cannot download this file.\nIt may be protected or forwarded from another bot.")
            return

        file_path = file_info["result"]["file_path"]

        # 2️⃣ Download file
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        file_bytes = requests.get(file_url).content

        resume_file = BytesIO(file_bytes)
        resume_file.filename = message["document"]["file_name"]

        # 3️⃣ Extract text
        text = parse_resume(resume_file)

        # 4️⃣ Analyze text
        result = analyze_resume(text)

        # 5️⃣ Format output
        formatted = f"""
📄 *Resume Analysis Report*

⭐ *ATS Score:* {result['ats_score']}%

🧩 *Skills Found:*
{", ".join(result['skills']) if result['skills'] else "None"}

📝 *Resume Length:* {result['word_count']} words

📧 *Email(s):*
{", ".join(result['emails']) if result['emails'] else "Not found"}

📞 *Phone(s):*
{", ".join(result['phones']) if result['phones'] else "Not found"}

💡 *Suggestions:*
{chr(10).join("✓ " + s for s in result['suggestions'])}
"""

        send_message(chat_id, formatted)
        return

    # Default fallback
    send_message(chat_id, "❌ Send a resume file (PDF / DOCX / TXT).")
