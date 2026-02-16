from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Chatbot backend is live"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    text = data.get("query", "").lower()

    # detect size
    size = "medium"
    if "small" in text:
        size = "small"
    elif "large" in text:
        size = "large"

    # detect flavor
    flavor = None
    flavors = ["chocolate", "vanilla", "strawberry", "mango"]
    for f in flavors:
        if f in text:
            flavor = f
            break

    # detect topping
    topping = "no topping"
    if "sprinkle" in text:
        topping = "sprinkles"
    elif "nuts" in text:
        topping = "nuts"

    # pricing
    price = 80
    if size == "small":
        price = 60
    elif size == "large":
        price = 100

    if topping != "no topping":
        price += 20

    # response logic
    if "ice cream" in text or flavor:
        reply = f"🍦 A {size} {flavor or 'ice cream'} with {topping} will cost ₹{price}. Want anything else?"
    else:
        reply = "🙂 I'm here with you. Tell me more."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
