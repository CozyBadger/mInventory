from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

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

    # Check input validity
    if item and amount and unit:
        pass
    else:
        flash("Missing required input. No item added.", "danger")
        return redirect("/")

    flash(f"Item {item} added with {amount} {unit}", "primary")
    return redirect("/")
