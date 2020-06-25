from flask import request
from flask import Blueprint
from flask_jwt import jwt_required
from utilidades.apiutil import retorno_sucesso, retorno_erro
import logging
from datetime import datetime
from flask_jwt import current_identity

blueprint_compra = Blueprint('compra', __name__, url_prefix='/compra')

@blueprint_compra.route('/', methods=['GET'])
@jwt_required()
def listar_compras():

    from compra.modelo import Compra
    from bancodedados import conexao
    from compra.servico import ServicoDeCompra

    compras = conexao.buscar(Compra, id_usuario=current_identity.id, campos_retorno=["codigo", "valor", "data", "status"])
    valores_cashback = ServicoDeCompra.calcular_cashback(compras)

    for compra in compras:
        mes = compra['data'][3:]
        porcentagem = valores_cashback[mes]['porcentagem']
        cashback = {
            'porcentagem': porcentagem,
            'valor': float('%g' % (compra['valor'] * porcentagem))
        }
        compra['cashback'] = cashback

    return retorno_sucesso(compras)

@blueprint_compra.route('/', methods=['POST'])
@jwt_required()
def cadastro_compra():
    payload = request.get_json()

    from bancodedados import conexao
    from compra.modelo import Compra
    from autenticacao.modelo import Usuario
    from sqlalchemy.orm import sessionmaker
    from compra.servico import ServicoDeCompra

    valido, error = ServicoDeCompra.validar_post_compra(payload)
    if not valido:
        return retorno_erro(error)

    if current_identity.usuario['cpf'] != payload['cpf']:
        from erros.erros import CodigosDeErro
        return retorno_erro(CodigosDeErro('COM_26'))

    try:
        id_usuario = conexao.buscar(Usuario, cpf=payload['cpf'], campos_retorno=["id"])[0]['id']
    except:
        logging.debug("Usuário com cpf {} não foi encontrado.".format(payload['cpf']))

        from erros.erros import CodigosDeErro
        return retorno_erro(CodigosDeErro('COM_21'))

    data = datetime.strptime(payload['data'], '%d-%m-%Y')

    parametros_compra = {
        'codigo': payload['codigo'],
        'valor': payload['valor'],
        'data': data,
        'id_usuario': id_usuario,
        'status': 'Em validação'
    }
    if payload['cpf'] == "15350946056":
        parametros_compra['status'] = "Aprovado"

    compra = Compra(**parametros_compra)
    from bancodedados import conexao
    compra_adicionada, extra = conexao.adicionar(compra)

    if not compra_adicionada:
        return retorno_erro(extra)

    return retorno_sucesso(extra)

@blueprint_compra.route('/cashback', methods=['GET'])
@jwt_required()
def listar_cashback():

    import requests
    from compra.modelo import Compra
    from bancodedados import conexao
    from compra.servico import ServicoDeCompra

    compras = conexao.buscar(Compra, id_usuario=current_identity.id, campos_retorno=["codigo", "valor", "data", "status"])
    cashbacks = ServicoDeCompra.calcular_cashback(compras)
    valor_acumulado = {}

    url = "https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf={}".format(current_identity.usuario['cpf'])
    headers = {'token': 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'}

    for mes, cashback in cashbacks.items():
        requisicao = requests.get(url, headers=headers)
        if not requisicao.ok:
            from erros.erros import CodigosDeErro
            return retorno_erro(CodigosDeErro('COM_27'))

        valor_acumulado[mes] = requisicao.json()['body']['credit']

    return retorno_sucesso(valor_acumulado)
