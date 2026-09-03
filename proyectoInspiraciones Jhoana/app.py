from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

products = {
    "Washitape": 10,
    "Stage": 5,
    "Stamps": 20,
    "Flexible Notebook": 35,
    "Organigasto": 120,
    "Memopad": 8,
    "Cat Divider": 8,
    "Large Divider": 8,
    "Flower Divider": 8,
    "Animal Divider": 8,
    "Animal Post-it": 8
}

@app.route("/")
def home():
    return render_template("order_form.html", products=products)

@app.route("/checkout", methods=["POST"])
def checkout():
    name = request.form.get("name")
    detail = request.form.get("detail")
    total = request.form.get("total")

    # Save orders per day
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"orders_{today}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {name} | {detail} | Total: {total}\n")

    # Build rows for table
    rows = []
    for item in detail.split(","):
        if ":" in item:
            product, qty = item.split(":")
            price = products[product]
            subtotal = int(qty) * price
            rows.append({"product": product, "qty": qty, "subtotal": subtotal})

    return render_template("checkout.html", name=name, rows=rows, total=total)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
