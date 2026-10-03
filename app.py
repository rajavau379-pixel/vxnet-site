import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.environ.get('CHAT_ID', '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.json
    service = data.get('service')
    name = data.get('name')
    contact = data.get('contact')
    message = data.get('message')

    telegram_message = (
        f"🔔 *New Service Request!*\n\n"
        f"🛠 *Service:* {service}\n"
        f"👤 *Name:* {name}\n"
        f"📱 *Contact:* {contact}\n"
        f"💬 *Details:* {message}"
    )

    if TELEGRAM_BOT_TOKEN and CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHAT_ID,
                "text": telegram_message,
                "parse_mode": "Markdown"
            }
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Telegram notification failed: {e}")

    return jsonify({"status": "success", "message": "Request received successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
