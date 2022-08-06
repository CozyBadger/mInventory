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
