from app import db


class Sonho(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    data_inicial = db.Column(db.DateTime, nullable=False)
    data_final = db.Column(db.DateTime, nullable=False)
    valor_inicial = db.Column(db.Double, nullable=False)
    valor_final = db.Column(db.Double, nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.nome


class SonhoAcompanhamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sonho_id = db.Column(db.Integer)
    data = db.Column(db.DateTime, nullable=False)
    valor = db.Column(db.Double, nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.nome
