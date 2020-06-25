from bancodedados.conexao import configuracao_inicial
from flask_jwt import JWT, jwt_required, current_identity
from flask import Flask
from autenticacao.rotas import blueprint_autenticacao
from compra.rotas import blueprint_compra
from autenticacao.jwt import autenticar, identificar
import logging

logging.basicConfig(level=logging.DEBUG)

configuracao_inicial()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, autenticar, identificar)

app.register_blueprint(blueprint_autenticacao)
app.register_blueprint(blueprint_compra)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
