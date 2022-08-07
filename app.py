# Public packages
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

import re

# Local packages
from helpers import validate_string

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def root():
    app.logger.info("I am alive!")
    return render_template("index.html")


@app.route("/add_item", methods=["POST"])
def add_item():
    """ Add an item to the database """

    item = request.form.get("item")
    app.logger.info(f"Item from form: {item}")

    amount = request.form.get("amount")
    app.logger.info(f"Amount from form: {amount}")

    unit = request.form.get("unit")
    app.logger.info(f"Unit from form: {unit}")

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

    # Acknolegde success and return to root
    flash(f"Item {item} added with {amount} {unit}", "primary")
    return redirect("/")
