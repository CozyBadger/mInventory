# Public imports
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

import sqlite3

# Local imports
from helpers import db_connect, format_items, validate_string

# Configure the Flask application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Local database
db = "minventory.db"

@app.route("/")
def root():
    app.logger.debug("I am alive!")
    conn = db_connect(db)
    cur = conn.cursor()
    entries = cur.execute("SELECT * FROM storage;").fetchall()

    conn.close()
    app.logger.debug(f"Items returned: {entries}")
    return render_template("index.html", storage_items=format_items(entries))


@app.route("/add_item", methods=["POST"])
def add_item():
    """ Add an item to the database """

    item = request.form.get("item")
    app.logger.debug(f"Item from form: {item}")

    amount = request.form.get("amount")
    app.logger.debug(f"Amount from form: {amount}")

    unit = request.form.get("unit")
    app.logger.debug(f"Unit from form: {unit}")

    # Check if all inputs are given
    if not item or not amount or not unit:
        flash("Missing required input. No item added.", "danger")
        return redirect("/")

    # Check if inputs are of allowed types
    try:
        int(amount)
    except ValueError:
        flash("Amount must be a number.", "danger")
        return redirect("/")

    if validate_string(item) is False or validate_string(unit) is False:
        flash("No special characters or numbers allowed for items and units", "danger")
        return redirect("/")

    # Write item details to database
    conn = db_connect(db)
    conn.execute(
        "INSERT INTO storage (item_name, amount, unit) VALUES (?, ?, ?)",
        (item, amount, unit)
    )

    conn.commit()
    conn.close()

    # Acknolegde success and return to root
    flash(f"Item {item} added with {amount} {unit}", "primary")
    return redirect("/")

@app.route("/remove_item", methods=["GET", "POST"])
def remove_item():
    """ Remove a specified amount of an item from the database """
    item_id = request.args.get("id")
    app.logger.debug(f"Getting info for item id: {item_id}")

    # Retrieve item information to populate form if item id is given
    if item_id:
        conn = db_connect(db)
        cur = conn.cursor()
        item_details = cur.execute("SELECT * FROM storage WHERE id = ?", item_id).fetchall()

        app.logger.debug(f"Item info fetched: {item_details}")

        return render_template("remove_item.html", item_details=format_items(item_details)[0])

    if request.method == "POST":

        flash("Item removed", "primary")
        return redirect("/")

    return render_template("remove_item.html")
