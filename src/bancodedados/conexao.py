from sqlalchemy import create_engine
import logging

engine = create_engine('mysql://user:pass@mysql:3306/vendas', echo=True)

def adicionar(entidade):
    from sqlalchemy.orm import sessionmaker
    from erros.erros import CodigosDeErro
    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()
    from sqlalchemy import exc

    logging.debug("Adicionando registo na tabela: {}".format(entidade.__tablename__))
    try:
        session.add(entidade)
        session.flush()
        session.commit()
        entidade = entidade.get_dict()
    except exc.IntegrityError as e:
        logging.error(e)
        session.rollback()
        return False, CodigosDeErro("{}_01".format(entidade.get_codigo()))
    except Exception as e:
        logging.error(e)
        return False, CodigosDeErro("ERRO_INESPERADO")
    finally:
        session.close()
    return True, entidade

def buscar(entidade, campos_retorno=None, **parametros_de_busca):
    from sqlalchemy.orm import sessionmaker
    from erros.erros import CodigosDeErro
    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()
    from sqlalchemy import exc

    resultado = []
    logging.debug("Buscando: {}".format(entidade.__tablename__))
    try:
        for item in session.query(entidade).filter_by(**parametros_de_busca).all():
            resultado.append(item.get_dict(campos_retorno))
    except Exception as e:
        logging.error(e)
    finally:
        session.close()

    return resultado

def configuracao_inicial():
    from sqlalchemy import MetaData, Table, Column, Integer, Numeric, String, Date, ForeignKeyConstraint
    logging.info("Criando tabelas no Banco de dados")

    meta = MetaData()
    Table(
       'usuario', meta,
       Column('id', Integer, primary_key=True, autoincrement=True),
       Column('nome', String(512), nullable=False),
       Column('email', String(128), unique=True, nullable=False),
       Column('cpf', String(11), unique=True, nullable=False),
       Column('senha', String(512), nullable=False),
    )

    Table(
       'compra', meta,
       Column('id', Integer, primary_key=True, autoincrement=True),
       Column('codigo', String(50), unique=True, nullable=False),
       Column('status', String(25), nullable=False),
       Column('valor', Numeric(precision=9, scale=2), nullable=False),
       Column('data', Date, nullable=False),
       Column('id_usuario', Integer, nullable=False),
       ForeignKeyConstraint(['id_usuario'],['usuario.id'])
    )
    meta.create_all(engine)
