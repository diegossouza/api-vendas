from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

COD_ERRO_USUARIO = "AUT"

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)
    cpf = Column(String)

    def __init__(self, **kwargs):
        kwargs['senha'] = Usuario._get_senha_hash(kwargs['senha'])
        super().__init__(**kwargs)

    def get_codigo(self):
        return COD_ERRO_USUARIO

    def get_dict(self, campos=None):
        dict = {}
        if not campos:
            campos = ["id", "nome", "email", "cpf"]

        for campo in campos:
            dict[campo] = getattr(self, campo)

        return dict

    @staticmethod
    def _get_senha_hash(senha, salt=None):
        import bcrypt
        if not salt:
            salt = bcrypt.gensalt()

        return  bcrypt.hashpw(senha, salt)
