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
    entries = cur.execute("SELECT * FROM storage").fetchall()

    conn.close()
    app.logger.debug(f"Items returned: {entries}")
    return render_template("index.html", storage_items=format_items(entries))


@app.route("/add_item", methods=["POST"])
def add_item():
    """ Add an item to the database """
    # TODO: unify entries for same name items into one item / avoid double entries for same or even similar item names

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
        # using fetchall() although ID is unique and always should return one - but who knows?
        item_details = cur.execute("SELECT * FROM storage WHERE id = (?)", (item_id,)).fetchall()
        conn.close()

        app.logger.debug(f"Item info fetched: {item_details}")

        return render_template("remove_item.html", item_details=format_items(item_details)[0])

    # Handling POST requests
    if request.method == "POST":

        item_id = request.form.get("item_id")
        remove_amount = request.form.get("amountNumber")

        # Check if required inputs are present
        if not item_id or not remove_amount:
            flash(f"Required input missing. No items removed.", "danger")
            return redirect("/")

        # Check if types are correct
        try:
            int(item_id)
            remove_amount = int(remove_amount)
        except ValueError:
            flash(f"Input type error for item id or amount (not int).", "danger")
            return redirect("/")

        # Get item information if exisits
        conn = db_connect(db)
        cur = conn.cursor()
        current_item = cur.execute("SELECT * FROM storage WHERE id = (?)", (item_id,))
        # no need to close connection yet

        # return early if query did not retrieve anything
        if current_item == []:
            flash(f"No item with ID {item_id} found in database.", "danger")
            return redirect("/")

        current_item = format_items(current_item)[0]

        try:
            available_amount = current_item.get("amount")
            item_name = current_item.get("item_name")
        except:
            # TODO create more meanigful exception handling
            flash("Database did not return expected values", "danger")
            return redirect("/")


        # remove nothing if remove amount is 0 or negative
        if remove_amount <= 0:
            conn.close()
            flash(f"Nothing removed from item {item_name}", "primary")
            return redirect("/")

        # remove item from storage completely if remove amount equals what is available
        changes_made = False

        if changes_made == False and available_amount - remove_amount == 0:
            conn.execute("DELETE FROM storage WHERE id = (?)", (item_id,))
            changes_made = True
        elif changes_made == False and available_amount - remove_amount > 0:
            new_amount = available_amount - remove_amount
            conn.execute("UPDATE storage SET amount = (?) WHERE id = (?)", (new_amount, item_id))
            changes_made = True

        if changes_made == True:
            conn.commit()
            conn.close()
        else:
            conn.close()
            flash("Something went wrong when making changes to the DB", "danger")
            return redirect("/")

        flash("Item removed", "primary")
        return redirect("/")

    # Leaving this for GET requests
    return render_template("remove_item.html")
