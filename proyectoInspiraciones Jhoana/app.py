from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

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
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
if not url or not key:
    raise ValueError("Supabase URL or Key is missing. Check your .env file.")

supabase_client: Client = create_client(url, key)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        price_to_sell = request.form.get("price_to_sell")
        revenue = request.form.get("revenue")
        profit_percentage = request.form.get("profit_percentage")

        supabase_client.table("products").insert({
            "product_id": product_id,
            "price_to_sell": price_to_sell,
            "revenue": revenue,
            "profit_percentage": profit_percentage
        }).execute()

        return redirect(url_for("list_products"))

    items = supabase_client.table("items").select("*").execute()
    return render_template("add_product.html", items=items.data)
@app.route("/list_products")
def list_products():
    # Traer todos los productos desde Supabase
    products = supabase_client.table("products").select("*").execute()
    # También traer info de items para mostrar nombre
    items = supabase_client.table("items").select("*").execute()

    # Crear un diccionario para mapear product_id → nombre
    item_map = {item["product_id"]: item["name"] for item in items.data}

    # Pasar productos y nombres al template
    return render_template("list_products.html", products=products.data, item_map=item_map)
@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form.get("name")
        provider = request.form.get("provider")
        short_description = request.form.get("short_description")
        quantity = request.form.get("quantity")
        time_of_purchase = request.form.get("time_of_purchase")
        unitary_price = request.form.get("unitary_price")

        # Insertar en la tabla items
        supabase_client.table("items").insert({
            "name": name,
            "provider": provider,
            "short_description": short_description,
            "time_of_purchase": time_of_purchase,
            "quantity": quantity,
            "unitary_price": unitary_price
        }).execute()

        return redirect(url_for("list_items"))

    return render_template("add_item.html")
@app.route("/list_items")
def list_items():
    items = supabase_client.table("items").select("*").execute()
    return render_template("list_items.html", items=items.data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



