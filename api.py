from flask import Flask, request, jsonify
import os
from telegram import Bot

app = Flask(__name__)

# تنظیمات ربات تلگرام
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # توکن ربات خود را جایگزین کنید
TELEGRAM_CHANNEL_ID = '@your_channel_username'  # یا 'channel_chat_id'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# مسیر ذخیره‌سازی فایل‌ها
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    caption = request.form.get('caption', '')  # دریافت کپشن

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # ذخیره فایل
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # ارسال فایل به تلگرام با کپشن
    try:
        with open(file_path, 'rb') as f:
            bot.send_document(chat_id=TELEGRAM_CHANNEL_ID, document=f, caption=caption)
        return jsonify({"message": "File uploaded and sent to Telegram successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # حذف فایل پس از ارسال
        os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)
