from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

SIZES = {
    "small": 60,
    "medium": 80,
    "large": 100
}

FLAVORS = [
    "vanilla",
    "chocolate",
    "strawberry",
    "mango",
    "butterscotch"
]

TOPPINGS = [
    "sprinkles",
    "choco chips",
    "chips",
    "nuts",
    "caramel"
]

@app.route("/")
def home():
    return "✅ ScoopBot backend is live"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    text = req.get("query", "").lower()

    # Detect size
    size = next((s for s in SIZES if s in text), None)

    # Detect flavor
    flavor = next((f for f in FLAVORS if f in text), None)

    # Detect topping
    topping = next((t for t in TOPPINGS if t in text), None)

    if size and flavor:
        price = SIZES[size]
        topping_text = "no topping"

        if topping:
            price += 20
            topping_text = topping

        reply = (
            f"🍦 Order confirmed!\n"
            f"{size.capitalize()} {flavor} ice cream\n"
            f"Topping: {topping_text}\n"
            f"Total: ₹{price}"
        )
    else:
        reply = (
            "Here’s our menu 🍨\n"
            "Sizes: Small ₹60, Medium ₹80, Large ₹100\n"
            "Flavors: Vanilla, Chocolate, Strawberry, Mango, Butterscotch\n"
            "Toppings (+₹20): Sprinkles, Choco Chips, Nuts, Caramel\n\n"
            "Try: “Large chocolate with sprinkles”"
        )

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
