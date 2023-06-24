import os

SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(
    SGBD="mysql+mysqlconnector",
    usuario=os.getenv("USER_DB"),
    senha=os.getenv("PWD_DB"),
    servidor=os.getenv("HOST"),
    database="savings_tracker",
)
