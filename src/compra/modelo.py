from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

COD_ERRO_COMPRA = "COM"

class Compra(Base):
    __tablename__ = 'compra'
    id = Column(Integer, primary_key=True)
    codigo = Column(String)
    status = Column(String)
    valor = Column(Numeric, default="Em validação")
    data = Column(Date)
    id_usuario = Column(Integer)

    def get_codigo(self):
        return COD_ERRO_COMPRA

    def get_dict(self, campos=None):
        dict = {}
        if not campos:
            campos = ["id", "codigo", "valor", "data", "status"]

        for campo in campos:
            if campo == 'data':
                dict[campo] = self.data.strftime("%d-%m-%Y")
            elif campo == 'valor':
                dict[campo] = float(self.valor)
            else:
                dict[campo] = getattr(self, campo)

        return dict
