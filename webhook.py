from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True)

    parameters = req.get("queryResult", {}).get("parameters", {})

    flavor = parameters.get("Flavour", "ice cream")
    size = parameters.get("Size", "medium")
    topping = parameters.get("topping", "no topping")

    price = 0
    if size == "small":
        price = 60
    elif size == "medium":
        price = 80
    elif size == "large":
        price = 100

    if topping not in ["no", "none", "no topping"]:
        price += 20

    reply = f"Your {size} {flavor} ice cream with {topping} costs ₹{price}."

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":

    app.run(port=5000)
