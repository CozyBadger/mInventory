from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def hello_world():
    app.logger.info("I am alive!")
    return render_template("storage.html")
