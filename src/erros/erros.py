class CodigosDeErro(object):

    MAPEAMENTO_DE_ERROS = {
        "AUT_01": "Usuário já cadastrado.",
        "AUT_21": "Nome completo inválido.",
        "AUT_22": "E-mail inválido.",
        "AUT_23": "CPF inválido.",
        "AUT_24": "Senha inválida.",
        "COM_01": "Compra já cadastrada.",
        "COM_21": "O cpf informado não está cadastrado.",
        "COM_22": "Codigo de compra inválido.",
        "COM_23": "O cpf é inválido.",
        "COM_24": "O valor é inválido.",
        "COM_25": "Data inválida.",
        "COM_26": "A compra não pertence ao usuário authenticado.",
        "COM_27": "Não foi possível calcular o cashbash. Tente novamente mais tarde.",
        "ERRO_INESPERADO": "Houve um erro inesperado, tente novamente.",
    }

    def __init__(self, codigo):
        self.codigo = codigo
        self.mensagem = self.MAPEAMENTO_DE_ERROS.get(codigo, "Ocorreu um erro inesperado.")

    def get_mensagem(self):
        return self.mensagem

    def get_codigo(self):
        return self.codigo
