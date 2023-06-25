from flask import request
import flask
from app import app, db
from models import Sonho, SonhoAcompanhamento


@app.route("/")
def index():
    sonhos = Sonho.query.order_by(Sonho.id)
    return flask.render_template("sonhos.html", titulo="Sonhos", sonhos=sonhos)


@app.route("/novo")
def novo():
    return flask.render_template("novo.html", titulo="Novo Sonho")


@app.route(
    "/criar",
    methods=[
        "POST",
    ],
)
def criar():
    nome = request.form["nome"]
    valor_inicial = request.form["valor_inicial"]
    valor_final = request.form["valor_final"]
    data_inicial = request.form["data_inicial"]
    data_final = request.form["data_final"]
    sonho = Sonho.query.filter_by(nome=nome).first()
    if sonho:
        flask.flash("Sonho já existente!")
    else:
        novo_sonho = Sonho(
            nome=nome,
            valor_inicial=valor_inicial,
            valor_final=valor_final,
            data_inicial=data_inicial,
            data_final=data_final,
        )
        db.session.add(novo_sonho)
        db.session.commit()

    return flask.redirect(flask.url_for("index"))


@app.route("/acompanhamento/<int:id>", methods=["GET"])
def acompanhamento(id):
    return flask.render_template(
        "novo_acompanhamento.html", titulo="Adicionar acompanhamento", sonho_id=id
    )


@app.route("/acompanhamentos", methods=["POST"])
def acompanhamentos():
    sonho_id = request.form["sonho_id"]
    valor = request.form["valor"]
    data = request.form["data"]
    acompanhamento = SonhoAcompanhamento(
        sonho_id=sonho_id,
        valor=valor,
        data=data,
    )
    db.session.add(acompanhamento)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))
