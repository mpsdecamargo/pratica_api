from datetime import datetime
from .app import db

cliente_endereco = db.Table('cliente_endereco',
    db.Column('id_cliente', db.Integer, db.ForeignKey('clientes.id_cliente', ondelete='CASCADE'), primary_key=True),
    db.Column('id_endereco', db.Integer, db.ForeignKey('enderecos.id_endereco', ondelete='RESTRICT'), primary_key=True)
)

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(11), nullable=False, unique=True)
    data_criado = db.Column(db.DateTime, default=datetime, nullable=False)
    data_modificado = db.Column(db.DateTime, default=datetime, onupdate=datetime, nullable=False)
    emails = db.relationship('Email', backref='clientes', lazy=True, passive_deletes=True)
    enderecos = db.relationship('Endereco', secondary=cliente_endereco, backref='clientes', lazy='dynamic', passive_deletes=True)

    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

    def __repr__(self):
        return f"<Cliente(id_cliente={self.id_cliente}, nome={self.nome}, telefone={self.telefone})>"

    def to_dict(self):
        return {
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'telefone': self.telefone,
            'data_criado': self.data_criado.isoformat() if self.data_criado else None,
            'data_modificado': self.data_modificado.isoformat() if self.data_criado else None
        }

class Email(db.Model):
    __tablename__ = 'emails'

    id_email = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    data_criado = db.Column(db.DateTime, default=datetime, nullable=False)
    data_modificado = db.Column(db.DateTime, default=datetime, onupdate=datetime, nullable=False)

    def __init__(self, id_cliente, email, is_main=False):
        self.id_cliente = id_cliente
        self.email = email
        self.is_main = is_main

    def __repr__(self):
        return f"<Email(id_email={self.id_email}, email={self.email}, is_main={self.is_main})>"

    def to_dict(self):
        return {
            'id_email': self.id_email,
            'id_cliente': self.id_cliente,
            'email': self.email,
            'is_main': self.is_main,
            'data_criado': self.data_criado.isoformat(),
            'data_modificado': self.data_modificado.isoformat()
        }

class Endereco(db.Model):
    __tablename__ = 'enderecos'

    id_endereco = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    tipo_logradouro = db.Column(db.String(120), nullable=False)
    nome_logradouro = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.Integer)
    complemento = db.Column(db.String(120))
    bairro = db.Column(db.String(120), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    cidade = db.Column(db.String(120), nullable=False)
    sigla_UF = db.Column(db.String(2), nullable=False)
    país = db.Column(db.String(120), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    data_criado = db.Column(db.DateTime, default=datetime, nullable=False)
    data_modificado = db.Column(db.DateTime, default=datetime, onupdate=datetime, nullable=False)

    def __init__(self, tipo_logradouro, nome_logradouro, numero, complemento, bairro, cep, cidade, sigla_UF, país, is_main=False):
        self.tipo_logradouro = tipo_logradouro
        self.nome_logradouro = nome_logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cep = cep
        self.cidade = cidade
        self.sigla_UF = sigla_UF
        self.país = país
        self.is_main = is_main

    def __repr__(self):
        return f"{self.tipo_logradouro} {self.nome_logradouro}, {self.numero}, {self.complemento}, bairro {self.bairro} - cep: {self.cep}  - {self.cidade}, {self.sigla_UF}, {self.país}"

    def to_dict(self):
        return {
            'id_endereco': self.id_endereco,
            'tipo_logradouro': self.tipo_logradouro,
            'nome_logradouro': self.nome_logradouro,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cep': self.cep,
            'cidade': self.cidade,
            'sigla_UF': self.sigla_UF,
            'país': self.país,
            'is_main': self.is_main,
            'data_criado': self.data_criado.isoformat(),
            'data_modificado': self.data_modificado.isoformat()
        }




