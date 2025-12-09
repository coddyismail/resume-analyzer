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
        user_first = message["from"].get("first_name", "")
        user_username = message["from"].get("username")

        # Prefer @username → else first name
        name = f"@{user_username}" if user_username else user_first

        send_message(
            chat_id,
            f"👋 Hi {name}!\n\nSend your resume (PDF, DOCX, TXT).\nI'll analyze it instantly."
        )
        return

    # ---- File Upload ----
    if "document" in message:

        # Reject forwarded or protected files
        if message.get("forward_origin") or message.get("forward_from"):
            send_message(
                chat_id,
                "❌ I cannot analyze forwarded files.\nPlease upload the resume directly."
            )
            return

        file_id = message["document"]["file_id"]

        # Get file info
        file_info = requests.get(
            BASE_URL + "getFile",
            params={"file_id": file_id}
        ).json()

        if not file_info.get("ok"):
            send_message(
                chat_id,
                "❌ Cannot download this file.\nIt may be protected or forwarded from another bot."
            )
            return

        file_path = file_info["result"]["file_path"]

        # Download file
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        file_bytes = requests.get(file_url).content

        resume_file = BytesIO(file_bytes)
        resume_file.filename = message["document"]["file_name"]

        # Extract text
        text = parse_resume(resume_file)

        # Analyze
        result = analyze_resume(text)

        # Format response
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
check out our 8d audio bot at @eightdaudio_bot
"""

        send_message(chat_id, formatted)
        return

    # Default fallback
    send_message(chat_id, "❌ Send a resume file (PDF / DOCX / TXT).")
