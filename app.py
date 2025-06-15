from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TRADOVATE_URL = "https://demo.tradovateapi.com/v1"  # change to live when ready
ACCESS_TOKEN = os.getenv("TRADOVATE_ACCESS_TOKEN")   # stored securely in Render

@app.route("/")
def home():
    return "Trading Bot is Live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received webhook:", data)

    action = data.get("action")
    symbol = data.get("symbol", "MESM2025")
    quantity = data.get("qty", 3)

    if action == "ENTRY_LONG":
        send_order(symbol, "Buy", quantity)
    elif action == "ENTRY_SHORT":
        send_order(symbol, "Sell", quantity)
    elif action.startswith("EXIT"):
        close_position(symbol)

    return jsonify({"status": "ok"}), 200

def send_order(symbol, side, quantity):
    order = {
        "accountSpec": os.getenv("TRADOVATE_ACCOUNT_SPEC"),
        "accountId": int(os.getenv("TRADOVATE_ACCOUNT_ID")),
        "action": side,
        "symbol": symbol,
        "orderQty": quantity,
        "orderType": "Market"
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    res = requests.post(f"{TRADOVATE_URL}/order/placeorder", json=order, headers=headers)
    print("Order sent:", res.status_code, res.text)

def close_position(symbol):
    # Optional: custom logic to flatten positions
    print("Close logic not implemented yet")

if __name__ == "__main__":
    app.run(debug=True)
