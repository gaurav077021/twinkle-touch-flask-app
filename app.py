from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1oHHzLUl_XW2pk3F7GXX55yrrrjbS8qsD2r6HX2SX9rA").sheet1

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    phone = data.get("phone", "")

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")   # Example: 2025-08-19
    time = now.strftime("%H:%M:%S")   # Example: 15:42:10

    # Append date, time, phone
    sheet.append_row([date, time, phone])

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(port=5000)
