
class ServicoDeAutenticacao(object):

    @staticmethod
    def validar_post_usuario(json_post):

        from erros.erros import CodigosDeErro
        from autenticacao.modelo import COD_ERRO_USUARIO

        nome = json_post.get("nome_completo")
        email = json_post.get("email")
        cpf = json_post.get("cpf")
        senha = json_post.get("senha")

        print(">>>>>>", str(senha))

        if not nome or len(nome.split()) < 2 or not isinstance(nome, str):
            return False, CodigosDeErro('{}_21'.format(COD_ERRO_USUARIO))

        import re
        valido=re.search(r'^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$',email)

        if not email or not valido or not isinstance(email, str):
            return False, CodigosDeErro('{}_22'.format(COD_ERRO_USUARIO))

        if not cpf or not cpf.isnumeric() or len(cpf) != 11 or not not isinstance(cpf, str):
            return False, CodigosDeErro('{}_23'.format(COD_ERRO_USUARIO))

        if not senha or not isinstance(senha, str):
            return False, CodigosDeErro('{}_24'.format(COD_ERRO_USUARIO))

        return True, None
