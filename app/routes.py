from flask import Flask, Blueprint, jsonify, render_template, request,redirect, url_for, session, flash
from .config import Config
from .models import Cliente, Email, Endereco, cliente_endereco
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_restx import Api, Resource, fields
from .app import db

api_bp = Blueprint('api', 'api', __name__, url_prefix='/api/v1')
api_v1 = Api(api_bp, doc='/doc',version='1.0', title='API REST - Prática Specialisterne - XP', description='Autor: Marcos de Camargo')


session = db.session

modelo_cliente = api_v1.model('ClienteResource', {
    'id_cliente': fields.Integer(required=True, description='ID do cliente', example=1),
    'nome': fields.String(required=True, description='Nome completo do cliente'),
    'telefone': fields.String(required=True, description='Telefone do cliente'),
    'email': fields.String(required=True, description='Email do cliente'),
    'data_criado': fields.DateTime(required=False, description='Data de criação'),
    'data_modificado': fields.DateTime(required=False, description='Data de modificação')
    })

modelo_email = api_v1.model('Email', {
    'email': fields.String(required=True, description='Email do cliente')
    })

@api_v1.doc()





@api_v1.route('/users')
class ClienteList(Resource):
    def get(self):
        """Listar clientes cadastrados"""
        clientes = Cliente.query.all()
        return jsonify([cliente.to_dict() for cliente in clientes])

@api_v1.route('/user')
class ClienteResource(Resource):
    @api_v1.expect(modelo_cliente)
    def post(self):
        """Cria usuários"""
        data = request.get_json()

        if 'nome' not in data or 'telefone' not in data:
            return jsonify({'message': 'Verifique se o nome e o telefone estão preenchidos'}), 400
        novo_cliente = Cliente(nome=data['nome'], telefone=data['telefone'])
        try:
            session.add(novo_cliente)
            print(novo_cliente)
            session.commit()
            if 'email' in data:
                email_cadastro = Email(email=data['email'], id_cliente=novo_cliente.id_cliente, is_main=True)
                try:
                    session.add(email_cadastro)
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    print(e)
        except SQLAlchemyError as e:
            session.rollback()
            print(e)

        dados_cliente = Cliente.to_dict(novo_cliente)
        if 'email' in data:
                dados_cliente["email"] = email_cadastro.email
        dados_cliente["message"] = "Novo cliente criado"

        return jsonify(dados_cliente)

@api_bp.route('/users/<int:id_cliente>', methods=['GET'])
def encontrar_cliente_por_id(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente, description = "Cliente não encontrado")
    email = next((email for email in cliente.emails if email.is_main), None)

    dados_cliente = cliente.to_dict()

    if email:
        dados_cliente['email'] = email.to_dict()
    return jsonify(dados_cliente.to_dict())

@api_bp.route('/users/<int:id_cliente>/emails', methods=['GET'])
def encontrar_emails_cliente_por_id(id_cliente):
    emails_cliente = Email.query.filter_by(id_cliente=id_cliente).all()

    if not emails_cliente:
        return jsonify({'message': 'Não foram encontrados emails para esse cliente'}), 404
    return jsonify({email.to_dict() for email in emails_cliente})

@api_bp.route('/users/<int:id_cliente>/adresses', methods=['GET'])
def encontrar_enderecos_cliente_por_id(id_cliente):
    enderecos_cliente = Endereco.query.filter_by(id_cliente=id_cliente).all()

    if not enderecos_cliente:
        return jsonify({'message': 'Não foram encontrados endereços para esse cliente'}), 404
    return jsonify({endereco.to_dict() for endereco in enderecos_cliente})

@api_v1.route('/users/<int:id_cliente>/details', methods=['GET'])

class Details(Resource):
    def get(self, id_cliente):
        """Listar detalhes do cliente"""
        cliente = Cliente.query.get_or_404(id_cliente, description = "Cliente não encontrado")
        email_principal = Email.query.filter_by(id_cliente=id_cliente, is_main=True).first_or_404(description = "Não há email principal para esse cliente")
        endereco_principal = Endereco.query.join(cliente_endereco).filter(cliente_endereco.c.id_cliente == id_cliente, Endereco.is_main == True).first_or_404(description="Não há endereço principal para esse cliente")
        endereco_str = str(endereco_principal)
        return jsonify({"message": "Detalhes para cliente encontrados", "id_cliente": cliente.id_cliente, "nome": cliente.nome, "email" : email_principal.email, "endereco": endereco_str})



@api_bp.route('/users/<int:id_cliente>', methods=['PUT'])
def editar_cliente_por_id(id_cliente):
    return ""

@api_bp.route('/users/<int:id_cliente>', methods=['DELETE'])
def excluir_cliente_pot_id(id_cliente):
    return ""

@api_bp.route('/emails', methods=['GET'])
def listar_emails():
    emails = session.query(Email).all()

    if emails.count == 0:
        return jsonify({"message": "Não foram encontrados emails"})
    return jsonify([email.to_dict() for email in emails])

@api_bp.route('/adresses', methods=['GET'])
def listar_enderecos():
    enderecos = session.query(Endereco).all()
    if enderecos.count == 0:
        return jsonify({"message": "Não foram encontrados endereços"})
    return jsonify([endereco.to_dict() for endereco in enderecos])