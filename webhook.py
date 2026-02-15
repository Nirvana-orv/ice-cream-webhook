from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # allows cross-origin requests from your HTML UI

# Home route to check if backend is live
@app.route("/")
def home():
    return "✅ Chatbot backend is live"

# Webhook route for ice cream orders
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req = request.get_json(force=True)  # parse JSON

        # Extract custom UI input
        user_text = req.get("query", "")

        # Try to get order parameters from UI or Dialogflow
        flavor = req.get("flavor") or req.get("Flavour") or req.get("queryResult", {}).get("parameters", {}).get("Flavour")
        size = req.get("size") or req.get("Size") or req.get("queryResult", {}).get("parameters", {}).get("Size")
        topping = req.get("topping") or req.get("queryResult", {}).get("parameters", {}).get("topping")

        # If any of flavor, size, or topping exists, calculate price
        if flavor or size or topping:
            flavor = flavor or "ice cream"
            size = size or "medium"
            topping = topping or "no topping"

            # base price by size
            size_lower = size.lower()
            if size_lower == "small":
                price = 60
            elif size_lower == "medium":
                price = 80
            elif size_lower == "large":
                price = 100
            else:
                price = 80  # default medium

            # add topping price
            if topping.lower() not in ["no", "none", "no topping"]:
                price += 20

            reply = f"Your {size} {flavor} ice cream with {topping} costs ₹{price}."
        else:
            # Default reply for any other message
            reply = f"You said: {user_text}"

        return jsonify({"reply": reply})

    except Exception as e:
        # Catch all errors so frontend always gets JSON
        return jsonify({"reply": "Oops, something went wrong on server 😅"}), 200

# Run on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
