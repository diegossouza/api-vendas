# Api-Compras

Backend de uma api de cadastro de compras com cashback.
- O objetivo do projeto é exercitar o desenvolvimento em Python de uma API.

## Características técnicas

O projeto foi desenvolvido utilizando Python 3 como linguagem e as principais tecnologias e frameworks são:
- [Docker](https://www.docker.com/) para criação dos containers que executam a aplicação
    - [Imagem Python](https://hub.docker.com/_/python)
    - [Imagem Mysql](https://hub.docker.com/_/mysql)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) como framework base para a aplicação web e api
- [Flask-JWT](https://pythonhosted.org/Flask-JWT/) para autenticação dos usuários.
- [SQLAlchemy](https://www.sqlalchemy.org/) para mapeamento objeto-relacional SQL (ORM).

## Instalação

Para executar a aplicação, basta realizar os passos a seguir:

1. Fazer a cópia do repositório
```shell
git clone https://github.com/diegossouza/api-vendas.git
```

2. Fazer o build da aplicação
```shell
sudo docker-compose build
```

3. Iniciar o servidor local
```shell
 sudo docker-compose up
```

4. Feito isso a aplicação está disponível na porta 5000

## Endpoints:

### Cadastro do vendedor

```json
POST /autenticacao/revendedor HTTP/1.1
Accept: application/json
Content-Type: application/json

{
	"nome_completo": "Nome Completo",
	"senha": "senhaXYZ",
	"cpf": "11122233300",
	"email": "teste@email.com.br"
}
```
**Resposta de sucesso:**
```json
HTTP/1.1 200 OK
{
	"status": "sucesso",
	"dado": {
		"id": 1,
		"nome_completo": "Nome Completo",
		"cpf": "11122233300",
		"email": "teste@email.com.br"
	}
}
```
**Resposta de erro:**
```json
HTTP/1.1 500 OK
{
  "status": "erro",
  "mensagem": "Causa do erro.",
  "codigo": "COD_00"
}
```

### Autenticação do vendedor

```json
POST /auth HTTP/1.1
Accept: application/json
Content-Type: application/json

{
	"username": "teste@email.com.br",
	"password": "senhaXYZ"
}
```
**Resposta de sucesso:**
```json
HTTP/1.1 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTMwNTc3NDcsImlhdCI6MTU5MzA1NzQ0NywibmJmIjoxNTkzMDU3NDQ3LCJpZGVudGl0eSI6MTF9.4oXmcOm4n6-1SVFHKDpEQa8zmj7svmcRieDNZslkwv4"
}
```
**Resposta de erro:**
```json
HTTP/1.1 500 OK
{
  "description": "Invalid credentials",
  "error": "Bad Request",
  "status_code": 401
}
```

### Cadastro de compra
*requer autenticação JWT

```json
POST /compra HTTP/1.1
Accept: application/json
Content-Type: application/json

{
	"codigo": "COD-1",
	"valor": 31.5,
	"data": "15-04-2020",
	"cpf": "11122233300"
}
```
**Resposta de sucesso:**
```json
HTTP/1.1 200 OK
{
  "status": "sucesso",
  "dado": {
    "id": 13,
    "codigo": "COD-1",
    "valor": 31.5,
    "data": "15-04-2020",
    "status": "Em validação"
  }
}
```
**Resposta de erro:**
```json
HTTP/1.1 500 OK
{
  "status": "erro",
  "mensagem": "Causa do erro.",
  "codigo": "COD_00"
}
```

### Lista de compras
*requer autenticação JWT

```json
GET /compra/ HTTP/1.1
Content-Type: application/json
```
**Resposta de sucesso:**
```json
HTTP/1.1 200 OK
{
  "status": "sucesso",
  "dado": [
    {
      "codigo": "COD-1",
      "valor": 31.5,
      "data": "01-06-2020",
      "status": "Em validacao",
      "cashback": {
        "porcentagem": 0.1,
        "valor": 3.15
      }
    },
    {
      "codigo": "COD-2",
      "valor": 31.5,
      "data": "15-06-2020",
      "status": "Em validação",
      "cashback": {
        "porcentagem": 0.1,
        "valor": 3.15
      }
    }
  ]
}
```
**Resposta de erro:**
```json
HTTP/1.1 500 OK
{
  "status": "erro",
  "mensagem": "Causa do erro.",
  "codigo": "COD_00"
}
```

### Extrato mensal do cashback
*requer autenticação JWT

```json
GET /compra/cashback HTTP/1.1
Content-Type: application/json
```
**Resposta de sucesso:**
```json
HTTP/1.1 200 OK
{
  "status": "sucesso",
  "dado": {
    "04-2020": 2514
  }
}
```
**Resposta de erro:**
```json
HTTP/1.1 500 OK
{
  "status": "erro",
  "mensagem": "Causa do erro.",
  "codigo": "COD_00"
}
```
