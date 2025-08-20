from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
import datetime
import os
import json

app = Flask(__name__)

# Google Sheets setup
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

# Load creds from environment variable
service_account_info = json.loads(os.environ["GOOGLE_CREDS"])
creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
client = gspread.authorize(creds)

# Replace with your actual sheet ID
SHEET_ID = "1oHHzLUl_XW2pk3F7GXX55yrrrjbS8qsD2r6HX2SX9rA"
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        phone = data.get("phone", "")

        # Current date & time
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")   # YYYY-MM-DD
        time = now.strftime("%H:%M:%S")   # HH:MM:SS

        # Append row → [Date, Time, Phone]
        sheet.append_row([date, time, phone])

        return jsonify({
            "status": "success",
            "data": {"date": date, "time": time, "phone": phone}
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
