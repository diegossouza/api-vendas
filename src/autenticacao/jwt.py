class UsuarioJWT(object):
    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario

    def __str__(self):
        return "User(id='%s')" % self.id

def autenticar(usuario, senha):
    from autenticacao.modelo import Usuario
    from bancodedados import conexao

    lista = conexao.buscar(Usuario, email=usuario, campos_retorno=["id", "nome", "senha"])
    if lista:
        usuario = lista[0]
        senha_valida = Usuario._get_senha_hash(senha, usuario['senha']) == usuario['senha']

        if senha_valida:
            return UsuarioJWT(lista[0]['id'], usuario)
    return None

def identificar(payload):
    from autenticacao.modelo import Usuario
    from bancodedados import conexao

    lista = conexao.buscar(Usuario, id=payload['identity'])

    if lista:
        return UsuarioJWT(lista[0]['id'], lista[0])
    else:
        return None
