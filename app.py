from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv  # noqa: F401

load_dotenv()

app = Flask(__name__)

app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

from views import *  # noqa: E402 F401 F403 # import das rotas após configuração do app

if __name__ == "__main__":
    app.run(debug=True)
