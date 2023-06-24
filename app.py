from flask import Flask
import flask
from models import Sonho

app = Flask(__name__)


@app.route("/")
def index():
    sonhos = [
        Sonho("primeiro"),
        Sonho("segundo"),
        Sonho("terceiro"),
    ]
    return flask.render_template("sonhos.html", titulo="Sonhos", sonhos=sonhos)


if __name__ == "__main__":
    app.run(debug=True)
