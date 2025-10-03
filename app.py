import sqlite3
from flask import Flask, render_template, request, flash, url_for
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key= "Secure_key_ewuiy"

def get_conn():
    conn = sqlite3.connect("data/products.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "POST":
        product_name = request.form.get("product_name")

        try:
            quantity = int(request.form.get("quantity"))
            if quantity < 0:
                flash("Quantity cannot be negative", "error")
                return redirect(url_for("products"))
        except (TypeError, ValueError):
            flash("Please enter a numeric value for Quantity", "error")
            return redirect(url_for("products"))

        try:
            price = float(request.form.get("price"))
            if price < 0:
                flash("Price cannot be negative", "error")
                return redirect(url_for("products"))
        except (TypeError, ValueError):
            flash("Please enter a numeric value for Price", "error")
            return redirect(url_for("products"))

        try:
            with get_conn() as conn:
                conn.execute(
                    "INSERT INTO products (product_name, quantity, price) VALUES (?, ?, ?)",
                    (product_name, quantity, price)
                )
                flash("Product added successfully!", "success")
        except Exception as e:
            flash(f"Something went wrong: {e}", "error")

        return redirect(url_for("products"))


    with get_conn() as conn:
        products = conn.execute("SELECT product_id, product_name, quantity, price FROM products" ).fetchall()

    return render_template("products.html", products=products)

@app.route("/products/delete/<int:product_id>", methods=["POST"])
def delete_products(product_id):
    try:
        with get_conn() as conn:
            conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
            flash("Product deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting Product: {e}","error")

    return redirect(url_for("products"))

@app.route("/search",methods=["GET", "POST"])
def search():
    name = request.form.get("name")

    with get_conn() as conn:
        result = conn.execute("Select * FROM products WHERE product_name = ?", (name,))
    return render_template("products.html", products=result)

if __name__ == '__main__':
    app.run(debug=True)

