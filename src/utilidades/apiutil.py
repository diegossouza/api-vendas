from flask import Response
import json

def retorno_sucesso(dados):
    info = {
        "status" : "sucesso",
        "dado" : dados
    }

    return Response(json.dumps(info), status=200, mimetype='application/json')

def retorno_erro(erro, status=500):
    info = {
        "status": "erro",
        "mensagem": erro.get_mensagem(),
        "codigo": erro.get_codigo()
    }

    return Response(json.dumps(info), status=status, mimetype='application/json')
