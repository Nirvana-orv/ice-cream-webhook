from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Home route to test if backend is live
@app.route("/")
def home():
    return "✅ Chatbot backend is live"
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"reply": "Oops, something went wrong on server 😅"}), 200
# Webhook route for your chatbot
@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True)
    if not req:
        return jsonify({"reply": "Sorry, I didn't get that."})

    # Check if it's coming from Dialogflow or custom UI
    user_text = req.get("query", "")
    
    # If parameters exist (Dialogflow style), extract them
    flavor = req.get("flavor") or req.get("Flavour")
    size = req.get("size") or req.get("Size")
    topping = req.get("topping")

    # If parameters exist, respond with ice cream order
    if flavor or size or topping:
        flavor = flavor or "ice cream"
        size = size or "medium"
        topping = topping or "no topping"

        price = 0
        if size.lower() == "small":
            price = 60
        elif size.lower() == "medium":
            price = 80
        elif size.lower() == "large":
            price = 100

        if topping.lower() not in ["no", "none", "no topping"]:
            price += 20

        reply = f"Your {size} {flavor} ice cream with {topping} costs ₹{price}."
    else:
        # Default reply for custom UI messages
        reply = f"You said: {user_text}"

    return jsonify({"reply": reply})

# Run the app on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

