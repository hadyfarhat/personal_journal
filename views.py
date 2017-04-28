from flask import (Flask, render_template, g)

app = Flask(__name__)


@app.route("/entries")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)