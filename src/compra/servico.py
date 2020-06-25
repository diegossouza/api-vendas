
class ServicoDeCompra(object):

    @staticmethod
    def validar_post_compra(json_post):

        from erros.erros import CodigosDeErro
        from compra.modelo import COD_ERRO_COMPRA

        codigo = json_post.get("codigo")
        valor = json_post.get("valor")
        cpf = json_post.get("cpf")
        data = json_post.get("data")

        if not codigo or not isinstance(codigo, str):
            return False, CodigosDeErro('{}_22'.format(COD_ERRO_COMPRA))

        if not cpf or not cpf.isnumeric() or not isinstance(cpf, str) or len(cpf) != 11:
            return False, CodigosDeErro('{}_23'.format(COD_ERRO_COMPRA))

        if not valor or not isinstance(valor, float):
            return False, CodigosDeErro('{}_24'.format(COD_ERRO_COMPRA))

        import re
        valido=re.search(r'^[0-9]{2}-[0-9]{2}-[0-9]{4}$', data)
        if not data:
            return False, CodigosDeErro('{}_25'.format(COD_ERRO_COMPRA))

        return True, None

    @staticmethod
    def calcular_cashback(compras):

        def porcentagem_cashback(valor):
            if valor <= 1000.0:
                return 0.1
            elif valor <= 1500.0:
                return 0.15

            return 0.2

        cashback = {}
        for compra in compras:
            mes = compra['data'][3:]
            valor_compra = compra['valor']

            valor_acumulado = cashback.get(mes, {}).get('valor_acumulado', 0.0) + valor_compra
            cashback[mes] = {
                'valor_acumulado': valor_acumulado,
                'porcentagem': porcentagem_cashback(valor_acumulado)
            }

        return cashback
