from flask import request
from flask import Blueprint
from flask_jwt import jwt_required
from utilidades.apiutil import retorno_sucesso, retorno_erro
import logging

blueprint_autenticacao = Blueprint('autenticacao', __name__, url_prefix='/autenticacao')

@blueprint_autenticacao.route('/revendedor', methods=['POST'])
def cadastro_revendedor():
    payload = request.get_json()

    from autenticacao.modelo import Usuario
    from sqlalchemy.orm import sessionmaker

    from autenticacao.servico import ServicoDeAutenticacao

    valido, erro = ServicoDeAutenticacao.validar_post_usuario(payload)
    if not valido:
        logging.info("Payload do cadastro de usuário é inválido: {}".format(str(payload)))
        return retorno_erro(erro)

    usuario = Usuario(nome=payload['nome_completo'], email=payload['email'],
                                senha=payload['senha'], cpf=payload['cpf'])
    from bancodedados import conexao
    usuario_adicionado, extra = conexao.adicionar(usuario)

    if not usuario_adicionado:
        return retorno_erro(extra)

    return retorno_sucesso(extra)
