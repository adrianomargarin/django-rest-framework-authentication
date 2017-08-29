# django-rest-framework-authentication

## Como desenvolver?

1. Clone o repositório.
2. Crie um virtualenv com Python 3.6
3. Ative o virtualenv.
4. Instale as dependências.
5. Configure a instância com o .env
6. Execute os testes.

```console
git clone git@github.com:adrianomargarin/django-rest-framework-authentication.git
cd django-rest-framework-authentication
virtualenv env --python=python3
source env/bin/activate
pip install -r requirements_dev.txt
cp contrib/env-sample .env
python manage.py test

```

## Como fazer o deploy?

1. Crie uma instância no heroku.
2. Envie as configurações para o heroku.
3. Define um SECRET_KEY segura para instância.
4. Defina DEBUG=True
5. Configure o serviço de email.
6. Envie o código para o heroku.

```console
heroku create minhainstancia

heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False

git push heroku master --force
```

## Testando:

```python
POST https://drf-authentication.herokuapp.com/login/

headers:
  "Content-Type": "application/json"

body:
  {
	  "username": "adrianomargarin",
	  "password": "asdf1234"
  }
  
response:
  {
    "token": "token-gerado"
  }
```

Com o token gerado, faça o próximo passo:

```python
GET https://drf-authentication.herokuapp.com/user/

headers:
  "Content-Type": "application/json"
  "Authorization": "Basic token-gerado-em-base64"

response:
  {
    "username": "adrianomargarin",
    "first_name": "",
    "last_name": ""
  }
```
