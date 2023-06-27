from flask import request
import flask
from datetime import datetime

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


@app.route("/acompanhamento", methods=["POST"])
def acompanhamento():
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

    return flask.redirect(flask.url_for("sonho_detalhes", id=sonho_id))


@app.route("/sonho_detalhes/<int:id>", methods=["GET"])
def sonho_detalhes(id):
    sonho = Sonho.query.filter_by(id=id).first()
    acompanhamentos = SonhoAcompanhamento.query.filter_by(sonho_id=id).order_by(
        SonhoAcompanhamento.data.desc()
    )
    return flask.render_template(
        "sonho_detalhes.html",
        titulo="Sonho Acompanhamento",
        sonho=sonho,
        acompanhamentos=acompanhamentos,
    )


@app.route("/sonho_detalhes_json/<int:id>", methods=["GET"])
def sonho_detalhes_json(id):
    acompanhamentos = SonhoAcompanhamento.query.filter_by(sonho_id=id).order_by(
        SonhoAcompanhamento.data
    )

    line = [["data", "valor"]]
    for ac in acompanhamentos:
        line.append([str(ac.data)[:10], ac.valor])

    return line


def calcular_taxa_juros_anual(
    valor_inicial, data_inicial, valor_final, data_final, aporte_anual
):
    # Cálculo do número total de dias entre as datas
    dias_totais = (data_final - data_inicial).days

    # Cálculo da taxa de juros anual iterativamente
    taxa_juros = 0.01  # Valor inicial para a taxa de juros (1%)
    precisao = 0.0001  # Precisão desejada
    valor_atual = valor_inicial

    while valor_atual < valor_final:
        valor_atual = valor_inicial
        for ano in range(1, (dias_totais // 365) + 1):
            valor_atual += aporte_anual
            valor_atual *= 1 + taxa_juros

        if valor_atual < valor_final:
            taxa_juros += precisao

    return taxa_juros


@app.route("/sonho_planejado_json/<int:id>", methods=["GET"])
def sonho_planejado_json(id):
    sonho = Sonho.query.filter_by(id=id).first()

    line = [["data", "valor"]]
    data = sonho.data_inicial
    valor = sonho.valor_inicial
    if valor == 0:
        valor = 1
    aporte_anual = 24000
    taxa_juros = calcular_taxa_juros_anual(
        valor, sonho.data_inicial, sonho.valor_final, sonho.data_final, aporte_anual
    )
    print(taxa_juros)
    line.append([str(data)[:10], valor])
    while data <= sonho.data_final:
        data = datetime(data.year + 1, data.month, data.day)
        valor += valor * taxa_juros + aporte_anual
        line.append([str(data)[:10], valor])

    return line
