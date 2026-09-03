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
# Connect to Supabase
url = "https://tfntvebjfawvmfypwshb.supabase.co"
key = "sb_publishable_XOVAUeupiJsrOHb_YcVZiQ_dD25Hn3w"
supabase_client = supabase.create_client(url, key)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        price_to_sell = request.form.get("price_to_sell")

        # Insert into products table
        data = {
            "product_id": product_id,
            "price_to_sell": price_to_sell
        }
        supabase_client.table("products").insert(data).execute()

        return redirect(url_for("list_products"))

    # Get items from Supabase to show in dropdown
    items = supabase_client.table("items").select("*").execute()
    return render_template("add_product.html", items=items.data)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
