import axios from "axios";
import FormData from "form-data";

const TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_API = `https://api.telegram.org/bot${TOKEN}`;
const ANALYZE_API = "https://resume-analyzer1-8cte.onrender.com/analyze";

export default async function handler(req, res) {

  if (req.method !== "POST") {
    return res.status(200).json({ status: "Resume Bot Running" });
  }

  try {
    const update = req.body;
    if (!update.message) return res.status(200).end();

    const chatId = update.message.chat.id;
    const text = update.message.text || "";

    // ------------------- COMMANDS -------------------
    if (text.startsWith("/")) {
      if (text === "/start") {
        await axios.post(`${TELEGRAM_API}/sendMessage`, {
          chat_id: chatId,
          text: `👋 Welcome to the Resume Analyzer Bot!\n\nSend me any *PDF, DOCX, or TXT resume*, and I will analyze it in seconds.`,
          parse_mode: "Markdown"
        });
        return res.status(200).end();
      }

      if (text === "/help") {
        await axios.post(`${TELEGRAM_API}/sendMessage`, {
          chat_id: chatId,
          text: `📘 *How to Use*\n\n1️⃣ Send a resume file (.pdf, .docx, .txt)\n2️⃣ Wait for analysis\n3️⃣ Get detailed breakdown instantly\n\n⚡ Powered by Smart Resume Analyzer`,
          parse_mode: "Markdown"
        });
        return res.status(200).end();
      }
    }

    // ------------------- FILE HANDLING -------------------
    let fileId = null;
    let fileName = "";

    if (update.message.document) {
      fileId = update.message.document.file_id;
      fileName = update.message.document.file_name;
    }

    if (!fileId) {
      await axios.post(`${TELEGRAM_API}/sendMessage`, {
        chat_id: chatId,
        text: "📄 Please send a *PDF, DOCX, or TXT resume*."
      });
      return res.status(200).end();
    }

    // Validate file extension
    if (
      !fileName.endsWith(".pdf") &&
      !fileName.endsWith(".docx") &&
      !fileName.endsWith(".txt")
    ) {
      await axios.post(`${TELEGRAM_API}/sendMessage`, {
        chat_id: chatId,
        text: "❌ Unsupported file type.\nSend only: PDF, DOCX, TXT"
      });
      return res.status(200).end();
    }

    // Processing message
    const processingMessage = await axios.post(`${TELEGRAM_API}/sendMessage`, {
      chat_id: chatId,
      text: "📥 Downloading your resume...",
    });
    const msgId = processingMessage.data.result.message_id;

    // ------------------- GET FILE FROM TELEGRAM -------------------
    const fileInfo = await axios.get(
      `${TELEGRAM_API}/getFile?file_id=${fileId}`
    );

    const filePath = fileInfo.data.result.file_path;
    const fileUrl = `https://api.telegram.org/file/bot${TOKEN}/${filePath}`;

    // Update status
    await axios.post(`${TELEGRAM_API}/editMessageText`, {
      chat_id: chatId,
      message_id: msgId,
      text: "📤 Uploading your resume to Analyzer..."
    });

    // ------------------- SEND FILE TO BACKEND -------------------
    const fileResponse = await axios.get(fileUrl, {
      responseType: "arraybuffer"
    });

    const form = new FormData();
    form.append("file", Buffer.from(fileResponse.data), fileName);

    const analysis = await axios.post(ANALYZE_API, form, {
      headers: form.getHeaders(),
    });

    // ------------------- SEND RESULT -------------------
    await axios.post(`${TELEGRAM_API}/editMessageText`, {
      chat_id: chatId,
      message_id: msgId,
      text: "📊 Resume Analyzed! Preparing report..."
    });

    const pretty = JSON.stringify(analysis.data, null, 2);

    await axios.post(`${TELEGRAM_API}/sendMessage`, {
      chat_id: chatId,
      text: `<b>📄 Resume Analysis Result:</b>\n\n<pre>${pretty}</pre>`,
      parse_mode: "HTML"
    });

    return res.status(200).json({ status: "Success" });

  } catch (err) {
    console.error("Bot error:", err.message);
    return res.status(200).json({ status: "Error" });
  }
}
