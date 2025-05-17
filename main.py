import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
BOT_TOKEN = os.getenv("bot_token")
CHAT_ID = os.getenv("chat_id")  # میتونی این رو ثابت بذاری یا از پیام‌ها بخونی
PROJECT_MAPPER = {
    1:"بازیگوشی"
}
def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    return response

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update:
        text = update['message']
        project = update.get('project_id', 1)

        send_telegram_message(CHAT_ID, f'''
نوتیفیکیشن پروژه : {PROJECT_MAPPER.get(project)}
    --------------------------------------------
    {text}
    ''')

    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway PORT env
    app.run(host="0.0.0.0", port=port)
